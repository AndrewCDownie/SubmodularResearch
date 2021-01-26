import sys
sys.path.append("..")
import math
import matplotlib.pyplot as plt
from submodular_sim import submodular_sim
import random
import pprint
from itertools import combinations_with_replacement,permutations,product,islice
import itertools
import numpy as np

sim = submodular_sim()

def unique_element_sequence():
    i = 1
    while True:
        yield "e"+str(i)
        i +=1
    
def get_n_new_elements(sequence,l):
    return list(islice(sequence,l))
    

def generate_worst_case_pessimistic(n,m):
    sequence = unique_element_sequence()

    #make central set
    S_c = set(get_n_new_elements(sequence,m))

    #make arm sets
    S_sets = [list(get_n_new_elements(sequence,m)) for i in range(n)]
    
    #make small sets
    S_epsilon_sets = [list(get_n_new_elements(sequence,1)) for i in range(n)]

    X = [set(s_ep) for s_ep in S_epsilon_sets]
    OPT = []
    for S in S_sets:
        s  = S_c|set(S)
        X.append(s)
        OPT.append(s)
    return X,OPT

def generate_worst_case_optimistic(n,m):
    sequence = unique_element_sequence()
    S_i =[list(get_n_new_elements(sequence,math.floor(m)))]
    X = []
    while len(S_i[0])>1:
        #make halfs
        S_iplus1_0 = [s[:len(s)//2] for s in S_i]
        S_iplus1_1 = [s[len(s)//2:] for s in S_i]
        #make and add x_i0 and x_i1
        x0 = []
        x1 = []
        for i in range(len(S_iplus1_0)):
            x0 += S_iplus1_0[i]
            x1 += S_iplus1_1[i]
        X.append(set(x0))
        X.append(set(x1))
        #combine sets
        S_i = S_iplus1_0 + S_iplus1_1

    #make Optimal Choices
    print(len(X))
    
    S_epsilon_sets = [set(list(get_n_new_elements(sequence,math.floor(m//4)-3))) for i in range(n-2)]
    OPT = [X[0], X[1]] + S_epsilon_sets
    print("OPT",set_coverage(OPT))
    print("SETS")
    print("Set",len(S_epsilon_sets))
    print("len epsilon set",len(S_epsilon_sets[0]))
    print("len first element",len(X[0]))
    X += S_epsilon_sets
    print("Marginal marginal",set_coverage(X[:4],X[-1])- set_coverage(X[:4]))
    print("Marginal upperbound marginal",sim.pairwise_upperbound_set(X[-1],X[:4]))
    print("Marginal upperbound marginal",sim.pairwise_upperbound_set(X[10],X[:9]))
    return X,OPT


def generate_worst_case_combined(n,m):
    sequence = unique_element_sequence()
    S_i =[list(get_n_new_elements(sequence,math.floor(m)))]
    X = []

    #make the poor elements for optimistic choice
    while len(S_i[0])>1:
        #make halfs
        S_iplus1_0 = [s[:len(s)//2] for s in S_i]
        S_iplus1_1 = [s[len(s)//2:] for s in S_i]
        #make and add x_i0 and x_i1
        x0 = []
        x1 = []
        for i in range(len(S_iplus1_0)):
            x0 += S_iplus1_0[i]
            x1 += S_iplus1_1[i]
        X.append(set(x0))
        X.append(set(x1))
        #combine sets
        S_i = S_iplus1_0 + S_iplus1_1
    print(len(X))
    print(set_coverage(X))
    #make central set
    S_c = set(get_n_new_elements(sequence,m//4))

    #make arm sets
    S_sets = [list(get_n_new_elements(sequence,m//4-2)) for i in range(n)]
    
    #make small sets
    S_epsilon_sets = [list(get_n_new_elements(sequence,1)) for i in range(n)]

    X += [set(s_ep) for s_ep in S_epsilon_sets]
    print(len(X[-1]))
    OPT = [X[0],X[1]]
    for S in S_sets:
        s  = S_c|set(S)
        X.append(s)
        OPT.append(s)
    print(len(X[0]))
    print(len(X[-1]))
    #Too many elements, need only n-2 of them
    OPT.pop(-1)
    OPT.pop(-1)
    print(len(OPT))
    return X,OPT

def combine_sets(sets):
    combined = set()
    for s in sets:
        combined |= s
    return combined

def random_case(l,m,k):
    sequence = unique_element_sequence()
    M_sets = [set(get_n_new_elements(sequence,1)) for _ in range(m)]
    print("random choice",random.choices(M_sets,k = k))
    X = [combine_sets(random.choices(M_sets,k = 5)) for _ in range(l)]
    print(M_sets)
    print(X)
    return X


def set_coverage(S,x = None):
    union_set = set()
    for s in S:
        union_set |= s
    if x is not None:
        union_set |= x
    return len(union_set)

def greedy_pairwise(X,n,LB = True):
    S = []
    S_g = []
    X_i = X.copy()
    for i in range(n):
        print("computing",i)
        #compute Reference:
        x_g = max(X_i,key = lambda x:(set_coverage(S,x)-set_coverage(S)))
        S_g.append(x_g)   
        if LB: 
            x_i = max(X_i,key = lambda x: sim.pairwise_lowerbound_set(x,S))
        else:
            x_i = max(X_i,key = lambda x: sim.pairwise_upperbound_set(x,S))
        S.append(x_i)
        X_i.remove(x_i)
    return S, S_g

def pairwise_sum(X,n):
    S = []
    S_g = []
    X_i = X.copy()
    for i in range(n):
        print("computing",i)
        #compute Reference:
        x_g = max(X_i,key = lambda x:(set_coverage(S,x)-set_coverage(S)))
        S_g.append(x_g)   
        x_i = max(X_i,key = lambda x: sim.pairwise_lowerbound_set(x,S)+ sim.pairwise_upperbound_set(x,S))
        
        S.append(x_i)
        X_i.remove(x_i)
    return S,S_g

def greedy_pairwise_alt(X,n):
    S = []
    S_g = []
    X_i = X.copy()
    for i in range(n):
        print("computing",i)
        #compute Reference:
        x_g = max(X_i,key = lambda x:(set_coverage(S,x)-set_coverage(S)))
        S_g.append(x_g)   
        if i%2 == 0: 
            x_i = max(X_i,key = lambda x: sim.pairwise_lowerbound_set(x,S))
        else:
            x_i = max(X_i,key = lambda x: sim.pairwise_upperbound_set(x,S))
        S.append(x_i)
        X_i.remove(x_i)
    return S, S_g


def probabalistic_choice(X,n):
    S = []
    S_g = []
    X_i = X.copy()
    for i in range(n):
        print("probablistically chosing",i)
        #generate Probabilites
        pmf = [sim.pairwise_lowerbound_set(x, S) + sim.pairwise_upperbound_set(x,S) for x in X_i]
        normalization = sum(pmf)
        pmf = [p/normalization  for p in pmf]
        #print(pmf)
        x_i = np.random.choice(X_i,p = pmf)
        S.append(x_i)
        X_i.remove(x_i)
    return S,S_g

# def brute_force(X,n):

#     for comb in 
#     print comb


def surface_experiment():
    n = 10
    k = 10
    data = zeros((10,10))
    


def main():
    n = 24
    n = n - n%2
    # #print(set_coverage(X))
    # #print(set_coverage(OPT))
    # S,S_g = greedy_pairwise(X,n,LB = True)
    # print(set_coverage(S))
    # print(set_coverage(OPT))
    m = math.floor(math.pow(2,n/2+1))

    #m =1000
    #X,OPT = generate_worst_case_pessimistic(n,m)
    #X,OPT = generate_worst_case_optimistic(n,m)
    X,OPT = generate_worst_case_combined(n,m)
    #X = random_case(20,40,10)
    #OPT = max(itertools.combinations(X, n),key = lambda S: set_coverage(S))
    print(OPT)
    #OPT = [set("e1")]
    # print(set_coverage(X))
    # print(set_coverage(OPT))
    S_p,_ = probabalistic_choice(X,n)
    
    print(len(X))
    S_l,_ = greedy_pairwise(X,n,LB = True)
    print(len(X))
    S_u,_ = greedy_pairwise(X,n,LB = False)
    print(len(X))
    S_sum,_ = pairwise_sum(X,n)
    S_alt,_ = greedy_pairwise_alt(X,n)
    print(len(X))
    print("Alternating",set_coverage(S_alt)/set_coverage(OPT))
    print("Upper bound",set_coverage(S_u)/set_coverage(OPT))
    print("Lower Bound",set_coverage(S_l)/set_coverage(OPT))
    print("Probalistic",set_coverage(S_p)/set_coverage(OPT))
    print("Sum",set_coverage(S_sum)/set_coverage(OPT))

if __name__ == '__main__':
    main()