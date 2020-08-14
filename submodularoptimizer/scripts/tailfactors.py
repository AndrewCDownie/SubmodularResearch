#tailing Term
from random import random
from shapely.geometry import Point
import itertools
from math import pow
import matplotlib.pyplot as plt
circles = [Point(5*random(),5*random()).buffer(2) for i in range(6)]


def getarea(shapes):
    shape = shapes[0]
    for s in shapes:
        shape = shape.intersection(s)
    return shape.area
#getarea(cirles)

def inclusion_exclusion_value(shapes):
    value = 0
    values =[]
    for i in range(1,len(shapes)):
        combos = list(itertools.combinations(shapes,i))
        print("combos length:",len(combos))
        term =0
        for combo in combos:
            term += getarea(combo)
        print("combo value:",term)
        value +=pow(-1,i+1)*term
        values.append(value)
    print(values)
    #plt.plot(values)
    return value

def inclusion_exclusion_diff(shapes):
    value = 0
    values =[]
    shapes_n_1 = shapes[0:-1]
    for i in range(1,len(shapes)):
        combos_n = list(itertools.combinations(shapes,i))
        combos_n_1 = list(itertools.combinations(shapes_n_1,i))
        print("len combos_n: ",len(combos_n))
        print("len combos_n_1: ",len(combos_n_1))
        term =0
        for combo in combos_n:
            term += getarea(combo)
        for combo in combos_n_1:
            term -= getarea(combo)
        print("combo value:",term)
        value +=pow(-1,i+1)*term
        values.append(value)
    print(values)
    plt.plot(values)
    plt.show()
    return value

def inclusion_exclusion_diff_tail(s,shapes):
    value = 0
    values =[]
    for i in range(1,len(shapes)):
        combos_n = list(itertools.combinations(shapes,i))
        term = 0
        for combo in combos_n:
            extended_combo = list(combo)
            extended_combo.append(s)
            term += getarea(extended_combo)
        value += pow(-1,i+1)*term

def get_total_area(shapes):
    shape = shapes[0]
    for s in shapes:
        shape = shape.union(s)
    return shape.area
    
print("I/E  :",inclusion_exclusion_value(circles))
print("Union:",get_total_area(circles))
lesscircles =circles[0:4] 
print("I/E diff :",inclusion_exclusion_diff(lesscircles))

print("I/E diff :",inclusion_exclusion_diff(circles))

plt.show()
