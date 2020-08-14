#this is a file that will be used to test ideas for submodular maximization.
from visualization import visualization
import pygame
from submodular_functions import coverage
from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.geometry import LinearRing
from shapely.geometry import box
import random
import time 




"""
To do create class structure to organize data
implement a memo coverage function to allow for better cost computation
"""


def get_X_in(node, edges):
    X_in =[]
    for edge in edges:
        if node == edge[1]:
            X_in.append(edge[0])
    return X_in


def generate_points(area_dim,boundry,n):
    #random.seed(10)
    points = []
    p = (0,0)
    for i in range(n):
        contained = False
        while not contained:
            p = (random.randint(0,area_dim[0]),random.randint(0,area_dim[1]))
            #print(p)
            contained = boundry.intersects(Point(p[0],p[1]))
        points.append(p)
    return points


def delta(x,S):
    S_union = list(S)
    #S_union =[]

    S_union.append(x)
    return coverage(S_union,10)- coverage(S,10)

def Greedy_Select_Points(X,S,n):
    """
    X is the domain of points that can be selected
    n is the number of agents selecting
    """
    X = list(X)
    for i in range(n):
        argmax_x = X[0]
        for x in X:
            if delta(argmax_x,S) < delta(x,S):
                argmax_x = x
        S.append(argmax_x)
        X.remove(argmax_x)
    return S

def distributed_select(X):
    S = []
    for i in range(len(X)):
        argmax_x_i = X[i][0]
        for x in X[i]:
            if delta(argmax_x_i,S) < delta(x,S):
                argmax_x_i = x
        S.append(argmax_x_i)
    return S



def limited_information_greedy(X,E):
    #previous Decisions
    decisions = [None for i in range(len(X))]
    # make Decisions
    for i in range(len(X)):
        #get list of selections that X_i can see
        X_in = get_X_in(i,E)
        S = [decisions[i] for i in X_in]
        argmax_x_i = X[i][0]
        for x in X[i]:
            if delta(argmax_x_i,S)< delta(x,S):
                argmax_x_i = x
        decisions[i] = argmax_x_i
    
    return decisions


def limited_information_greedy_with_replacement(X,E):
    #previous Decisions
    decisions = [None for i in range(len(X))]
    total_X = []
    for x_i in X:
        total_X.extend(x_i)
    # make Decisions
    for i in range(len(X)):
        #get list of selections that X_i can see
        X_in = get_X_in(i,E)
        S = [decisions[i] for i in X_in]
        argmax_x_i = X[i][0]
        #replace missing X's With globally found
        replace_number = i - len(X_in)
        S = Greedy_Select_Points(total_X,S,replace_number)
        for x in X[i]:
            if delta(argmax_x_i,S)< delta(x,S):
                argmax_x_i = x
        decisions[i] = argmax_x_i
    
    return decisions


def get_CDAG(n):
    E = []
    for i in range(n):
        for j in range(i+1,n+1):
            E.append((i,j))
    return E

def get_minimal_DAG(n):
    E = []
    for i in range(1,n):
        E.append((i-1,i))
    return E

def get_clique(n,m):
    E = []
    for i in range(n,m):
        for j in range(i+1,m+1):
            E.append((i,j))
    return E

def get_overalap_points(dim,n,density):
    X = []
    for i in range(n):
        X_i =generate_points(dim,box(0,0,dim[0],dim[1]),density)
        X.append(X_i)
    return X

def sim():
    area_dimensions = (50,50)
    trial_nums = 20
    avgs =[]
    for n in range(3,6):
        E1 = get_CDAG(n)
        E2 = get_minumal_DAG(n)
        print(E1,E2)
        avg = [0,0]
        for i in range(trial_nums):
            X = get_overalap_points(area_dimensions,n,5)
            S1 = limited_information_greedy(X,E1)
            S2 = limited_information_greedy(X,E2)
            S3 = limited_information_greedy_with_replacement(X,E1)
            S4 = limited_information_greedy_with_replacement(X,E2)
            avg[0] += (coverage(S2,10)/coverage(S1,10))/trial_nums
            avg[1] += (coverage(S4,10)/coverage(S1,10))/trial_nums

        avgs.append(avg)
        print("No Replacement Avg: {0}, with Replacement Avg: {1}".format(avg[0],avg[1]))

def main():
    print("main")
    area_dimensions = (50,50)
    vis = visualization(area_dimensions,5)
    running = True
    #points = generate_points(area_dimensions,box(0,0,area_dimensions[0],area_dimensions[1]),20)
    #points = generate_points(area_dimensions,box(0,0,100,100),20)
    #coverage(points,10)
    #vis.draw_cirles(points,25,"BLACK")
    #picked = Greedy_Select_Points(points,5)
    n =3
    
    total_X = []

    E1 = [
        (0,1),
        (0,2),
        (0,3),
        (1,2),
        (1,3),
        (2,3)
    ]

    E1 = []
    for i in range(16):
        for j in range(i+1,16+1):
            E1.append((i,j))
    #print(E1)
    #exit()
    E2 = []
    for i in range(1,16):
        E2.append((i-1,i))
    print(E2)
    print(E1)
    #exit()
    """
    exit()
    E2 = [
        (0,1),
        (1,2),
        (2,3),
        (3,4),
        (4,5),
        (5,6),
        (6,7),
        (7,8),
        (8,9)
    """
    avgNoReplace =0
    avgReplace =0
    for i in range(100):
        X = []
        for i in range(n):
            for j in range(n):
                #X_i =generate_points(area_dimensions,box(i*(area_dimensions[0]/n),j*(area_dimensions[1]/n),(i+1)*(area_dimensions[0]/n),(j+1)*(area_dimensions[1]/n)),5)
                X_i =generate_points(area_dimensions,box(0,0,area_dimensions[0],area_dimensions[1]),10)
                X.append(X_i)
                total_X.extend(X_i)
        """
        for x in X:
            vis.draw_cirles(x,1,"BLACK")
        """
        vis.update()
        
        S1 = limited_information_greedy(X,E1)
        S2 = limited_information_greedy(X,E2)

        #S3 = limited_information_greedy_with_replacement(X,E1)
        S4 = limited_information_greedy_with_replacement(X,E2)
        avgNoReplace += (coverage(S2,10)/coverage(S1,10))/100
        avgReplace += (coverage(S4,10)/coverage(S1,10))/100
    results = "no replace average {0}, replace average{1}".format(avgNoReplace,avgReplace)
    print(results)

    """
    results ="No Replacement for E1 Coverage = {0}, for E2 Coverage = {1}"
    results2 = "Replacemment for E1 Coverage = {0}, for E2 Coverage = {1}"
    results = results.format(coverage(S1,10),coverage(S2,10))
    results2 = results2.format(coverage(S3,10),coverage(S4,10))
    """

    vis.draw_cirles(S1,10,"GREEN")
    vis.update()
    vis.draw_cirles(S2,9,"BLUE")
    vis.update()

    vis.draw_cirles(S3,8,"RED")
    vis.update()

    vis.draw_cirles(S4,7,"PURPLE")        
    vis.update()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False



def coverage_plot():
    import matplotlib.pyplot as plt
    x = [0,0]
    values = []
    d = []
    for i in range(0,200):
        x1 = [i/10,0]
        values.append(coverage([x],10)-(coverage([x,x1],10)-coverage([x],10)))
        d.append(i/10)
    plt.plot(d,values)
    plt.show()


if __name__ =="__main__":
    #main()
    #sim()
    #print(get_clique(2,4))
    coverage_plot()
