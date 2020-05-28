from modules.submodular_sim import submodular_sim
import random
from modules.visualization import visualization
from math import sqrt, pi
def run():
    dims = (100,100)
    vis =visualization(dims,5)

    n =20
    m =50 
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
        Xn.append([{'x':random.random()*100,'y':random.random()*100,'r':random.uniform(sqrt(a/pi),sqrt(b/pi))} for i in range(m)])
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
    Sg2 = sim.distributed_greedy(Xn,graph2)
    Sd1 = sim.distributed_dist_greedy(Xn,a,b) 
    S_aug = sim.distributed_augmented_greedy(Xn,graph2,a,b) 
    S_uninformed = sim.distributed_uninformed_greedy(Xn)
    print("Coverage with complete graph                       :",sim.coverage(Sg1))
    print("Coverage with missing edges                        :",sim.coverage(Sg2))
    print("Coverage with no edges                             :",sim.coverage(S_uninformed))
    print("Coverage with our algorithm and no edges in graph  :",sim.coverage(Sd1))
    print("Coverage with our algorithm and some edges in graph:",sim.coverage(S_aug)) 
    vis.draw_circles_dict(Sg1,"BLACK",width = 4)
    #vis.draw_circles_dict(S_uninformed,"BLUE")
    vis.draw_circles_dict(Sg2,"RED",width = 3)
    #vis.draw_circles_dict(Sd1,"GREEN",width= 2)
    vis.draw_circles_dict(S_aug,"PURPLE",width= 1)
    vis.update()
    vis.draw()
if __name__ =="__main__":
    run()
