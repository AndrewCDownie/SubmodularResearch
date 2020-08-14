from modules.pairwisecoverage import dist,weight
import numpy as np
from math import sqrt,pi,floor
import random
import networkx as nx
from modules.submodular_sim import submodular_sim







def compute_similarity_matrix(Xn,n,m,a,b):
    #create W
    W = np.zeros((n*m,n*m))

    #generate complete multipartite graph
    connections = [m for i in range(n)]
    G = nx.complete_multipartite_graph(*connections)
    for edge in G.edges:

        #select points to relate
        x_i = Xn[floor(edge[0]/m)][edge[0] % m]
        x_j = Xn[floor(edge[1]/m)][edge[1] % m]
        
        #compute weights
        d = dist(x_i,x_j)
        w = weight(d,a,b)
        W[edge[0],edge[1]] = w
        W[edge[1],edge[0]] = w
    return W

if __name__ == "__main__":
    n = 20
    m = 10
    a =500
    b = 500
    dims = (100,100)
    Xn = []
    for i in range(n):
        Xn.append([{'x':random.random()*dims[0],'y':random.random()*dims[1],'r':random.uniform(sqrt(a/pi),sqrt(b/pi))} for i in range(m)])
    """
    def create_similarity_matrix(Xn,n,m):
        W = np.zeros((n*m,n*m))
        for i in range(n*m):
            for j in range(n*m):
                if floor(i/m) != floor(j/m):
                    x_i = Xn[floor(i/m)][(i % m)]
                    x_j = Xn[floor(j/m)][j % m]
                    d = dist(x_i,x_j)
                    W[i,j] = weight(d,a,b)
        return W
    """
    W = compute_similarity_matrix(Xn,n,m,a,b)
    E,V = np.linalg.eig(W)
    print(E)
    print("1/n norm",(1/n)*np.linalg.norm(W,float('inf')))
    print()
    #print("norm:",np.linalg.norm(W,float('inf')))
    print('m^2',m*m)
    """
    sim = submodular_sim(dims = dims)

    S = sim.distributed_dist_greedy(Xn,a,b)
    print(S)
    
    weights = []
    for i in range(n):
        for j in range(i):
            d = dist(S[i],S[j])
            weights.append(weight(d,a,b))

    print("sum weights",sum(weights))
    print("nm^2",n*m*m)
    print("n*norm",np.linalg.norm(W,float('inf')))
    
    #connections.append([j+n*i for j in range(m)])
    #*y = [3,3,3
    """

    

