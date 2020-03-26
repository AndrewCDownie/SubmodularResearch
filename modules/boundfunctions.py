from math import sqrt,pi
from shapely.geometry import Point
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


