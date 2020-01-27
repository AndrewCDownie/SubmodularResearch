#triangulation functions
import math

def triangulation(p1,p2,p3,r1,r2,r3):
    #simplify the coordinates
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]
    x3 = p3[0]
    y3 = p3[1]

    #caluclate  y and x assuming solution exists
    y = ((x2-x3)*((math.pow(x2, 2)-math.pow(x1, 2))+(math.pow(y2, 2)-math.pow(y1, 2))+(math.pow(r1,2)-math.pow(r2,2))) -(x1-x2)*((math.pow(x3,2)-math.pow(x2,2))+(math.pow(y3,2)-math.pow(y2,2))+(math.pow(r2,2)-math.pow(r3,2))))/(2*((y1-y2)*(x2-x3)-(y2-y3)*(x1-x2)))
    x = ((y2-y3)*((math.pow(y2, 2)-math.pow(y1, 2))+(math.pow(x2, 2)-math.pow(x1, 2))+(math.pow(r1,2)-math.pow(r2,2))) -(y1-y2)*((math.pow(y3,2)-math.pow(y2,2))+(math.pow(x3,2)-math.pow(x2,2))+(math.pow(r2,2)-math.pow(r3,2))))/(2*((x1-x2)*(y2-y3)-(x2-x3)*(y1-y2)))
    return (-x,-y)


def main():
    print(triangulation((3,8),(3,1),(2,-1),3,math.sqrt(58),math.sqrt(4+81)))

if __name__ == "__main__":
    main()