import sys
sys.path.append(sys.path[0] + "/..")
print(sys.path)
from submodular_sim import submodular_sim
import random
from visualization import visualization
import matplotlib.pyplot as plt
from math import sqrt, pi
import numpy as np
from pairwisecoverage import dist, similairty_weight
from similarity_matrix import compute_similarity_matrix
def compute_upper_lower_marginal(S,sim):
    H = 0
    G = 0
    C = 0
    S_i = []
    zero_count = 0
    avg_diff = 0
    H_margs = []
    G_margs = []
    C_G = []
    C_H = []
    C_C = []
    margs =[]
    for s in S:
       marg = sim.delta(s,S_i)
       C += marg
       C_C.append(C)
       margs.append(marg)
       H_marg= max([sim.full_info_upperbound(s,S_i),0])
       H_margs.append(H_marg)
       H +=H_marg 
       C_H.append(H)
       G_marg =max([sim.full_info_lowerbound(s,S_i),0])
       G_margs.append(G_marg)
       G += G_marg
       C_G.append(G)
       avg_diff +=(H_marg-G_marg)/len(S)
       if G_marg ==0:
           zero_count += 1
       S_i.append(s)
       
    """
    plt.figure()
    plt.plot(H_margs)
    plt.plot(G_margs)
    plt.plot(margs)
    """
    print("H/G:",H/G)
    plt.figure()
    plt.plot(C_H)
    plt.plot(C_G)
    plt.plot(C_C)
    plt.legend([r"$H(S_i)$",r"$G(S_i)$",r"$f(S_i)$"])
    plt.xlabel("i")
    plt.ylabel("Value")

def run():
    dims = (100,100)
    vis =visualization(dims,5)
    n = 30
    m = 10
    a = 400
    b =500
    print("------------Distributed Submodular Test -----------")
    print("# of agents = ",n)
    print("|X_i| = ",m)
    print("Minimum Sensor Area = ",a)
    print("Maximum Sensor Area = ",b)
    print("dimensions of area ",dims[0],"x",dims[1])
    print("ground sets are uniformly distributed over the area")
    print("---------------------Executing --------------------")
    Xn = []
    for i in range(n):
        #Xn.append([{'x':random.gauss(1,1)*10,'y':random.gauss(1,1)*10,'r':random.uniform(sqrt(a/pi),sqrt(b/pi))} for i in range(m)])
        Xn.append([{'x':random.random()*dims[0],'y':random.random()*dims[1],'r':random.uniform(sqrt(a/pi),sqrt(b/pi))} for i in range(m)])
    graph1 = [[]]
    graph2 = [[]]
    for i in range(1,n):
        graph1.append([j for j in range(i)])
    for i in range(1,n):
        graph2.append([j for j in range(i)])
        while len(graph2[i])>n-i:
            graph2[i].pop(0)
    sim = submodular_sim()
    Sg1 = sim.distributed_greedy(Xn,graph1) 
    
    Su = sim.distributed_upperbound_greedy(Xn)
    Sl = sim.distributed_lowerbound_greedy(Xn)
    compute_upper_lower_marginal(Su,sim)
    compute_upper_lower_marginal(Sl,sim)
    compute_upper_lower_marginal(Sg1,sim)
    W = compute_similarity_matrix(Xn,n,m,a,b)
    print(" 1/n||W||",(1/n)*np.linalg.norm(W,float("inf")))
    eps =  (1/(m*n))*np.linalg.norm(W,float("inf"))
    gamma = eps/(1-eps)
    weights = []
    for i in range(n):
        for j in range(i):
            d = dist(Sl[i],Sl[j])
            weights.append(similarity_weight(d,a,b))
    
    print("sum of weights:",sum(weights))
    #alpha = sum(weights)
    print("1+gamma", 1+ gamma)
    print(W)
    exit()
    plt.show()

    
    
    print("Actual Value:",sim.f(Su))
    graph1 = [[]]
    graph2 = [[]]
    for i in range(1,n):
        graph1.append([j for j in range(i)])
    for i in range(1,n):
        graph2.append([j for j in range(i)])
        while len(graph2[i])>n-i:
            graph2[i].pop(0)
    Sg1 = sim.distributed_greedy(Xn,graph1)
    print("full graph greedy:",sim.f(Sg1))

    """
    Sg2 = sim.distributed_greedy(Xn,graph2)
    Sd1 = sim.distributed_dist_greedy(Xn,a,b) 
    S_aug = sim.distributed_augmented_greedy(Xn,graph2,a,b) 
    S_uninformed = sim.distributed_uninformed_greedy(Xn)
    print("Coverage area with complete graph                       :",sim.coverage(Sg1))
    print("Coverage area with missing edges                        :",sim.coverage(Sg2))
    print("Coverage area with no edges                             :",sim.coverage(S_uninformed))
    print("Coverage area with our algorithm and no edges in graph  :",sim.coverage(Sd1))
    print("Coverage area with our algorithm and some edges in graph:",sim.coverage(S_aug)) 
    vis.draw_circles_dict(Sg1,"BLACK",width = 4)
    #vis.draw_circles_dict(S_uninformed,"BLUE")
    vis.draw_circles_dict(Sg2,"RED",width = 3)
    #vis.draw_circles_dict(Sd1,"GREEN",width= 2)
    vis.draw_circles_dict(S_aug,"PURPLE",width= 1
    """
    #vis.update()
    #vis.draw()
if __name__ =="__main__":
    run()
