from shapely.geometry import Point
import sys,os
from modules.visualization import visualization
from math import sin, cos,pi,sqrt,ceil,floor

from modules.submodular_sim import submodular_sim
import matplotlib.pyplot as plt
from modules.boundfunctions import garea

def get_circles(n,rc,rout,center):
    theta_diff = 2*pi/n
    circles = [{'x':center[0],'y':center[1],'r':rc}]
    for i in range(1,n+1):
        x = center[0] + (rc+rout)*cos(theta_diff*i)
        y = center[1] + (rc+rout)*sin(theta_diff*i)

        circles.append({'x':x,'y':y,'r':rout})
    return circles

def run():
    dims = (1000,1000)
    scale = 1
    n = 100
    vis = visualization(dims,scale,cap="circle diagram")
    sim = submodular_sim([],dims = dims)
    cirs = get_circles(6,sqrt(1000/pi),sqrt(10000/pi),(500,500)) 
    P = list(range(1,7))
    data  = []
    bounds = []
    for p in P:
        data.append([])
        bounds.append([])
        b =1 
        As = [b*i/100 for i in range(1,100)] 
        for a in As:
            Cs = get_circles(p,sqrt(b/pi),sqrt(a/pi),(15,15))
            cov = sim.coverage(Cs)
            data[-1].append(cov)
            m = a/garea(sqrt(b/pi)+sqrt(a/pi),b,b)
            k = floor(n/(m+p))
             
            if k == 0:
                bounds[-1].append(0)
            else:
                bounds[-1].append((b+a*k)/(k*(cov)))
    for d in data:
        plt.plot(As,d)
    legend_text = ["p = "+str(p) for p in P]
    plt.legend(legend_text)
    plt.show()
    for bound in bounds:
        plt.plot(As,bound)
    plt.legend(legend_text)
    plt.show()
    print("coverage:",sim.coverage(cirs)) 
    vis.draw_circles_dict(cirs[1:],"BLUE")
    vis.draw_circles_dict(cirs[0:1],"RED")
    vis.update()

    vis.draw()
if __name__ == "__main__":
    run()
