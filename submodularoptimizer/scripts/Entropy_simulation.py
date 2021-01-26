import sys
sys.path.append("..")
import math
#mport matplotlib.pyplot as plt
import numpy as np
import itertools as it
from linetimer import CodeTimer

class EntropyProblem:
    def __init__(self,points,gamma):
        self.points = points
        (self.n , self.d) = self.points.shape
        self.gamma = gamma 
        self.scale_factor = 1
        self.X = self.generate_X(self.points)
        (evals,_) = np.linalg.eig(self.X)
        min_val = min(evals)
        if min_val<1:
            self.scale_factor = 1/(0.1*min_val)
            print('Rescalling')
            self.X = self.scale_factor*self.X
            eig = np.linalg.eigvals(self.X)
            print(min(eig))
        


    def min_dist(self):
        dists = [np.linalg.norm(self.points[i,:]-self.points[j,:]) for (i,j) in it.combinations(range(self.n),2)]
        return min(dists)

    def generate_X(self,points):
        (n,_) = points.shape
        X = np.zeros((n,n))
        for i,j in it.product(range(n),range(n)):
            X[i,j] = np.exp(-self.gamma*np.power(np.linalg.norm(points[i,:]-points[j,:]),2))
        return X

    def sub_matrix(self,S):
        return self.X[np.ix_(S,S)]
        """
        X_sub = np.zeros((len(S),len(S)))
        for i,s_1 in enumerate(S):
            for j,s_2 in enumerate(S):
                X_sub[i,j] = self.X[s_1,s_2]
        """
        return X_sub 
        
    def objective(self,S):
        X_sub = self.sub_matrix(sorted(S))
        return np.log(np.linalg.det(X_sub))

    def marginal(self,X,S):
        #print(X)
        #print(S)
        if type(X) ==type(set()):
            #print("Set Version")
            #print(self.objective(S.union(X)),self.objective(S))
            return self.objective(S.union(X))- self.objective(S)
        #print(self.objective(S.union({X})),self.objective(S))
        return self.objective(S.union({X}))- self.objective(S)

    def pairwise_upperbound(self,x,S):
        if len(S)==0:
            return self.objective({x})
        max_s = min(S,key = lambda s:self.marginal({x},{s}))
        return self.marginal({x},{max_s})
        
    def greedy(self,X,n):
        S = set()
        X = X.copy()
        for _ in range(n):
            x_i = max(X,key = lambda x:self.marginal(x,S))
            S.add(x_i)
            X.remove(x_i)
        return S

    def upper_bound_greedy(self,X,n):
        S = set()
        X = X.copy()
        for _ in range(n):
            x_i = max(X,key = lambda x:self.pairwise_upperbound(x,S))
            S.add(x_i)
            X.remove(x_i)
        return S


        


if __name__ == "__main__":
    d = 4
    n = 300
    k = 200
    Points = np.random.rand(n,d)*3
    print (Points)
    EP = EntropyProblem(Points,0.1)
    X = list(range(n))
    with CodeTimer():
        S = EP.greedy(X,k)
    print("greedy Set",S)
    print("greedy Value",EP.objective(S))
    with CodeTimer():
        S_u = EP.upper_bound_greedy(X,k)
    print("upper bound set Set",S_u)
    print("greedy Value",EP.objective(S_u))
    """
    with CodeTimer():
        OPT_set = max(it.combinations(X,k),key = lambda s:EP.objective(set(s)))
    print("OPT set",OPT_set)
    print("OPT set value",EP.objective(OPT_set))
    """
    #for i in range(1,n):
    #    print(EP.marginal(i,{0}))