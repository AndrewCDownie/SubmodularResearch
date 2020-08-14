from modules.visualization import visualization
from modules.submodular_sim import submodular_sim
import pygame
import random

def draw(vis):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

if __name__ =="__main__":
    dims = (100,100)
    X = [{"x":random.random()*dims[0], "y":random.random()*dims[1], "r":random.randint(4,10)} for i in range(50)]
    
    sim = submodular_sim(X)
    sim.f = sim.coverage
    sim.dims = dims
    print("Regular Greedy")
    S1 = sim.greedy(20)
    print("Distance Greedy")
    S2 = sim.greedy(20,delta_f = sim.distDelta)
    print("Doc Sum Greedy")
    S3 = sim.greedy(20,delta_f = sim.docSumDelta)

    print("greedy output:",sim.coverage(S1))
    print("dist output:",sim.coverage(S2))
    print("doc sum output:",sim.coverage(S3))
    vis = visualization(dims,8)
    #vis.draw_circles_dict(X,"RED") 
    vis.draw_circles_dict(S1,"BLUE")
    vis.draw_circles_dict(S2,"PURPLE")
    vis.update()
    draw(vis)
    vis = visualization(dims,8)
    #vis.draw_circles_dict(X,"RED") 
    vis.draw_circles_dict(S1,"BLUE")
    vis.draw_circles_dict(S3,"PURPLE")
    vis.update()
    draw(vis)