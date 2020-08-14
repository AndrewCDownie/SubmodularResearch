from modules.submodular_sim import submodular_sim

from modules.visualization import visualization
from shapely.geometry import Point
from math import sqrt, pi
import random
import matplotlib.pyplot as plt


from modules.boundfunctions import g,h
random.seed(100)

def marginalG(x,S,b):
    fx = Point(0,0).buffer(x['r']).area
    marg = fx
    for s in S:
        d = submodular_sim.dist_(x,s)
        marg += -g(d,fx,b)
    return max([marg,0])


def marginalH(x,S,a):
    fx = Point(0,0).buffer(x['r']).area
    if len(S) == 0:
        return fx
    xh = max(S,key = lambda xi:h(submodular_sim.dist_(x,xi),fx,a))
    return fx - h(submodular_sim.dist_(x,xh),fx,a)

def uninformed(X,n,sim):
    Xn = X.copy()
    deltas = []
    S = []
    for i in range(n):
        xi = max(Xn,key = lambda x:sim.coverage([x]))
        deltas.append(sim.delta(xi,S))
        S.append(xi)
        Xn.remove(xi)

    return S,deltas


def improvement(X,n,a,b,sim):
    Xn = X.copy()
    deltas = []
    S = []
    for i in range(n):
        xg = max(Xn,key = lambda x:sim.coverage([x]))
        xi = max(Xn,key = lambda x:marginalG(x,S,b))
        maxMarginal = marginalH(xg,S,a)

        if maxMarginal< marginalG(xi,S,b):
            xI = xi
        else:
            xI = xg 
        deltas.append(sim.delta(xI,S))
        S.append(xI)
        Xn.remove(xI)
    return S,deltas 

def get_ordered_marginals(X,sim):
    Xn = X.copy()
    S = []
    deltas = []
    for i in range(len(Xn)):
        xi = max(Xn,key=lambda x:sim.delta(x,S))
        deltas.append(sim.delta(xi,S))
        S.append(xi)
        Xn.remove(xi)
    return deltas,S


def main():

    a = 500
    b = 500

    n = 25
    dims = [100,100]
    X = [{"x":random.random()*dims[0], "y":random.random()*dims[1], "r":sqrt(random.randint(a,b)/pi)} for i in range(100)]
    sim = submodular_sim(X,dims = dims)
    sim.f = sim.coverage

    vis = visualization(dims,6,cap="uninformed vs informed")   
    Sg,dg = uninformed(X,n,sim)
    print("uninformed value:",sim.coverage(Sg))

    Si,di = improvement(X,n,a,b,sim)
    print("informed value:",sim.coverage(Si))
    
    vis.draw_circles_dict(X,"BLUE")
    vis.draw_circles_dict(Si,"GREEN")
    vis.draw_circles_dict(Sg,"RED")
    
    vis.update()

    #plot particular relivant figures 

    #plot marginals as selected
    plt.figure()
    plt.plot(list(range(n)),dg)
    plt.plot(list(range(n)),di)
    plt.legend(['dg','di'])

    cumg = []
    cumi = []
    sumg = 0
    sumi = 0
    for i in range(n):
        sumg +=dg[i]
        cumg.append(sumg)
        sumi +=di[i]
        cumi.append(sumi)
    #plot the cummulative
    plt.figure()
    plt.plot(list(range(n)),cumg)
    plt.plot(list(range(n)),cumi)
    plt.legend([r"$S_i^g$",r"$S_i^I$"])


    """

    #vis.draw()
    sumg = 0
    sumi = 0
    cumg = []
    cumi = []
    disort = sorted(di,reverse=True)
    dgsort = sorted(dg,reverse=True)
    for i in range(n):
        sumg +=dgsort[i]
        cumg.append(sumg)
        sumi +=disort[i]
        cumi.append(sumi)
    
    
    plt.figure()
    plt.plot(list(range(n)),cumg)
    plt.plot(list(range(n)),cumi)
    plt.legend(["cumg",'cumi'])

   


    #ordered elements
    ordered_deltas_g,ordered_sg = get_ordered_marginals(Sg,sim)
    ordered_deltas_i, ordered_si = get_ordered_marginals(Si,sim)

    plt.figure()
    plt.plot(list(range(len(ordered_deltas_g))),ordered_deltas_g)
    plt.plot(list(range(len(ordered_deltas_i))),ordered_deltas_i)
    plt.legend(['g','i'])

    cumg = []
    cumi = []
    sumg = 0
    sumi = 0
    for i in range(n):
        sumg +=ordered_deltas_g[i]
        cumg.append(sumg)
        sumi +=ordered_deltas_i[i]
        cumi.append(sumi)
    plt.figure()
    plt.plot(list(range(len(cumg))),cumg)
    plt.plot(list(range(len(cumi))),cumi)
    plt.legend(['g','i'])

    """
    plt.show()


if __name__ == "__main__":
    main()