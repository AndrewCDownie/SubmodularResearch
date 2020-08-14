from math import gamma
import math
import matplotlib.pyplot as plt
from modules.pairwisecoverage import area

# Function that computes the expected distance to the nth furthest point sampled unifomly over cirle of radius R
def expectiation(n,N,R):
    return R*(gamma(n + 1/2)/gamma(n))/(gamma(N+1+1/2)/gamma(N+1))

def compute_weight(d,a,b):
    return area({"x":0,"y":0,"r":math.sqrt(a/math.pi)},{"x":d,"y":0,"r":math.sqrt(b/math.pi)})/a


a = 400 # area of smaller disk
b = 500 # area of largest disk

N = 16 # number of agents
R = 50 # Radius being unifomly sampled over

weight_sum = 0

max_weight = compute_weight(expectiation(1,N,R),a,b) #Expected Weight of closest element

weights = []

# Loop over the rest of the selected elements from closest to furthest and then compute there sum
for i in range(2,N):
    weights.append(compute_weight(expectiation(i,N,R),a,b))
    weight_sum += weights[-1]


epsilion = weight_sum/(1-max_weight) #calcualate the ratio between the closest and the rest of the sum

print("weight sum: ",weight_sum) 
print("max_weight",max_weight)
print("must be less than ",1-max_weight)

print("eps",epsilion)
gamma = epsilion/(1-epsilion) #compute Gamma
print("1+Gamma",1+gamma) 


l = [w for w in weights if w >0] # compute the neighbor hood 
print("size of L:",len(l))
#plt.show()
