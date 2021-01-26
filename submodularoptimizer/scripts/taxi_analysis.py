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
import datetime
import pandas as pd
from alpha_factors import compute_bound_sequential

from linetimer import CodeTimer
import os
import geopandas as gpd
import earthpy as et

import pprint
import probalistic_coverage
import json
pp = pprint.PrettyPrinter()



def plot_location_data(centroids_feet,counts,selected_centroids,alternative_centroids,r_s):
    locations = gpd.read_file("/Users/andrewdownie/Documents/Graduate Studies/Research/Simulations/taxi_data/taxi_zones.shp")
    max_index = counts.index(max(counts))
    fig,ax = plt.subplots(figsize=(5,5))
    locations.plot(ax = ax,color = "g")
    x,y = zip(*centroids_feet)
    counts = [c/2 for c in counts]
    ax.scatter(x,y,c = counts,s = counts)
    
    x_s,y_s = zip(*selected_centroids)
    x_s_a,y_s_a = zip(*alternative_centroids)
    #ax.scatter(x_s,y_s,color = "r",marker = "x")
    #ax.scatter(x_s_a,y_s_a,color = "b",marker = "+")

    # for c in selected_centroids:
    #     circle =  plt.Circle((c[0], c[1]), r_s*3937/1200,fill = False, color='r') 
    #     ax.add_artist(circle)

    # for c in alternative_centroids:
    #     circle =  plt.Circle((c[0], c[1]), r_s*3937/1200,fill = False, color='b') 
    #     ax.add_artist(circle)

    plt.show()



def open_locations_data():
    US_SURVEY_FOOT_TO_METER = 1200/3937
    locations = gpd.read_file("../../../taxi_data/taxi_zones.shp")
    centroids_meters = []
    centroids_feet = []
    
    for row in locations.iterrows():
        #print(row[1].get("geometry"))
        geometry  =  row[1].get("geometry")
        centroids_meters.append((geometry.centroid.x*US_SURVEY_FOOT_TO_METER,geometry.centroid.y*US_SURVEY_FOOT_TO_METER))
        centroids_feet.append((geometry.centroid.x,geometry.centroid.y))

    return centroids_meters,centroids_feet

def open_ride_data(start_time,end_time):
    #returns number of pick ups indexed by locationID
    file_path = "../../../taxi_data/fhv_tripdata_2020-01.csv"

    #Open file and convert column to datetime format
    df = pd.read_csv(file_path)

    #Collect the where the time of day constraint is met 
    df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])
    ride_sets =[df.loc[(df['pickup_datetime'] > start_time+datetime.timedelta(days=i)) & (df['pickup_datetime'] < end_time+datetime.timedelta(days=i))] for i in range(31)]
    rides = pd.concat(ride_sets)
    
    #compute the average values
    counts = [len(rides.loc[rides["PULocationID"] == i])/31 for i in range(1,264)]
    return counts

def compute_theoretical_alphas(S_g,S,problem):
    #theoretical_alphas_lb = [problem.marginal(S_g_l[i],S_lower[:i])/max([problem.marginal(S_lower[i],S_lower[:i]),0.00001] )for i in range(n)]
    theoretical_alphas = []
    for i in range(len(S)):
        if problem.marginal(S_g[i],S[:i]) > 0.0001:
            theoretical_alphas.append(problem.marginal(S_g[i],S[:i])/max([problem.marginal(S[i],S[:i]),0.00001] )) 
        else:
            print("numerator zero")
            theoretical_alphas.append(1)
    return theoretical_alphas

def effectiveness_experiment(n):
    centroids_meters, centroids_feet = open_locations_data()
    r_s = 3000
    experiment_data = []

    #Collect Data for testing
    count_sets = []
    for t in range(12):
        start_time = datetime.datetime(2020,1,1,0, 0, 0)+datetime.timedelta(hours=2*t)
        end_time = datetime.datetime(2020,1,1,2, 0, 0)+datetime.timedelta(hours=2*t)
        print(start_time)
        counts = open_ride_data(start_time,end_time)
        count_sets.append(counts)
    
    # with open('/Users/andrewdownie/Documents/Graduate Studies/Research/Simulations/Experimental_Data/countdata.json', 'w+') as outfile:
    #     json.dump(count_sets, outfile)
    
    #with open('/Users/andrewdownie/Documents/Graduate Studies/Research/Simulations/Experimental_Data/countdata.json', 'r') as infile:
    #    count_sets = json.load(infile)

    for t in range(12):
        estimated_bounds = []
        theoretical_bounds = []
        greedy_values = []
        lb_values = []
        
        start_time = datetime.datetime(2020,1,1,0, 0, 0)+datetime.timedelta(hours=2*t)
        end_time = datetime.datetime(2020,1,1,2, 0, 0)+datetime.timedelta(hours=2*t)
        print(start_time)
        counts = count_sets[t]
        g_timer = CodeTimer("greedy time",unit = "s")
        lb_timer = CodeTimer("lb time", unit = "s")
        ub_timer = CodeTimer("ub time", unit = "s")

        trial_data = {"n":n,"t":t}
        #initalize problem
        problem = probalistic_coverage.ProbablisticCoverage_v2(centroids_meters,centroids_meters,counts,r_s,soft_edges = True, soft_edge_eps = 0.05)
        
        # execute Algorithms
        with g_timer:
            S = problem.greedy(n)
        trial_data["greedy_time"] = g_timer.took
        
        with lb_timer:
            S_lower = problem.bound_greedy_accel_general(n,lowerbound = True)
        trial_data["lb_time"] = lb_timer.took

        with ub_timer:
            S_upper = problem.bound_greedy_accel_general(n,lowerbound = False)
        trial_data["ub_time"] = ub_timer.took


        # Lower Bound Approximation Analysis
        print("computing bounds for lower bound algo")
        S_g_l = problem.find_greedy_choices(S_lower)
        S_u_l = problem.find_greedy_choices(S_lower,upperbound=True)

        # for i in range(n):
        #     print("numer",problem.marginal(S_g_l[i],S_lower[:i]))
        #     print("denominator",max([problem.marginal(S_lower[i],S_lower[:i]),0.00001]))

        

        theoretical_alphas_lb = compute_theoretical_alphas(S_g_l,S_lower,problem)
        #print("Theortical Alphas",theoretical_alphas_lb)
        trial_data["theoretical_bounds_lb"] = [compute_bound_sequential(theoretical_alphas_lb[:i+1])for i in range(len(theoretical_alphas_lb))]

        
        # print("Theortical Alphas",theoretical_alphas_lb)
        # print("Theoretical Bound",trial_data["theoretical_bounds_lb"])

        estimated_alphas_lb = [problem.pairwise_upperbound(S_u_l[i],S_lower[:i])/max([problem.pairwise_lowerbound(S_lower[i],S_lower[:i]),0.0000001] )for i in range(n)]
        trial_data["estimated_bounds_lb"] = [compute_bound_sequential(estimated_alphas_lb[:i+1])for i in range(len(estimated_alphas_lb))]
    

        # print("Estimated Alphas",estimated_alphas_lb)
        # print("Estimated Bound",trial_data["estimated_bounds_lb"])


        print("computing bounds for upper bound algo")
        S_g_u = problem.find_greedy_choices(S_upper)

        theoretical_alphas_ub = compute_theoretical_alphas(S_g_u,S_upper,problem)
        trial_data["theoretical_bounds_ub"] = [compute_bound_sequential(theoretical_alphas_ub[:i+1])for i in range(len(theoretical_alphas_ub))]

        
        # print("Theortical Alphas ub",theoretical_alphas_ub)
        # print("Theoretical Bound ub",trial_data["theoretical_bounds_ub"])

        estimated_alphas_ub = [problem.pairwise_upperbound(S_upper[i],S_upper[:i])/max([problem.pairwise_lowerbound(S_upper[i],S_upper[:i]),0.00001] )for i in range(n)]
        trial_data["estimated_bounds_ub"] = [compute_bound_sequential(estimated_alphas_ub[:i+1])for i in range(len(estimated_alphas_ub))]
    

        # print("Estimated Alphas",estimated_alphas_ub)
        # print("Estimated Bound",trial_data["estimated_bounds_ub"])
        trial_data["greedy_values"] = [problem.objective(S[:i])for i in range(1,len(S)+1)]
        trial_data["lb_values"] = [problem.objective(S_lower[:i])for i in range(1,len(S)+1)]
        trial_data["ub_values"] = [problem.objective(S_upper[:i])for i in range(1,len(S)+1)]
        
        experiment_data.append(trial_data)

    print(experiment_data)
    now = datetime.datetime.now()
    date_time = now.strftime("%m-%d-%Y_%H-%M")
    print("date and time:",date_time)	
    with open('../../../Experimental_Data/experiment '+date_time+"_soft.json", 'w+') as outfile:
        json.dump(experiment_data, outfile)
    

    
def speed_experiment():
    centroids_meters, centroids_feet = open_locations_data()
    r_s = 3000
    experiment_data = []
    with open('../../../Experimental_Data/countdata.json', 'r') as infile:
        count_sets = json.load(infile)

    speed_data = []
    for t in range(12):
        data = {"t":t}
        print("Time:",t)
        data['g_times'] = []
        data['lb_times'] = []
        data['ub_times'] = []
        counts = count_sets[t]
        timer  = CodeTimer()
        problem = probalistic_coverage.ProbablisticCoverage_v2(centroids_meters,centroids_meters,counts,r_s,soft_edges = True,soft_edge_eps = 0.05)
        n_s = list(range(1,51))
        S, times = problem.greedy_with_timing(50)
        data['g_times'] = times
        for n in n_s:
            print("n = ",n)
            # print("greedy")
            # with timer:
            #     S = problem.greedy(n)
            # data['g_times'].append(timer.took)

            print("greedy")
            with timer:
                S = problem.bound_greedy_accel_general(n,lowerbound = True)
            data['lb_times'].append(timer.took)

            print("greedy")
            with timer:
                S = problem.bound_greedy_accel_general(n,lowerbound = False)
            data['ub_times'].append(timer.took)
        print(data)
        speed_data.append(data)
    now = datetime.datetime.now()
    date_time = now.strftime("%m-%d-%Y_%H-%M")
    with open('../../../Experimental_Data/speed experiment '+date_time+"_soft.json", 'w+') as outfile:
        json.dump(speed_data, outfile)
            



def set_version():
    centroids_meters, centroids_feet = open_locations_data()   
    r_s = 4000
    t = 6
    start_time = datetime.datetime(2020,1,1,0, 0, 0)+datetime.timedelta(hours=2*t)
    end_time = datetime.datetime(2020,1,1,2, 0, 0)+datetime.timedelta(hours=2*t)
    print(start_time)
    counts = open_ride_data(start_time,end_time)
    problem1 = probalistic_coverage.ProbablisticCoverage.from_events_and_sensors(centroids_meters,centroids_meters,counts,r_s)
    problem2 = probalistic_coverage.ProbablisticCoverage_v2(centroids_meters,centroids_meters,counts,r_s)
    problem3 = probalistic_coverage.ProbablisticCoverage_v2(centroids_meters,centroids_meters,counts,r_s,soft_edges = True,soft_edge_eps = 0.05)
    # with CodeTimer("P1 not soft"):
    #     o1 = problem1.objective(problem1.sensors[:100],soft = False)
    # print("problem 1 Objective",o1)
    # with CodeTimer("P1 soft"):
    #     o2 = problem1.objective(problem1.sensors[:100],soft = True)
    # print("problem 1 Objective",o2)

    # with CodeTimer("P2 not soft"):
    #     o3 = problem2.objective(list(range(100)))
    # print("problem 2 Objective",o3)
    # with CodeTimer("P2 soft"):
    #     o4 = problem3.objective(list(range(100)))
    # print("problem 3 Objective",o4)

    # with CodeTimer("Greedy 1"):
    #     S = problem1.greedy(10,soft = False)
    # print(problem1.objective(S))
    ct = CodeTimer()
    g_times = []
    lb_times = []
    ac_times = []
    acg_times = []
    g_values = []
    lb_values = []
    ac_values = []
    acg_values = []
    n_s = list(range(1,200,5))
    for n_test in n_s:
        with ct:
            S = problem2.greedy(n_test)
        g_times.append(ct.took)
        v = problem2.objective(S)
        print(v)
        g_values.append(v)

        with ct:
            S = problem2.lb_greedy_2(n_test)
        lb_times.append(ct.took)
        v = problem2.objective(S)
        print(v)
        lb_values.append(v)

        with ct:
            S = problem2.lb_greedy_accel(n_test)
        ac_times.append(ct.took)
        v = problem2.objective(S)
        print(v)
        ac_values.append(v)
        with ct:
            S = problem2.lb_greedy_accel_general(n_test)
        acg_times.append(ct.took)
        v = problem2.objective(S)
        print(v)
        acg_values.append(v)

    plt.figure()
    plt.plot(n_s,g_times)
    plt.plot(n_s,lb_times)
    plt.plot(n_s,ac_times)
    plt.plot(n_s,acg_times)
    plt.legend(["g","lb","ac","acg"])

    print(ac_values)
    print(lb_values)
    plt.figure()
    plt.plot(n_s,g_values)
    plt.plot(n_s,lb_values)
    plt.plot(n_s,ac_values)
    plt.plot(n_s,acg_values)
    plt.legend(["g","lb","ac","acg"])
    plt.show()
    print("original",problem2.pairwise_lowerbound(11,list(range(10))))
    print("accelerated",problem2.pairwise_lowerbound_v2(11,list(range(10))))
    

def testing():
    centroids_meters, centroids_feet = open_locations_data()   
    r_s = 4000
    t = 6
    start_time = datetime.datetime(2020,1,1,0, 0, 0)+datetime.timedelta(hours=2*t)
    end_time = datetime.datetime(2020,1,1,2, 0, 0)+datetime.timedelta(hours=2*t)
    print(start_time)
    #counts = open_ride_data(start_time,end_time)
    #with open('../../../Experimental_Data/test_countdata.json', 'w+') as outfile:
    #    json.dump(counts, outfile)
    
    with open('../../../Experimental_Data/test_countdata.json', 'r') as infile:
        counts = json.load(infile)

    problem2 = probalistic_coverage.ProbablisticCoverage_v2(centroids_meters,centroids_meters,counts,r_s)
    problem3 = probalistic_coverage.ProbablisticCoverage_v2(centroids_meters,centroids_meters,counts,r_s,soft_edges = True,soft_edge_eps = 0.05)

    k = 10
    with CodeTimer("general accel"):
        S = problem3.bound_greedy_accel_general(k,lowerbound = True)
    print(problem2.objective(S))
    # with CodeTimer("special accel"):
    #     S2 = problem2.lb_greedy_accel_specialized(k)
    # print(problem2.objective(S2))
    with CodeTimer("basic"): 
        S3 = problem3.lb_greedy(k)
    print(problem2.objective(S3))
    with CodeTimer("basic specialized"):
        S4 = problem2.lb_greedy_2(k)
    print(problem2.objective(S4))
    print(S)
    print(S3)
    print(S4)
    n = 25
  
    S_g = problem2.find_greedy_choices(S)
    S_u = problem2.find_greedy_choices(S,upperbound=True)

    margs = [problem2.objective([S[i]]+S[:i])-problem2.objective(S[:i]) for i in range(len(S))]
    g_margs = [problem2.objective([S_g[i]]+S[:i])-problem2.objective(S[:i]) for i in range(len(S))]
    
    u_margs_true = [problem2.pairwise_upperbound(S[i],S[:i]) for i in range(len(S))]
    u_margs = [problem2.pairwise_upperbound(S_u[i],S[:i]) for i in range(len(S))]

    l_margs_true = [problem2.pairwise_lowerbound(S[i],S[:i]) for i in range(len(S))]
    plt.figure()
    plt.plot(margs)
    plt.plot(g_margs)
    plt.legend(["marginals","best marginals "])
    plt.figure()
    plt.plot(u_margs)
    plt.plot(u_margs_true)
    plt.plot(l_margs_true)
    plt.legend(["Opt Upper bounds","our upperbound","lowerbounds"])
    plt.show()




if __name__ == "__main__":
    #effectiveness_experiment(40)
    speed_experiment()
    #testing()
   
    

