#from modules.submodular_sim import submodular_sim
import matplotlib.pyplot as plt
from shapely.geometry import Point
from math import sqrt, pi, pow
r1 = 3

def g3(dist):
    r2 = 1
    p1area = Point(0,0).buffer(r1).area
    p2area = Point(0,0).buffer(r2).area  

    slope = 0.5
    return min([p2area,max([(1-(dist-(r1-r2)*1.1)*slope)*p2area,0])])


def g2(dist):
    return max([(1-dist*0.5),0])

def h2(dist):
    return max([1-dist,0])


def h3(dist):
    r2 = 1
    p1area = Point(0,0).buffer(r1).area
    p2area = Point(0,0).buffer(r2).area  

    slope = 0.65
    return min([p2area,max([(1-(dist-(r1-r2))*slope)*p2area,0])])

def g(dist,fx,l):
    P = Point(0,0).buffer(sqrt(fx/pi))
    Pg = Point(dist,0).buffer(sqrt(l/pi))
    return P.intersection(Pg).area


def h(dist,fx,U):
    P = Point(0,0).buffer(sqrt(fx/pi))
    Ph = Point(dist,0).buffer(sqrt(U/pi))
    return P.intersection(Ph).area


def crappyg(dist,fx,a,b):
    P = Point(0,0).buffer(sqrt(fx/pi))
    d = (sqrt(fx/pi)+sqrt(a/pi))*(dist/(sqrt(fx/pi)+sqrt(b/pi)))
    Pg = Point(d,0).buffer(sqrt(a/pi))
    return (fx/a)*P.intersection(Pg).area





def testIntervalRange():
    #the interval is [a, b]

    a = 350
    b = 400

    xarea = (a+b)/2

    ra = sqrt(a/pi)
    rb = sqrt(b/pi)
    rx = sqrt(xarea/pi)
    #data collection
    delta = 0.1
    tmax = int((rx+rb+2)/delta)
    
    dist = [i*delta for i in range(tmax)]
    L = [0 for i in range(tmax)]
    S = [0 for i in range(tmax)]
    M = [0 for i in range(tmax)]
    E = [0 for i in range(tmax)]
    E2 = [0 for i in range(tmax)]
    E3 = [0 for i in range(tmax)]

    for i in range(tmax):
        P = Point(0,0).buffer(rx)
        PMi = Point(dist[i],0).buffer(rx)
        PUp = Point(dist[i],0).buffer(rb)
        PLo = Point(dist[i],0).buffer(ra)
        """
        L[i] = P.area - P.intersection(PUp).area
        S[i] = P.area - P.intersection(PLo).area
        M[i] = P.area - P.intersection(PMi).area
        """
        L[i] =  P.intersection(PUp).area
        S[i] = P.intersection(PLo).area
        M[i] = P.intersection(PMi).area
        E[i] =(3/5)*P.intersection(PUp).area
        E2[i] =3*P.intersection(PLo).area
        E3[i] = crappyg(dist[i],P.area,a,b)        

    plt.plot(dist,L)
    plt.plot(dist,S)
    plt.plot(dist,M)
    plt.plot(dist,E3)
    
    plt.xlabel(r"$d(x_i,x_j)$")
    plt.ylabel(r"$f(x_1) - f(x_1|x_2)$")
    plt.legend([r'$f(x_2) = b$',r'$f(x_2) = a$',r'$f(x_2) = f(x_1)$',r"Experimentally found $g$"])
    plt.title(r"$f(x_1) - f(x_1|x_2)$ VS Distance")
    plt.show()

def testLipshitz():
    #sim = submodular_sim(None,dims=(100,100))
    
    delta = 0.1
    r1 = 1
    r2 = 4

    tmax = 50
    dist = [i*delta for i in range(tmax)]
    data = [0 for i in range(tmax)]
    datalipshitzmax = [[0 for i in range(tmax)] for i in range(10)]
    datalipshitzmin = [[0 for i in range(tmax)] for i in range(10)]
    lower = [0 for i in range(tmax)]
    radii = lower = [0 for i in range(tmax)]
    for i in range(tmax):
        P1 = Point(0,0).buffer(r1)
        

        P2 = Point(dist[i],0).buffer(r1)
        
        data[i] = P1.area - P1.intersection(P2).area
        for j in range(2):
            rmax = sqrt(j*(dist[i])/pi + pow(r1,2)) -r1
            rmin = sqrt(max([-j*(dist[i])/pi + pow(r1,2),0])) -r1
            P3 = Point(dist[i],0).buffer(r1+rmax)
            P4 = Point(dist[i],0).buffer(r1+rmin)

            datalipshitzmax[j][i] = P1.area - P1.intersection(P3).area
            datalipshitzmin[j][i] = P1.area - P1.intersection(P4).area

        #lower[i] = P1.area - g2(dist[i])*P1.area
    
    #lower = [ g(delta*i) for i in reversed(range(100))]
    # upper = [h(delta*i) for i in reversed(range(100))]
    plt.plot(dist,data)
    #plt.plot(dist,lower)
    for i in range(10):
        plt.plot(dist,datalipshitzmax[i])
        plt.plot(dist,datalipshitzmin[i])

    plt.legend(['actual',"lipshitz"])
    plt.xlabel(r"$d(x_i,x_j)$")
    plt.show()


def main():
    testIntervalRange()

if __name__ == "__main__":
    main()