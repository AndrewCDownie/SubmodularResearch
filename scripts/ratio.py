import matplotlib.pyplot as plt
from shapely.geometry import Point
from math import sqrt, pi, pow
from modules.visualization import visualization
import pygame
def calcRatio(p1,p2,p3):
    A1 = Point((p1['x'],p1['y'])).buffer(p1['r'])
    A2 = Point((p2['x'],p2['y'])).buffer(p2['r'])
    A3 = Point((p3['x'],p3['y'])).buffer(p3['r'])

    ratio = (A1.intersection(A2).area+ A1.intersection(A3).area+A2.intersection(A3).area)/(A1.intersection(A2).intersection(A3).area+1)
    return ratio

def calcRatio4(p1,p2,p3,p4):
    A1 = Point((p1['x'],p1['y'])).buffer(p1['r'])
    A2 = Point((p2['x'],p2['y'])).buffer(p2['r'])
    A3 = Point((p3['x'],p3['y'])).buffer(p3['r'])
    A4 = Point((p4['x'],p4['y'])).buffer(p4['r'])
    numerator = A1.area+ A2.area+ A3.area+ A4.area-A1.intersection(A2).area- A1.intersection(A3).area-A2.intersection(A3).area - A4.intersection(A1).area - A4.intersection(A2).area - A4.intersection(A3).area
    numerator = A1.intersection(A2).area + A1.intersection(A3).area+A2.intersection(A3).area + A4.intersection(A1).area + A4.intersection(A2).area + A4.intersection(A3).area
    denominator =1 + A1.intersection(A2).intersection(A3).area + A1.intersection(A2).intersection(A4).area + A1.intersection(A3).intersection(A4).area +A2.intersection(A3).intersection(A4).area -A1.intersection(A2).intersection(A3).intersection(A4).area
    return numerator/denominator

    
    return ratio
    #print(A1.area)

p1 = {"x":10+1,"y":10+1,"r":4}
p2 = {"x":10+1,"y":10+8,"r":4}
p3 = {"x":10+4,"y":10+1,"r":4}
p4 = {"x":10+4,"y":10+1,"r":4}

calcRatio(p1,p2,p3)


dims = [25,25]
scale = 20
vis = visualization(dims,scale)






running = True
while running:
    vis.clear()
    vis.draw_circles_dict([p1],"BLUE")
    vis.draw_circles_dict([p2],"RED")
    vis.draw_circles_dict([p3],"GREEN")
    vis.draw_circles_dict([p4],"PURPLE")
    vis.update()
    val = calcRatio4(p1,p2,p3,p4)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                (mouse_pressed,_,_) = pygame.mouse.get_pressed()
                print("Key downie")
                if mouse_pressed == 1:
                    coords =pygame.mouse.get_pos()
                    p1['x'] = int(coords[0]/scale)
                    p1['y'] = int(coords[1]/scale)
            if event.key == pygame.K_2:
                (mouse_pressed,_,_) = pygame.mouse.get_pressed()
                if mouse_pressed == 1:
                    coords =pygame.mouse.get_pos()
                    p2['x'] = int(coords[0]/scale)
                    p2['y'] = int(coords[1]/scale)
            if event.key == pygame.K_3:

                (mouse_pressed,_,_) = pygame.mouse.get_pressed()
                if mouse_pressed == 1:
                    coords =pygame.mouse.get_pos()
                    p3['x'] = int(coords[0]/scale)
                    p3['y'] = int(coords[1]/scale)
            if event.key == pygame.K_4:

                (mouse_pressed,_,_) = pygame.mouse.get_pressed()
                if mouse_pressed == 1:
                    coords =pygame.mouse.get_pos()
                    p4['x'] = int(coords[0]/scale)
                    p4['y'] = int(coords[1]/scale)
            
    if val != calcRatio4(p1,p2,p3,p4):
        
        print("Ratio: ",calcRatio4(p1,p2,p3,p4))


