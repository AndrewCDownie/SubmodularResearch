import matplotlib.pyplot as plt
import matplotlib
import json
import pprint
import datetime
from taxi_analysis import open_ride_data
import matplotlib.dates as mdates
pp = pprint.PrettyPrinter()
import statistics
import numpy as np

import os

def get_total_rides():
    total_rides = []
    for t in range(12):
        start_time = datetime.datetime(2020,1,1,0, 0, 0)+datetime.timedelta(hours=2*t)
        end_time = datetime.datetime(2020,1,1,2, 0, 0)+datetime.timedelta(hours=2*t)
        counts = open_ride_data(start_time,end_time)
        total_rides.append(sum(counts))
    return total_rides


if __name__ == "__main__":
    latex = True

    #plotting and colour set ups
    if latex:
        matplotlib.use("pgf")
        matplotlib.rcParams.update({
            "pgf.texsystem": "pdflatex",
            'font.family': 'serif',
            'text.usetex': True,
            'pgf.rcfonts': False,
        })
    CB91_Blue = '#2CBDFE'
    CB91_Green = '#47DBCD'
    CB91_Pink = '#F3A0F2'
    CB91_Purple = '#9D2EC5'
    CB91_Violet = '#661D98'
    CB91_Amber = '#F5B14C'
    color_list = [CB91_Blue, CB91_Pink, CB91_Green, CB91_Amber,
              CB91_Purple, CB91_Violet]
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list)



    file_name = "../../../Experimental_Data/experiment 01-19-2021_15-19_soft.json"
    with open(file_name,"r") as infile:
        data = json.load(infile)
    # pp.pprint(data)

    # compute in values for each n
    
    #ratios = [min([100*data[j]["lb_values"][i]/data[j]["greedy_values"][i] for i in range(len(data[j]["greedy_values"]))]) for j in range(12)]
    
    #compute averages over twelve trials
    fig_1, (ax1, ax2) = plt.subplots(1, 2)
    s = [14 for _ in range(data[11]["n"])]
    f_size = 7
    print("computing total rides")
    # total_rides = get_total_rides()
    # with open("/Users/andrewdownie/Documents/Graduate Studies/Research/Simulations/Experimental_Data/total_rides_dump.json","w+") as outfile:
    #     json.dump(total_rides,outfile)

    with open("../../../Experimental_Data/total_rides_dump.json","r+") as infile:
        total_rides = json.load(infile)
    n = data[0]['n']
    
    #Compute Averages over trials and minimum and maximum for the 3 algorithms
    averages_greedy = np.array([statistics.mean([100*data[j]['greedy_values'][i]/total_rides[j]  for j in range(12)]) for i in range(data[0]["n"])])
    max_greedy = np.array([max([100*data[j]['greedy_values'][i]/total_rides[j]  for j in range(12)]) for i in range(data[0]["n"])])
    min_greedy = np.array([min([100*data[j]['greedy_values'][i]/total_rides[j]  for j in range(12)]) for i in range(data[0]["n"])])
    
    averages_lb = [statistics.mean([100*data[j]['lb_values'][i]/total_rides[j]  for j in range(12)]) for i in range(data[0]["n"])]
    max_lb = np.array([max([100*data[j]['lb_values'][i]/total_rides[j]  for j in range(12)]) for i in range(data[0]["n"])])
    min_lb = np.array([min([100*data[j]['lb_values'][i]/total_rides[j]  for j in range(12)]) for i in range(data[0]["n"])])

    averages_ub = [statistics.mean([100*data[j]['ub_values'][i]/total_rides[j]  for j in range(12)]) for i in range(data[0]["n"])]
    max_ub = np.array([max([100*data[j]['ub_values'][i]/total_rides[j]  for j in range(12)]) for i in range(data[0]["n"])])
    min_ub = np.array([min([100*data[j]['ub_values'][i]/total_rides[j]  for j in range(12)]) for i in range(data[0]["n"])])

    #Find worst performance compared to greedy for both lower and upper bound algorithms

    min_ratio_lb = min([min([100*data[j]['lb_values'][i]/data[j]['greedy_values'][i] for j in range(12)]) for i in range(data[0]['n'])])
    min_ratio_ub = min([min([100*data[j]['ub_values'][i]/data[j]['greedy_values'][i] for j in range(12)]) for i in range(data[0]['n'])])

    print("min ratio lb",min_ratio_lb)
    print("min ratio ub",min_ratio_ub)

    #Compute average theoretical bounds with mins and maxes for lower bound algorithm
    average_theoretical_bounds_lb = [statistics.mean([data[j]['theoretical_bounds_lb'][i]  for j in range(12)]) for i in range(data[0]["n"]-1)]
    max_tb_lb = np.array([max([data[j]['theoretical_bounds_lb'][i]  for j in range(12)]) for i in range(data[0]["n"]-1)])
    min_tb_lb = np.array([min([data[j]['theoretical_bounds_lb'][i]  for j in range(12)]) for i in range(data[0]["n"]-1)])

    average_estimated_bounds_lb = [statistics.mean([data[j]['estimated_bounds_lb'][i]  for j in range(12)]) for i in range(data[0]["n"]-1)]
    max_eb_lb = np.array([max([data[j]['estimated_bounds_lb'][i]  for j in range(12)]) for i in range(data[0]["n"]-1)])
    min_eb_lb = np.array([min([data[j]['estimated_bounds_lb'][i]  for j in range(12)]) for i in range(data[0]["n"]-1)])

    #Compute average theoretical bounds with mins and maxes for upper bound algorithm
    average_theoretical_bounds_ub = [statistics.mean([data[j]['theoretical_bounds_ub'][i]  for j in range(12)]) for i in range(data[0]["n"]-1)]
    max_tb_ub = np.array([max([data[j]['theoretical_bounds_ub'][i]  for j in range(12)]) for i in range(data[0]["n"]-1)])
    min_tb_ub = np.array([min([data[j]['theoretical_bounds_ub'][i]  for j in range(12)]) for i in range(data[0]["n"]-1)])

    average_estimated_bounds_ub = [statistics.mean([data[j]['estimated_bounds_ub'][i]  for j in range(12)]) for i in range(data[0]["n"]-1)]
    max_eb_ub = np.array([max([data[j]['estimated_bounds_ub'][i]  for j in range(12)]) for i in range(data[0]["n"]-1)])
    min_eb_ub = np.array([min([data[j]['estimated_bounds_ub'][i]  for j in range(12)]) for i in range(data[0]["n"]-1)])


    #plot average perfromances
    ax1.plot(list(range(1,n+1)),averages_greedy)
    ax1.plot(list(range(1,n+1)),averages_lb)
    ax1.plot(list(range(1,n+1)),averages_ub)

    #plot upper and lower bounds on performances
    ax1.fill_between(list(range(1,n+1)),  min_greedy,  max_greedy,color='blue', alpha=0.1)
    ax1.fill_between(list(range(1,n+1)),  min_lb,  max_lb,color='pink', alpha=0.1)
    ax1.fill_between(list(range(1,n+1)),  min_ub,  max_ub,color='cyan', alpha=0.1)
    ax1.legend(["Classical Greedy","Pessimistic Greedy","Optimistic Greedy"],fontsize=f_size)
    ax1.set_xlabel(r"$n$")
    ax1.set_ylabel("Total Rides Covered (%)")
    ax1.grid(b=True, which='major', color='#999999', alpha=0.2)
    ax1.minorticks_on()
    ax1.grid(b=True, which='minor', color='#999999', alpha=0.2)
    #plot avererage estimated and theoretical bounds
    ax2.plot(list(range(1,n)),average_theoretical_bounds_lb)
    ax2.plot(list(range(1,n)),average_estimated_bounds_lb)
    ax2.plot(list(range(1,n)),average_theoretical_bounds_ub)    
    ax2.plot(list(range(1,n)),average_estimated_bounds_ub)

    #plot min and maxes of the bounds
    ax2.fill_between(list(range(1,n)),  min_tb_lb,  max_tb_lb,color='blue', alpha=0.1)
    ax2.fill_between(list(range(1,n)),  min_eb_lb,  max_eb_lb,color='pink', alpha=0.1)
    ax2.fill_between(list(range(1,n)),  min_tb_ub,  max_tb_ub,color='cyan', alpha=0.1)
    ax2.fill_between(list(range(1,n)),  min_eb_ub,  max_eb_ub,color='orange', alpha=0.1)
    ax2.legend(["Pessimistic Theoretical","Pessimistic Estimated","Optimistic Theoretical","Optimistic Estimated"],fontsize=f_size)
    ax2.set_xlabel(r"$n$")
    ax2.set_ylabel("Lower Bound on Performance")

    #data through out the day
    fig_1.set_size_inches(w=7, h=3)
    ax2.grid(b=True, which='major', color='#999999', alpha=0.2)
    ax2.minorticks_on()
    ax2.grid(b=True, which='minor', color='#999999', alpha=0.2)
    plt.savefig("../../../Experimental_Data/expdata.pgf",bbox_inches='tight')

    #time of day analysis
    print("counting total rides")
    print("min time ratio",min([d['lb_values'][25]/total_rides[i] for i,d in enumerate(data)]))
    print("plotting")
    greedy_n_25 = [d['greedy_values'][25] for d in data]
    lb_n_25 = [d['lb_values'][25] for d in data]
    ub_n_25 = [d['ub_values'][25] for d in data]
    hour_starts = [datetime.time(2*d["t"],0,0) for d in data]
    fig_2,ax = plt.subplots() 
    ax.scatter(hour_starts,greedy_n_25,s = s)
    ax.scatter(hour_starts,lb_n_25, s = s)
    ax.scatter(hour_starts,ub_n_25, s = s)
    ax.scatter(hour_starts,total_rides,s = s)
    ax.legend(["Classical Greedy","Pessimistic Greedy ","Optimistic Greedy","Total Number of Rides"],fontsize = f_size,loc='lower right')
    ax.grid(b=True, which='major', color='#999999', alpha=0.2)
    ax.minorticks_on()
    ax.grid(b=True, which='minor', color='#999999', alpha=0.2)
    fig_2.set_size_inches(w=3, h=3)
    ax.set_xlabel("Time")
    ax.set_ylabel("Number of Rides Covered")
    plt.savefig("../../../Experimental_Data/time_of_day.pgf",bbox_inches='tight')

    #speed analysis data
    file_name = "../../../Experimental_Data/speed experiment 01-19-2021_18-46_soft.json"
    with open(file_name,"r") as infile:
        data = json.load(infile)
    
    fig_3,ax = plt.subplots() 
    n_s = list(range(1,51))
    average_greedy_times = np.array([statistics.mean([data[j]['g_times'][i]/1000 for j in range(12)]) for i in range(len(data[0]['g_times']))])
    average_lb_times = np.array([statistics.mean([data[j]['lb_times'][i]/1000 for j in range(12)]) for i in range(len(data[0]['lb_times']))])
    average_ub_times = np.array([statistics.mean([data[j]['ub_times'][i]/1000 for j in range(12)]) for i in range(len(data[0]['lb_times']))])
    print(average_greedy_times)


    max_greedy_times = np.array([max([data[j]['g_times'][i]/1000 for j in range(12)]) for i in range(len(data[0]["g_times"]))])
    max_lb_times     = np.array([max([data[j]['lb_times'][i]/1000 for j in range(12)]) for i in range(len(data[0]["lb_times"]))])
    max_ub_times     = np.array([max([data[j]['ub_times'][i]/1000 for j in range(12)]) for i in range(len(data[0]["ub_times"]))])

    min_greedy_times = np.array([min([data[j]['g_times'][i]/1000 for j in range(12)]) for i in range(len(data[0]["g_times"]))])
    min_lb_times     = np.array([min([data[j]['lb_times'][i]/1000 for j in range(12)]) for i in range(len(data[0]["lb_times"]))])
    min_ub_times     = np.array([min([data[j]['ub_times'][i]/1000 for j in range(12)]) for i in range(len(data[0]["ub_times"]))])


    ratio_times_lb = [average_greedy_times[i]/average_lb_times[i] for i in range(len(average_greedy_times))]
    ratio_times_ub = [average_greedy_times[i]/average_ub_times[i] for i in range(len(average_greedy_times))]
    


    ax.plot(n_s,average_greedy_times,)
    ax.plot(n_s,average_lb_times)
    ax.plot(n_s,average_lb_times)

    ax.fill_between(n_s,  min_greedy_times,  max_greedy_times,color='blue', alpha=0.1)
    ax.fill_between(n_s,  min_lb_times,  max_lb_times,color='pink', alpha=0.1)
    ax.fill_between(n_s,  min_ub_times,  max_ub_times,color='cyan', alpha=0.1)
    ax.grid(b=True, which='major', color='#999999', alpha=0.2)
    ax.minorticks_on()
    ax.grid(b=True, which='minor', color='#999999', alpha=0.2)
    fig_3.set_size_inches(w=3, h=3)
    plt.legend(["Greedy","Pessimistic","Optimistic"],fontsize=f_size)
    ax.set_xlabel(r"$n$")
    ax.set_ylabel("Execution Time (s)")
    plt.savefig("../../../Experimental_Data/execution_times.pgf",bbox_inches='tight')

    fig_4,ax = plt.subplots()
    ax.plot(n_s,ratio_times_lb)
    ax.plot(n_s,ratio_times_ub)
    ax.legend(["Pessimistic","Optimistic"],fontsize=f_size)
    ax.grid(b=True, which='major', color='#999999', alpha=0.2)
    ax.minorticks_on()
    ax.grid(b=True, which='minor', color='#999999', alpha=0.2)
    fig_4.set_size_inches(w=3, h=3)
    ax.set_xlabel(r"$n$")
    ax.set_ylabel("Ratio with Classical Greedy Execution Time")
    plt.savefig("../../../Experimental_Data/execution_ratios.pgf",bbox_inches='tight')
    plt.show()
