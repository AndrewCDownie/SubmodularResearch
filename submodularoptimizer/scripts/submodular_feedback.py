from visualization import visualization
import pygame
from submodular import generate_points, delta, get_CDAG, get_minimal_DAG
from submodular_functions import coverage
from shapely.geometry import box
import pprint
import matplotlib.pyplot as plt
pp = pprint.PrettyPrinter()
import random
import math

def get_X_ins(i,E,D):
    X_in = []
    for e in E:
        if i == e[1] and D[e[0]] is not None:
            X_in.append(D[e[0]])
        #elif i == e[0] and D[e[1]] is not None:
        #    X_in.append(D[e[1]])
    return X_in


def dist(x,y):
    return math.sqrt((x[0]-y[0])**2+(x[1]-y[1])**2)

def dist_delta(x,X_in,D):
    f_x = delta(x,X_in)
    discount = 0
    count = 0
    L = 5000
    for d in D:
        if d is None:
            break
        if d not in X_in:
            count +=1
            discount += L/dist(x,d)
    if count == 0:
        return f_x
    f_x = f_x - discount/count
    
    return f_x

def GreedyFeedBack(X,E,D):
    for i in range(len(X)):
        X_in = get_X_ins(i,E,D)
        argmax_x = random.choice(X[i])
        max_x = delta(argmax_x,X_in)
        for x in X[i]:
            new_delta = delta(x,X_in)
            if max_x < new_delta:
                argmax_x = x
                max_x = new_delta
        D[i] = argmax_x
    return D

def GreedyDistance(X,E,D):
    for i in range(len(X)):
        X_in = get_X_ins(i,E,D)
        argmax_x = random.choice(X[i])
        max_delta = dist_delta(argmax_x,X_in,D) 
        for x in  X[i]:
            new_delta = dist_delta(x,X_in,D)
            if max_delta < new_delta:
                max_delta = new_delta
                argmax_x = x
        D[i] = argmax_x
    return D

def reDraw(vis,D,X):
    vis.display.fill(vis.WHITE)
    #vis.draw_circles(D,10,"BLACK")

    for i in range(len(X)):
        c = (10*i,10*i, 10*i)
        vis.draw_circles([D[i]],10,"BLACK",cc=c)
        vis.draw_circles(X[i],2,"RED",cc =c)
    vis.update() 

def main():
    dim = (100,100)
    vis = visualization(dim,5)
    running = True
    n = 25
    X = [generate_points(dim,box(0,0,dim[0],dim[1]),15) for i in range(n)]
    E = [(0,1),(0,2),(1,2),(1,3),(2,1),(3,4),(4,0)]
    E = get_CDAG(n-1)
    E = get_minimal_DAG(n-1)
    D = [None for i in range(n)]
    D = GreedyDistance(X,E,D)
    D_2 = GreedyFeedBack(X,E,[None for i in range(n)])
    print(coverage(D,10),coverage(D_2,10))
    t = [0]
    v = [coverage(D,10)]
    vis.draw_circles(D,10,"BLACK")
    for x in X:
        vis.draw_circles(x,2,"RED")
    vis.update() 
    reDraw(vis,D,X)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                D = GreedyFeedBack(X,E,D)
                t.append(t[-1]+1)
                v.append(coverage(D,10))
                reDraw(vis,D,X)
                plt.plot(v)
                plt.show()
                print("redraw")
if __name__ =="__main__":
    main()
