#dist Mode
from modules.submodular_functions import coverage,dist
from modules.visualization import visualization
import pygame
import random
import math


def delta(x,S):
    S_union = list(S)
    S_union.append(x)
    return coverage(S_union,10)- coverage(S,10)

def distDelta(x,S):
    dim = (100,100)
    fxi = coverage([x],1)
    nf = 1/math.sqrt(math.pow(dim[0],2)+math.pow(dim[1],2)) 
    discount = 0
    for xk in S:
        #print(dist(x,xk)*nf)
        
        if dist(x,xk)*nf <500:
            discount += math.pow((1-dist(x,xk)*nf),4)*min([coverage([x],10),coverage([xk],10)])
            #print("found")
            pass
        else:
            print("not found")
    return fxi - discount


def docSumDelta(x,V,S):

    l = 10
    val = 0
    discount= 0
    for v in V:
        val += dist(x,v)
    
    for s in S:
        discount += dist(x,s)

    return l*discount - val       

def greedyDocSum(X,n):
    S = []
    for i in range(n):
        x = max(X,key=lambda xi:docSumDelta(xi,X,S))  
        S.append(x)
        X.remove(x) 
    return S

def greedDist(X,n):
    S = []
    for i in range(n):
        x = max(X,key=lambda xi:distDelta(xi,S))  
        S.append(x)
        X.remove(x) 
    print(S)
    return S

def greedy(X,n):
    S = []
    for i in range(n):
        x = max(X,key=lambda x: delta(x,S))
        S.append(x)
        X.remove(x)
    print(S)
    return S



def main():
    n = 15

    dim = (100,100)

    nf = 1/math.sqrt(math.pow(dim[0],2)+math.pow(dim[1],2))
    print(nf)
    X = [[dim[0]*random.random(),dim[1]*random.random()] for i in range(5*n)]
    X1 = X.copy()
    X2 = X.copy()
    X3 = X.copy()
    S = greedy(X1,n)
    print(coverage(S,10))
    S2 = greedDist(X2,n)
    S3 = greedyDocSum(X3,n)
    print("dist:",coverage(S2,10))
    print("doc sum:",coverage(S3,10))
    area_dimensions = dim
    vis = visualization(area_dimensions,9)

    vis.draw_circles(S,10,"RED")
    vis.update()

    vis.draw_circles(S2,10,"PURPLE")        
    vis.update()

    vis.draw_circles(S3,10,"BLUE")        
    vis.update()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

if __name__ == "__main__":
    main()