
import sys
sys.path.append("..")
import math
import matplotlib.pyplot as plt
from pairwisecoverage import area, similarity_weight, dist
from submodular_sim import submodular_sim

#from visualization import visualization
import random
import pprint
from itertools import combinations_with_replacement,permutations,product

from linetimer import CodeTimer

def lowerbound_with_greedy_choice_sequential(X,n):
    S = []
    S_g = []
    X_i = X.copy()
    prev_value = 0
    for i in range(n):
        print("Selecting element ",i)
        x_i = max(X_i,key = lambda x:sim.full_info_lowerbound(x,S))
        x_g_i = max(X_i,key = lambda x:sim.delta(x,S))
        X_i.remove(x_i)
        S.append(x_i)
        S_g.append(x_g_i)
        prev_value = sim.f(S)
        
    return S,S_g


def lowerbound_with_greedy_choice_sequential_width_admissable(X,n):
    S = []
    S_g = []
    X_i = X.copy()
    
    for i in range(n):
        print("Selecting element ",i)
        x_g_i = max(X_i,key = lambda x:sim.delta(x,S))
        x_i = X_i[0]
        fx_max = sim.full_info_lowerbound_v2(x_i,S)

        for x in X_i:
            fx = sim.full_info_lowerbound_v2(x,S)
            if fx > fx_max:
                if sim.full_info_upperbound(x,S)>0:
                    x_i = x 
                    fx_max = fx
        X_i.remove(x_i)
        S.append(x_i)
        S_g.append(x_g_i)
        
    return S,S_g

def lowerbound_with_greedy_choice_matroid(Xn):
    S = []
    S_g = []
    prev_value = 0
    for X_i in Xn:
        x_i = max(X_i,key = lambda x:sim.full_info_lowerbound_v2(x,S))
        x_g_i = max(X_i,key = lambda x:sim.delta(x,S))
        S.append(x_i)
        S_g.append(x_g_i)
        prev_value = sim.coverage([S])

    return S,S_g

def theoretical_alphas(S,S_g):
    alphas = []
    for i in range(len(S)):
        alpha_i = sim.delta(S_g[i],S[:i])/(sim.delta(S[i],S[:i])+0.0000001)
        print("numer",sim.delta(S_g[i],S[:i]))
        print("denom",sim.delta(S[i],S[:i]))
        alphas.append(alpha_i)
        print("alpha",alpha_i)
    return alphas 


def compute_alphas(S,S_g):
    alphas = []
    uppers = []
    lowers = []
    g_lowers = []
    g_uppers = []
    for i in range(len(S)):
        print(S_g[i])
        f_x = sim.coverage([S[i]])
        upper = sim.full_info_upperbound(S_g[i],S[:i])
        lower = sim.full_info_lowerbound_v2(S_g[i],S[:i])
        g_lowers.append(max([sim.full_info_lowerbound_v2(S[i],S[:i]),0]))
        g_uppers.append(sim.full_info_upperbound(S[i],S[:i])/f_x)
        alpha =  (upper/(max([lower,0.000001])))
        print(upper,lower)
        print("alpha_",i," ",alpha)
        alphas.append(alpha)
        f_x = sim.coverage([S_g[i]])
        uppers.append(upper/f_x)
        lowers.append(lower/f_x)
    return alphas,uppers,lowers,g_lowers,g_uppers

# def compute_bound_sequential(alphas):
#     numerator = 1
#     denominator = 1
#     n = len(alphas)
#     for alpha in alphas:
#         numerator = numerator*(alpha*n-1)
#         denominator =denominator*(alpha*n)
#     bound = 1-numerator/denominator
#     return bound

def compute_bound_sequential(alphas):
    n = len(alphas)
    if n == 1:
        return 1-(alphas[0]-1)/alphas[0]
    log_sum = 0
    for alpha in alphas:
        log_sum += math.log(alpha*n-1)-math.log(alpha*n)
    
    bound = 1-math.exp(log_sum)
    return bound


def compute_bound_matriod(alphas,S):
    f_S = sim.coverage(S)
    alpha_sum = 0
    for i in range(len(S)):
        alpha_sum += alphas[i]*sim.delta(S[i],S[:i])
    bound = 1/(2+alpha_sum/f_S)
    return bound


def computer_alphas_from_graph(Xn):
    weights = []
    for i in range(len(Xn)):
        weights.append([])
        for j in range(i):
            pairs = product(Xn[i],Xn[j])
            max_pair = max(list(pairs),key = lambda pair:area(pair[0],pair[1]))
            weight = area(max_pair[0],max_pair[1])
            weights[i].append(weight)
    return weights     

def compute_errors(S_g,S):
    errors = []
    marginals_g = []
    marginals = []
    lowers = []
    for i in range(len(S_g)):
        errors.append(sim.delta(S_g[i],S[:i]) - sim.full_info_lowerbound_v2(S_g[i],S[:i]))
        marginals_g.append(sim.delta(S_g[i],S[:i]))
        marginals.append(sim.delta(S[i],S[:i]))
        lowers.append(sim.full_info_lowerbound_v2(S_g[i],S[:i]))
    return errors,marginals,marginals_g,lowers
#print(X)  




def minimum_loss(X,n):
    S = []
    S_g = []
    S_l = []
    S_h = []
    Xn = X.copy()
    for i in range(n):
        print("Selecting Element ",i)
        #compute elements with max upperbound
        x_l = max(Xn,key = lambda x: sim.full_info_lowerbound_v2(x,S))
        x_h = max(Xn,key = lambda x: sim.full_info_upperbound(x,S))

        #compute reference 
        x_g =max(Xn,key = lambda x: sim.delta(x,S))
        S_g.append(x_g)
        # find element with second highest upperbound
        Xl = Xn.copy()
        Xl.remove(x_h)
        x_h2 =max(Xl,key = lambda x: sim.full_info_upperbound(x,S))
        
        #compute max losses 
        upper_loss = sim.full_info_upperbound(x_h2,S) - min([sim.full_info_lowerbound_v2(x_h,S),0])
        lower_loss = sim.full_info_upperbound(x_h,S) - min([sim.full_info_lowerbound_v2(x_l,S),0])
        
        if lower_loss<upper_loss:
            S.append(x_l)
            Xn.remove(x_l)
            print("selecting Lower")
        else:
            print("selecting Upper")
            S.append(x_h)
            Xn.remove(x_h)
        S_l.append(x_l)
        S_h.append(x_h)

    return S,S_g,S_l,S_h


def risk_reward_select(X,n,beta):
    S = []
    S_g = []
    X_i = X.copy()
    for i in range(n):
        print("selecting",i)
        #compute Reference
        x_g =max(X_i,key = lambda x: sim.delta(x,S))
        S_g.append(x_g)
        #compute Lowerbound
        x_l = max(X_i,key = lambda x: sim.full_info_lowerbound_v2(x,S))
        
        #set up max lower and current max upper bound
        x_i = x_l
        max_lower = max([sim.full_info_lowerbound_v2(x_l,S),0])
        max_upper = sim.full_info_upperbound(x_l,S)

        #find max value upperbound such that the lowerbound is guarrenteed
        for x in X_i:
            ub = sim.full_info_upperbound(x,S)
            if ub > max_upper and max([sim.full_info_lowerbound_v2(x,S),0]) >= beta*max_lower:
                max_upper = ub
                x_i = x
        S.append(x_i)
        X_i.remove(x_i)
    
    return S,S_g

def alternating_greedy(X,n):
    S = []
    S_g = []
    X_i = X.copy()
    for i in range(n):
        print("Selecting",i)
        #compute Reference
        x_g =max(X_i,key = lambda x: sim.delta(x,S))
        S_g.append(x_g)
        if i % 2 == 0:
            x_i = max(X_i,key = lambda x: sim.full_info_lowerbound_v2(x,S))
        else:
            x_i = max(X_i,key = lambda x: sim.full_info_upperbound(x,S))
        S.append(x_i)
        X_i.remove(x_i)
    return S,S_g

def update_animation(fig1,ax1,ax2,vis,marginals,marginals_g,errors,X,S,x_g,bounds):
    #update plots
    ax1.clear()
    ax1.plot(marginals,marker="o")
    ax1.plot(marginals_g)
    ax1.set_ylabel("Marginal return")
    ax1.legend([r"$f(x_i|S_{i-1})$",r"$f(x_i^g|S_{i-1})$"])
    ax1.title.set_text("Marginal Returns")

    ax2.clear()
    ax2.title.set_text("Approximiation bound")
    ax2.set_ylabel("Appoximation factor")
    ax2.plot(bounds)
    fig.canvas.draw()
    fig.canvas.flush_events()
    vis.clear()
    #update visualization
    vis.draw_circles_dict(X,"PURPLE",width = 1)
    vis.draw_circles_dict(S,"BLUE")
    vis.draw_circles_dict(S,"BLACK",width = 1)
    vis.draw_circles_dict([S[-1]],"GREEN",width = 1)
    vis.draw_circles_dict([x_g],"RED",width = 2)
    vis.update()



def lb_greedy(X,n,sim):
    X = X.copy()
    S = []
    for i in range(n):
        x_i = max(X,key = lambda x:sim.full_info_lowerbound_v2(x,S))
        S.append(x_i)
        X.remove(x_i)
    return S

def lb_greedy_accelerated(X,n,sim):
        #initalize lists
        if n == 0:
            return []
        X = X.copy()
        S = []

        #compute inital marginals
        lb_marginals = [{"idx":x,"marg":sim.coverage([x])} for x in X]
        x_i = max(lb_marginals,key = lambda x:x['marg'])
        lb_marginals.remove(x_i)
        S.append(x_i['idx'])

        #greedily select rest
        for i in range(1,n):
            # update marginals
            for i in range(len(lb_marginals)):
                #lb_marginals[i]["marg"] -= area(lb_marginals[i]['idx'],x_i['idx']) 
                lb_marginals[i]["marg"] -= sim.coverage([lb_marginals[i]['idx']])+ sim.coverage([x_i['idx']]) -  sim.coverage([x_i['idx'],lb_marginals[i]['idx']])
            x_i = max(lb_marginals,key = lambda x:x['marg'])
            lb_marginals.remove(x_i)
            S.append(x_i['idx'])
        return S


if __name__ == '__main__':
    random.seed(2)
    pp = pprint.PrettyPrinter()
    #Theorem for stationary distribution

    n =10

    m1 = 200
    dims = [50,50]
    offset = 20
    dims_outer = [dims[0]+2*offset,dims[1]+2*offset]
    alphas = []
    sim = submodular_sim(dims= dims)
    a = 400
    b = 600
    X = [{'x':random.random()*dims[0]+offset,'y':random.random()*dims[1]+offset,'r':random.uniform(math.sqrt(a/math.pi),math.sqrt(b/math.pi))} for i in range(m1)]
    m2 = 3
    #Xn = [[{'x':random.random()*dims[0],'y':random.random()*dims[1],'r':random.uniform(math.sqrt(a/math.pi),math.sqrt(b/math.pi))} for i in range(m2)]for i in range(n)]

    
    print("Computing Greedy Algorithm") 
    ct_lb = CodeTimer("lb_greedy",unit = "s")
    ct_g = CodeTimer("greedy",unit = "s")
    ct_lba = CodeTimer("accel lb greedy",unit = "s")

    lb_times = []
    g_times = []
    lba_times = []

    n_s = list(range(0,50,10))
    for n_test in n_s:
        with ct_lb:
            S = lb_greedy(X,n_test,sim)
        print(ct_lb.took)
        print(sim.coverage(S))
        lb_times.append(ct_lb.took)

        with ct_g:
            S_g = sim.fast_coverage_greedy(X, n_test)
        print(ct_g.took)
        print(sim.coverage(S))
        g_times.append(ct_g.took)

        with ct_lba:
            S_g = lb_greedy_accelerated(X,n_test,sim)
        print(ct_lba.took)
        print(sim.coverage(S))
        lba_times.append(ct_lba.took)

    plt.plot(n_s,lb_times)
    plt.plot(n_s,g_times)
    plt.plot(n_s,lba_times)
    plt.legend(["lb","greedy","lba"])
    plt.show()









    
