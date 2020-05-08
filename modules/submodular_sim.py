"""
The purpose of this class is to create an enviroment for easy testing of 
Submodular maximization ideas using greedy strategies
"""

import math
from shapely.geometry import Point,box
from modules.boundfunctions import garea

class submodular_sim:

    def __init__(self,X = None,Xn = None,dims = None,f = None):
        self.f = None
        """
        Initalized parameters for submodular functions and space elements to test
        function
        """
        if f is not None and callable(f):
            self.f = f
        else:
            self.f = self.coverage
        self.X = X
        self.Xn = Xn
        self.dims = dims

    def delta(self,x,S):
        Sx = list(S)
        Sx.append(x)
        #print(Sx)
        return self.f(Sx)-self.f(S)

    def fast_delta(self,x,S,last_val):
        return self.f(S,x) - last_val
    

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
    
    def fast_coverage_greedy(self,X,n):
        S = []
        X = X.copy()
        last_val = 0
        for i in range(n):
            x = max(X,key = lambda xi:self.fast_delta(xi,S,last_val))
            S.append(x)
            last_val = self.coverage(S)
            X.remove(x)
        return S
     
    def distributed_greedy(self,Xn,graph):
        #find Xin
        #retrieve selected element
        S = [] 
        for i,Xi in enumerate(Xn):
            Xin = [S[j] for j in graph[i]]
            S.append(self.agent_greedy(Xi,Xin))
        return S
    
    def agent_greedy(self,Xi,S):
        S_value = self.f(S) 
        x_max = max(Xi,key = lambda xi:self.fast_delta(xi,S,S_value) )
        return x_max
    
    def distributed_dist_greedy(self,Xn,a,b):
        S = []
        for Xi in Xn:
            S.append(self.agent_dist_greedy(Xi,S,a,b))
        return S
    
    def agent_dist_greedy(self,Xi,S,a,b):
        xg = max(Xi,key = lambda x:self.f([x]))
        xI = max(Xi,key = lambda x:self.lowerbound(x,S,b))
        if self.upperbound(xg,S,a) <self.lowerbound(xI,S,b):
            return xI
        else:
            return xg

    def lowerbound(self,x,S,b):
        fx = self.f([x])
        marg = fx
        for s in S:
            d = self.dist(x,s)
            marg += - garea(d,fx,b)
        return max([marg,0])

    def upperbound(self,x,S,a):
        fx = self.f([x])
        marg = fx
        if len(S) == 0:
            return marg
        xi = max(S,key=lambda xi:garea(self.dist(x,xi),fx,a))
        return max([fx - garea(self.dist(x,xi),fx,a),0])


    def coverage(self,S,x = None):

        #print("Coverage",S)
        polygons = []
        if len(S) == 0:
            return 0
        for p in S:
            polygons.append(Point(p["x"],p["y"]).buffer(p["r"]))
        
        if x is not None:
            polygons.append(Point(x["x"],x["y"]).buffer(x["r"]))

        total_area = 0
        union_poly = polygons[0]
        for poly in polygons:
            total_area += poly.area
            union_poly = union_poly.union(poly)
        #union_poly.intersection(box(0,0,self.dims[0],self.dims[1]))
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


