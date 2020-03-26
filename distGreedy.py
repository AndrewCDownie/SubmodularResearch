from modules.submodular_sim import submodular_sim

from modules.visualization import visualization
from shapely.geometry import Point
from math import sqrt, pi
import random
import matplotlib.pyplot as plt

def h(dist,fx,l):
    P = Point(0,0).buffer(sqrt(fx/pi))
    Pg = Point(dist,0).buffer(sqrt(l/pi))
    return P.intersection(Pg).area

def g(dist,fx,U):
    P = Point(0,0).buffer(sqrt(fx/pi))
    Ph = Point(dist,0).buffer(sqrt(U/pi))
    return P.intersection(Ph).area

def crappyg(dist,fx,a,b):
    P = Point(0,0).buffer(sqrt(fx/pi))
    d = (sqrt(fx/pi)+sqrt(a/pi))*(dist/(1+sqrt(fx/pi)+sqrt(b/pi)))
    Pg = Point(d,0).buffer(sqrt(a/pi))
    return (fx/a)*P.intersection(Pg).area



def marginalCrappy(x,S,a,b):
    fx = Point(0,0).buffer(x['r']).area
    marg = fx
    for s in S:
        d = submodular_sim.dist_(x,s)
        marg += -crappyg(d,fx,a,b)
    return max([marg,0])


def marginalH(x,S,a):
    fx = Point(0,0).buffer(x['r']).area
    marg = fx
    if len(S) == 0:
        return marg
    xi =max(S,key=lambda xi:h(submodular_sim.dist_(x,xi),fx,a))
    marg -= h(submodular_sim.dist_(x,xi),fx,a)
    return max([marg,0])

def marginal(x,S,b):
    fx = Point(0,0).buffer(x['r']).area
    marg = fx
    for s in S:
        d = submodular_sim.dist_(x,s)
        marg += -g(d,fx,b)
    return max([marg,0])



def dGreedy(X,n,a,b):
    
    S = []
    Xn = X.copy()
    while len(S)<n:
        xi = max(Xn,key=lambda x: marginal(x,S,b))
        #print(xi)
        S.append(xi)
        Xn.remove(xi)
    return S


def dGreedyCrappy(X,n,a,b):
    S = []
    Xn = X.copy()
    while len(S)<n:
        xi = max(Xn,key=lambda x: marginalCrappy(x,S,a,b))
        #print(xi)
        S.append(xi)
        Xn.remove(xi)
    return S


def calculateLowerBound(X,b):
    X = X.copy()
    S = []
    f = 0
    for x in X:
        f += marginal(x,S,b)
        S.append(x)
    return f


def calculateLowerBoundCrappy(X,a,b):
    X = X.copy()
    S = []
    f = 0
    for x in X:
        f += marginalCrappy(x,S,a,b)
        S.append(x)
    return f


def calcApproximationRatio(sim,X,a,b):
    S = [X[0]]
    ratios = []
    for x in X[1:]:
        upper = sim.coverage(S)
        lower = calculateLowerBound(S,b)
        ratios.append(upper/lower)
        S.append(x)
    return ratios




def main():

    a = 250
    b = 300

    n = 70
    dims = [100,100]
    X = [{"x":random.random()*dims[0], "y":random.random()*dims[1], "r":sqrt(random.randint(a,b)/pi)} for i in range(100)]
    sim = submodular_sim(X,dims = dims)

    sim.f = sim.coverage
    print("Running Regular Greedy...")
    S1 = sim.greedy(n)
    """
    print("running Dist Greedy...")
    S2 = dGreedy(X,n,a,b)
    print("running Dist Greedy with Bad Objective...")
    S3 = dGreedyCrappy(X,n,a,b)
    vis = visualization(dims,6,cap="Regualar Greedy")
    #vis.draw_circles_dict(X,"RED") 
    vis.draw_circles_dict(X,"BLUE")
    vis.draw_circles_dict(S2,"PURPLE")
    #vis.draw_circles_dict(S1,"BLACK")
    print("coverage Greedy      :",sim.coverage(S1))
    print("coverage dGreedy     :",sim.coverage(S2))
    print("coverage dGreedyCrap :",sim.coverage(S3))
    #print("value of lower bound :",calculateLowerBound(S2,b))
    print("ratio                :",calculateLowerBound(S2,b)/sim.coverage(S1))
    print("crap ratio           :",calculateLowerBoundCrappy(S3,a,b)/sim.coverage(S1))
    vis.update()
    vis.draw()
    vis = visualization(dims,6,cap="Distance Greedy")
    vis.update()
    vis.draw_circles_dict(X,"BLUE")
    vis.draw_circles_dict(S1,"RED")
    vis.update()

    vis.draw()
    """
    ratios = calcApproximationRatio(sim,S1,a,b)
    plt.plot(ratios)
    plt.show()
if __name__=="__main__":
    main()
