from math import ceil,floor, pow,sqrt,pi
import matplotlib.pyplot as plt
from modules.pairwisecoverage import area

def boundgiven(n,e):
    m = ceil(1/e)
    print("m:",m)
    k = floor((n-m)/m)
    print("k",k)
    bound = (2*e*k+1)/(e*k+k)
    print("bound:",bound)
    return bound

def smoothbound(n,e):
    m = 1/e
    k = (n-m)/m
    bound = (2*e*k+1)/(e*k+k)
    return bound

def minboundgivenn(n):
    ep = ((6*n)+sqrt(pow(-6*n,2)+4*2*pow(n,2)*(n-3)))/(4*pow(n,2))
    bound = (2*pow(ep,2)*(n-1/ep)+1)/((1+ep)*ep*(n-1/ep))
    return bound

def numberofagentsgiven(b,e):
    print("b:",b)
    k = ceil(1/(b*(1+e)-2*e))
    m = ceil(1/e)
    n = (k+1)*m
    print("n:",n)
    return n

def minN(b):
    ep =(pow(b,2)-b-2-b*sqrt(b+1)+2*sqrt(b+1))/(-pow(b,2)+4*b-4)
    n = floor((1/(b*(ep+1)-2*ep)+1))*ceil(1/ep)
    return n

def getm(a,b):
    A = {'x':0,'y':0,'r':sqrt(b/pi)}
    B = {'x':0,'y':sqrt(a/pi)+sqrt(b/pi),'r':sqrt(b/pi)}
    print(a/area(A,B))
    return ceil(a/area(A,B))



def lowestboundgivenn(n,b):
    #his assumes the interval mode
    bounds = []
    theoretic_bounds = [ ]
    ms = []
    As = []
    for i in range(1,1000):
        a = b*i/1000
        m = ceil(2*a/(b-a))
        ms.append(m)
        k = floor((n)/(m+1))
        theoretic_bounds.append(a/(a+b))
        if k ==0:
            break
        bounds.append((b+a*k)/((a+b)*k))
        As.append(a)
    return bounds,As




def plot_lower_bounds_fixed_n():
    N = [50,100,200,400,800,1600]
    b = 1
    for n in N:
        bounds,As = lowestboundgivenn(n,b)
        plt.plot(As,bounds)
    As = []
    theoretic_bounds = []
    for i in range(1,1000):
        a = i/1000
        As.append(a)
        theoretic_bounds.append(a/(a+b))
    plt.plot(As,theoretic_bounds)
    legend_list = ["N = " + str(n) for n in N]
    legend_list.append("Theoretical lower bound")
    plt.legend(legend_list)
    plt.xlabel("lower bound a of interval [a,b]")
    plt.ylabel("ratio")
    plt.show()


if __name__ == "__main__":
    plot_lower_bounds_fixed_n()
