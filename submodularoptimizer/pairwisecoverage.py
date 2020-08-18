from math import sqrt, pow,asin,acos,pi


def similarity_weight(d,a,b):
    A = {"x":d,"y":0,"r":sqrt(a/pi)}
    B = {"x":0,"y":0,"r":sqrt(b/pi)}
    return area(A,B)/a

def dist(a,b):
    return sqrt(pow(a['x']-b['x'],2)+ pow(a['y']-b['y'],2))

def area(A,B):
    d = sqrt(pow(B['x']-A['x'],2) +pow(B['y']-A['y'],2))
    if d < A['r'] +B['r']:
        a = pow(A['r'],2)
        b = pow(B['r'],2)
        if d<=abs(B['r']-A['r']):
            return pi*min(a,b)
        x = (a-b+d*d)/(2*d)
        z = x*x
        y = sqrt(a-z)
        return a*asin(y/A['r']) + b*asin(y/B['r'])-y*(x+sqrt(z+b-a))
    else:
        return 0


if __name__ == "__main__":
    print("area",area({'x':0,'y':sqrt(2/pi)+sqrt(1/pi),'r':sqrt(2/pi)},{'x':0,'y':0,'r':sqrt(1/pi)}))
