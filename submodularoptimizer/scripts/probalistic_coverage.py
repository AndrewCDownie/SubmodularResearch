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
from linetimer import CodeTimer
from alpha_factors import compute_bound_sequential

class ProbablisticCoverage:
    def __init__(self,n_e,n_s,r_s,dims):
        #random sample events
        self.events = [(dims[0]*random.random(), dims[1]*random.random()) for i in range(n_e)]
        self.event_values = [1/n_e for _ in range(n_e)]

        #randomly generate sensors
        self.sensors = [(dims[0]*random.random(), dims[1]*random.random()) for i in range(n_s)]
        self.r_s = r_s
        self.n_s = n_s
    
    @classmethod
    def from_events_and_sensors(cls,events,sensors,values,r_s):
        instance = cls.__new__(cls)
        super(ProbablisticCoverage,instance).__init__()
        instance.events = events
        instance.sensors = sensors
        instance.event_values = values
        instance.r_s = r_s
        instance.n_s = len(instance.sensors)
        print(instance)
        return instance


    def objective(self,S,soft = True):
        terms = [(1-self.get_event_prob_product(e, S,soft))*self.event_values[i] for i,e in enumerate(self.events)]
        return sum(terms)
        
    def marginal(self,x,S,soft = True):
        terms = [(1-self.get_event_prob_product(e,[x],soft))*self.get_event_prob_product(e,S,soft)*self.event_values[i] for i,e in enumerate(self.events)]
        return sum(terms)

    def get_event_prob_product(self,event,S,soft):
        probs = [1-self.get_prob(event,x,soft)+ 0.000001 for x in S]
        #print(probs)
        return math.exp(sum(map(math.log, probs)))

    def get_prob(self,event,x,soft):
        if soft:
            return math.exp(-math.pow(self.dist(event,x),2)/math.pow(self.r_s,2))
        else:
            return 1 if self.dist(x,event) < self.r_s else 0 

    def dist(self,p1,p2):
        return math.sqrt(math.pow(p1[0]-p2[0],2)+ math.pow(p1[1]-p2[1],2))

    
    def greedy(self,n,soft = True):
        Sensors = self.sensors.copy()
        S = []
        for i in range(n):
            # print("selecting",i)
            x = max(Sensors,key = lambda x: self.marginal(x,S,soft = soft))
            S.append(x)
            Sensors.remove(x)
        return S

    def pairwise_lowerbound(self,x,S):
        fx = self.objective([x])
        marg = fx
        for s in S:
            marg -= fx-self.marginal(x,[s])
        return marg

    def pairwise_upperbound(self,x,S):
        if len(S) == 0:
            return self.objective([x])
        s_min = min(S, key = lambda s: self.marginal(x, [s]))
        return self.marginal(x,[s_min])

    def fast_lowerbound(self,x,S):
        values = [self.event_values[i]*self.get_prob(e,x)*(1-sum([self.get_prob(e, s) for s in S])) for i,e in enumerate(self.events)]
        return sum(values)

    def lowerbound_greedy_accelerated(self,n):
        #initalize lists
        X = self.sensors.copy()
        S = []
        #compute inital marginals
        lb_marginals = [{"idx":x,"marg":self.objective([x])} for x in X]
        x_i = max(lb_marginals,key = lambda x:x['marg'])
        lb_marginals.remove(x_i)
        S.append(x_i['idx'])

        #greedily select rest
        for i in range(1,n):
            # update marginals
            for i in range(len(lb_marginals)):
                lb_marginals[i]["marg"] -= self.objective([lb_marginals[i]['idx']]) + self.objective([x_i['idx']]) - self.objective([lb_marginals[i]['idx'],x_i['idx']]) 

            x_i = max(lb_marginals,key = lambda x:x['marg'])
            lb_marginals.remove(x_i)
            S.append(x_i['idx'])
        return S,S,S

    def lowerbound_greedy(self,n):
        Sensors = self.sensors.copy()
        S_u = []
        S_g = []
        S = []
        for i in range(n):
            # print("selecting",i)
            x = max(Sensors,key = lambda x: self.fast_lowerbound(x,S))
            x_u = max(Sensors,key = lambda x: self.pairwise_upperbound(x,S))
            x_g = max(Sensors,key = lambda x: self.marginal(x,S))
            S.append(x)
            S_u.append(x_u)
            S_g.append(x_g)
            Sensors.remove(x)
        return S,S_u,S_g



class ProbablisticCoverage_v2:
    def __init__(self,events,sensors,values,r_s,soft_edges = False,soft_edge_eps = 0):
        self.events = events
        self.sensors = sensors
        self.values = values
        self.r_s = r_s
        self.sensor_sets = []
        self.soft_edges = soft_edges
        self.soft_edge_eps = soft_edge_eps
        
        for s in self.sensors:
            sensor_set = []
            for j,e in enumerate(self.events):
                if self.get_prob(e,s,soft = self.soft_edges) > self.soft_edge_eps:
                        sensor_set.append(j)

                    
            self.sensor_sets.append(sensor_set)
        print(len(self.sensor_sets))

    def objective(self,S):
        """
        S is now a list of indices of data data points

        Need to change this for soft edges
        """

        total_events  = set()
        for s in S:
            total_events |= set(self.sensor_sets[s])

        if not self.soft_edges:
            value = sum([self.values[i] for i in total_events])
        else:
            value = sum([(1-self.get_event_prob_product(e, S,self.soft_edges))*self.values[e] for e in total_events])
            
        return value

    def get_prob(self,event,x, soft = False):
        if soft:
            return math.exp(-math.pow(self.dist(event,x),2)/math.pow(self.r_s,2))
        else:
            return 1 if self.dist(x,event) < self.r_s else 0    
    
    def get_event_prob_product(self,e,S,soft):
        probs = [1-self.get_prob(self.events[e],self.sensors[x],soft)+ 0.000001 for x in S]
        #print(probs)
        return math.exp(sum(map(math.log, probs)))
            
    def dist(self,p1,p2):
        return math.sqrt(math.pow(p1[0]-p2[0],2)+ math.pow(p1[1]-p2[1],2))

    def greedy(self,n,timing = False):
        X = list(range(len(self.sensor_sets)))
        S = []
        for i in range(n):
            x = max(X,key = lambda x: self.objective(S+[x])-self.objective(S))
            S.append(x)
            X.remove(x)
        return S

    def greedy_with_timing(self,n):
        ct = CodeTimer()
        X = list(range(len(self.sensor_sets)))
        S = []
        times = []
        cummulative_time = 0
        for i in range(n):
            with ct:
                x = max(X,key = lambda x: self.objective(S+[x])-self.objective(S))
                S.append(x)
                X.remove(x)
            cummulative_time += ct.took
            times.append(cummulative_time)
        return S, times


    def marginal(self,x,S):
        return self.objective(S+[x])-self.objective(S)


    def lb_greedy(self,n):
        X = list(range(len(self.sensor_sets)))
        S = []
        for i in range(n):
            # print("selecting",i)
            x = max(X,key = lambda x: self.pairwise_lowerbound(x,S))
            #print(self.pairwise_lowerbound(x,S))
            S.append(x)
            X.remove(x)
        return S

    def lb_greedy_2(self,n):
        X = list(range(len(self.sensor_sets)))
        S = []
        for i in range(n):
            # print("selecting",i)
            x = max(X,key = lambda x: self.pairwise_lowerbound_v2(x,S))
            S.append(x)
            X.remove(x)
        return S




    def bound_greedy_accel_general(self,n,lowerbound = True):
        #initalize lists
        X = list(range(len(self.sensor_sets)))
        S = []
        #compute inital marginals
        marginals = [{"idx":x,"marg":self.objective([x])} for x in X]
        singluar_values  = [m['marg']for m in marginals]
        #greedily select rest
        for i in range(n):
            # select
            x_i = max(marginals,key = lambda x:x['marg'])
            marginals.remove(x_i)
            S.append(x_i['idx'])  
            #update other marginalså
            for i in range(len(marginals)):
                f_x_i = self.objective([x_i['idx']])
                if lowerbound:
                    #marginals[i]["marg"] -= self.objective([marginals[i]['idx']]) + f_x_i - self.objective([marginals[i]['idx'],x_i['idx']]) 
                    marginals[i]["marg"] -= singluar_values[marginals[i]['idx']] + f_x_i - self.objective([marginals[i]['idx'],x_i['idx']])
                else:
                    marg = self.objective([marginals[i]['idx'],x_i['idx']]) - f_x_i
                    marginals[i]["marg"] = min([marginals[i]['marg'], marg])
            
              

        return S


    def lb_greedy_accel_specialized(self,n):
        #print("accell specialized")
        X = list(range(len(self.sensor_sets)))
        S = []
        x_i_sets = [set(self.sensor_sets[x]) for x in X]
        marginals = [{"idx":x,"marg":self.objective([x])} for x in X]
        for i in range(n):
            x_i = max(marginals,key = lambda x:x['marg'])
            #print(x_i['marg'])
            marginals.remove(x_i)
            S.append(x_i["idx"])
            for i in range(len(marginals)):
                marginals[i]["marg"] -= sum([self.values[i] for i in x_i_sets[marginals[i]['idx']].intersection(x_i_sets[x_i['idx']])])
            
        return S


    # def lb_greedy_accel(self,n):

    #     #initalize lists
    #     X = list(range(len(self.sensor_sets)))
    #     S = []
    #     x_i_sets = [set(self.sensor_sets[x]) for x in X]

    #     #compute inital marginals
    #     lb_marginals = [{"idx":x,"marg":self.objective([x])} for x in X]
    #     x_i = max(lb_marginals,key = lambda x:x['marg'])
    #     lb_marginals.remove(x_i)
    #     S.append(x_i['idx'])

    #     #greedily select rest
    #     for i in range(1,n):
    #         # update marginals
    #         for i in range(len(lb_marginals)):
    #             lb_marginals[i]["marg"] -= sum([self.values[i] for i in x_i_sets[lb_marginals[i]['idx']].intersection(x_i_sets[x_i['idx']])])

    #         x_i = max(lb_marginals,key = lambda x:x['marg'])
    #         lb_marginals.remove(x_i)
    #         S.append(x_i['idx'])
    #     return S
        

    def pairwise_lowerbound_v2(self,x,S):
        fx = sum([self.values[i] for i in self.sensor_sets[x]])
        x_set = set(self.sensor_sets[x])
        marg = fx
        for s in S:
            marg -= sum([self.values[i] for i in x_set.intersection(set(self.sensor_sets[s]))])
        return marg


    
    def pairwise_lowerbound(self,x,S):
        fx = self.objective([x])
        marg = fx
        for s in S:
            marg -= fx-self.objective([s]+[x])+self.objective([s])
        return marg

    def pairwise_upperbound(self,x,S):
        if len(S) == 0:
            return self.objective([x])
        x_k = min(S,key = lambda x_j:self.objective([x,x_j])-self.objective([x_j]))
        return self.objective([x,x_k])-self.objective([x_k])

    def find_greedy_choices(self,S,upperbound = False):
        X = list(range(len(self.sensor_sets)))
        S_g = []
        for i in range(len(S)):
            if upperbound:
                x = max(X,key = lambda x:self.pairwise_upperbound(x,S[:i]) )
            else:
                x = max(X,key = lambda x: self.objective(S[:i]+[x])-self.objective(S[:i]) )
            S_g.append(x)
            X.remove(S[i])
        return S_g


def run_trails(params,n_trials):
    """
    Each test will do 20 trails average
    We want to record
    - greedy strategy value
    - lb strategy value
    - true approximation factors
    - upper bound approximation factors
    - parameters of the trails average
    """

    for i in range(n_trials):
        problem = ProbablisticCoverage(params['n_e'],params['n_s'],params['r_s'],params['dims'])
        S_greedy = problem.greedy(params['n'])
        S_l,S_u,S_g = problem.lowerbound_greedy(params['n'])
        theoretical_alphas = [problem.marginal(S_g[i],S_l[:i])/max([problem.marginal(S_l[i],S_l[:i]),0.0000001] )for i in range(params['n'])]
        theoretical_bound = compute_bound_sequential(theoretical_alphas)
        print(theoretical_bound)


    






if __name__ == '__main__':
    problem = ProbablisticCoverage(50,30,10,[100,100])
    true_marginals = []
    lowerbounds = []
    for i in range(10):
        params = {"n_e":60,"n_s":50,"r_s":4,"dims":[10*i+1,10*i+1],"n":10+3*i}
        run_trails(params,1)
    # for i in range(30):
    #     print(" ")

    #     with CodeTimer():
    #         print("full objective",problem.objective(problem.sensors[:i]+[problem.sensors[-1]])-problem.objective(problem.sensors[:i]))
        
    #     with CodeTimer():
    #         true_marginals.append(problem.marginal(problem.sensors[-1],problem.sensors[:i]))

    #     with CodeTimer():
    #         lowerbounds.append(problem.pairwise_lowerbound(problem.sensors[-1],problem.sensors[:i]))



    # plt.plot(true_marginals)
    # plt.plot(lowerbounds)
    # plt.show()

    # with CodeTimer():
    #     S = problem.greedy(10)
    
    # with CodeTimer():
    #     S_lb = problem.lowerbound_greedy(10)
    # S_rand = random.choices(problem.sensors, k=10)
    # print("greedy",problem.objective(S))
    # print("lb",problem.objective(S_lb))
    # print("random",problem.objective(S_rand))