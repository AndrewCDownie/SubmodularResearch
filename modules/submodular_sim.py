"""
The purpose of this class is to create an enviroment for easy testing of 
Submodular maximization ideas using greedy strategies
"""

import math
from shapely.geometry import Point,box
import pygame

class submodular_sim:

    def __init__(self,X,Xn = None,dims = None):
        """
        Initalized parameters for submodular functions and space elements to test
        function
        """
        self.f = None
        self.X = X
        self.Xn = Xn
        self.dims = dims

    def delta(self,x,S):
        Sx = list(S)
        Sx.append(x)
        #print(Sx)
        return self.f(Sx)-self.f(S)

    def greedy(self,n,delta_f = None):
        """
        run basic greedy strat with submodular function specified in the simulator
        n - cardinality constraint
        return set of elements selected
        """
        S = []
        X = self.X.copy()
        for i in range(n):
            if delta_f is not None:
                x = max(X,key = lambda xi:delta_f(xi,S))
            else:
                x = max(X,key = lambda xi:self.delta(xi,S))
            #print(x)
            S.append(x)
            X.remove(x)
        return S
    
    def coverage(self,S):
        #print("Coverage",S)
        polygons = []
        if len(S) == 0:
            return 0
        for p in S:
            polygons.append(Point(p["x"],p["y"]).buffer(p["r"]))
        total_area = 0
        union_poly = polygons[0]
        for poly in polygons:
            total_area += poly.area
            union_poly = union_poly.union(poly)
        union_poly.intersection(box(0,0,self.dims[0],self.dims[1]))
        return union_poly.area

    def distDelta(self,x,S):
        dim = self.dims
        fxi = self.coverage([x])
        nf = 1/math.sqrt(math.pow(dim[0],2)+math.pow(dim[1],2)) 
        discount = 0
        for xk in S:
            discount += (1-self.dist(x,xk)*nf*0.65)*max([self.coverage([x]),self.coverage([xk])])
        return fxi - discount

    def dist(self,x1,x2):
        return math.sqrt(math.pow(x1['x']-x2['x'],2)+ math.pow(x1['y']-x2['y'],2))

    def dist_(x1,x2):
        return math.sqrt(math.pow(x1['x']-x2['x'],2)+ math.pow(x1['y']-x2['y'],2))

    def docSumDelta(self,x,S):
        l = 10
        val = 0
        discount= 0
        for v in self.X:
            if v not in S:
                val += self.dist(x,v)
        for s in S:
            discount += self.dist(x,s)

        return (l*discount*self.coverage([x])  - val)  


