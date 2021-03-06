from modules.submodular_sim import submodular_sim

from modules.visualization import visualization
from shapely.geometry import Point
from math import sqrt, pi
import random
import matplotlib.pyplot as plt
from timeit import default_timer as timer
from modules.pairwisecoverage import area


def h(dist,fx,l):
    P = Point(0,0).buffer(sqrt(fx/pi))
    Pg = Point(dist,0).buffer(sqrt(l/pi))
    return P.intersection(Pg).area

def g(dist,fx,U):
    P = Point(0,0).buffer(sqrt(fx/pi))
    Ph = Point(dist,0).buffer(sqrt(U/pi))
    return P.intersection(Ph).area
def g2(dist,fx,U):
    A = {"x":0,"y":0,'r':sqrt(fx/pi)}
    B = {"x":0,"y":dist,'r':sqrt(U/pi)}
    return area(A,B)
    

def crappyg(dist,fx,a,b):
    P = Point(0,0).buffer(sqrt(fx/pi))
    d = (sqrt(fx/pi)+sqrt(a/pi))*((dist)/(sqrt(fx/pi)+sqrt(b/pi)))
    Pg = Point(d,0).buffer(sqrt((a)/pi))
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
        marg += -g2(d,fx,b)
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


def uninformed(X,n,sim):
    Xn = X.copy()
    S = []
    for i in range(n):
        xi = max(Xn,key = lambda x:sim.coverage([x]))
        S.append(xi)
        Xn.remove(xi)

    return S

def marginalH(x,S,a):
    fx = Point(0,0).buffer(x['r']).area
    if len(S) == 0:
        return fx
    xh = max(S,key = lambda xi:h(submodular_sim.dist_(x,xi),fx,a))
    return fx - h(submodular_sim.dist_(x,xh),fx,a)

def improvement(X,n,a,b,sim):
    Xn = X.copy()
    deltas = []
    S = []
    for i in range(n):
        xg = max(Xn,key = lambda x:sim.coverage([x]))
        xi = max(Xn,key = lambda x:marginal(x,S,b))
        maxMarginal = marginalH(xg,S,a)

        if maxMarginal< marginal(xi,S,b):
            xI = xi
        else:
            xI = xg 
        deltas.append(sim.delta(xI,S))
        S.append(xI)
        Xn.remove(xI)
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

    a = 200
    b = 300

    n = 70
    N = [15,20,25,30,35,40]

    dims = [75,75]
    GreedyData = []
    dGreedyData = []
    improveData = []
    uninformedData = []
    trials = 1 
    for n in N:
        greedyAvg = 0
        dGreedyAvg = 0
        improvedAvg = 0
        uninformedAvg = 0
        for i in range(trials):
            X = [{"x":random.random()*dims[0], "y":random.random()*dims[1], "r":sqrt(random.randint(a,b)/pi)} for i in range(50)]
            sim = submodular_sim(X,dims = dims)
            print("Running Greedy...",n)
            Sg = sim.fast_coverage_greedy(X,n)
            print("Running dist Greedy...",n)
            Sdist = dGreedy(X,n,a,b)
            print("Running improvement...",n)
            Sunidist = improvement(X,n,a,b,sim)
            print("Running Uninformed...",n)
            Suniformed = uninformed(X,n,sim)
            GreedyValue = sim.coverage(Sg)
            dGreedyValue = sim.coverage(Sdist)
            improveGreedyValue = sim.coverage(Sunidist)
            uninformedValue = sim.coverage(Suniformed)

            print("Greedy value    : ",GreedyValue)
            print("dGreedy value   : ",dGreedyValue)
            print("impove Value    : ",improveGreedyValue)
            print("uninformed Value: ",uninformedValue)

            greedyAvg +=GreedyValue
            dGreedyAvg +=dGreedyValue
            improvedAvg += improveGreedyValue
            uninformedAvg += uninformedValue
        GreedyData.append(greedyAvg/trials)
        dGreedyData.append(dGreedyAvg/trials)
        improveData.append(improvedAvg/trials)
        uninformedData.append(uninformedAvg/trials)
    plt.plot(N,GreedyData)
    plt.plot(N,dGreedyData)
    plt.plot(N,improveData)
    plt.plot(N,uninformedData)
    plt.legend(['Greedy','Lower Bound','Improved Over Uninformed',"Uninformed"])
    plt.show()
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

if __name__=="__main__":
    main()
