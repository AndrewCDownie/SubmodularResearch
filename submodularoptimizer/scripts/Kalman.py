#Kalman Filter Sensor Selection
import numpy as np
from numpy.linalg import inv


 # vector which is the diagonal of V

# print(A)
# print(C)
# print(V)

X = np.zeros((4,0))

x = np.matrix([[0],[1],[0],[1]])




# for i in range(T):
#     x = A.dot(x)
#     print(x)
#     X = np.hstack([X,x])

#DEAL WITH NEGATIVES
# Do do so make a class for the objective function and then normalize based on the sensor with the worst error
# print(X)

def measure(x,H,V,m,n):
    y = H.dot(x) + np.random.multivariate_normal(np.zeros(m),np.diag(V),1).T
    return y

class KalmanSensors:
    def __init__(self,m,n,d):
        self.C = np.random.rand(m,d)
        #self.C = np.random.rand((m,d))
        self.V = 10*np.random.rand(m)
        self.Pk_k_1 = np.diag(np.ones(d))
        worst_sensor = min(range(m), key = lambda x:-np.trace(self.get_covarience([x])))
        self.bias = self.get_bias()
        print(self.bias)
        print("bias",self.bias)

    def get_bias(self):
        return (1/self.V).sum()

    def get_covarience(self,sensors):
        S = np.array(sorted(sensors))
        Vs = self.V[S]
        Hs = self.C[S]
        return inv(inv(self.Pk_k_1)+ Hs.T.dot(inv(np.diag(Vs))).dot(Hs))

    def objective(self,S):
        return -np.trace(self.get_covarience(S)) + self.bias

    def error(self,S):
        return np.trace(self.get_covarience(S))

    def marginal(self,x,S):
        if len(S) ==0:
            return self.objective([x])
        return self.objective(S+[x]) - self.objective(S) 

    def pairwise_lowerbound(self,x,S):
        fx = self.objective([x])
        print("fx",fx)
        print()
        lb = fx
        for s in S:
            print("print f(x)+f(y)-f(x,y)", fx + self.objective([s]) - self.objective([s,x]))
            print("f(y)", self.objective([s]))
            print("f(x,y)",self.objective([s,x]))
            lb -= fx-self.marginal(x, [s])
        return lb


if __name__ == '__main__':
    d = 100
    T = 10
    m = 100
    n = 4
    k = 2
    KalmanS = KalmanSensors(m,n,d)

    x = 0
    S = list(range(1,10))
    print(S)
    print("marginal",KalmanS.marginal(x,S))
    print(S)
    print("pairwise marginal",KalmanS.pairwise_lowerbound(x,S))
    print(S)
    #System Model
    A = np.matrix([[1,1,0,0],
                    [0,1,0,0],
                    [0,0,1,1],
                    [0,0,0,1]])