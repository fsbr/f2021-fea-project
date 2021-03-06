# this code generates plots for a higher order shape functions in 
# what element types 1D bar
import numpy as np
from numpy.polynomial import Polynomial
#import np.polynomial 
import matplotlib.pyplot as plt
import time

def makequadfigure():
    x = np.linspace(0,1,500)
    # plots from hutton
    L = 1
    N1 = 1 - (3/L)*x + (2/L**2)*x**2
    N2 = (4*x/L)*(1 - x/L)
    N3 = (x/L)*(2*x/L -1)
    plt.plot(x,N1, label = "N1")
    plt.plot(x,N2, label = "N2")
    plt.plot(x,N3, label = "N3")
    plt.title("Shape Function Roots (Hutton)")
    plt.xlabel("x (as a fraction of L)")
    plt.ylabel("Shape Function Value")
    plt.legend()
    plt.grid()
    plt.show()

def computeShapeFunctionsMONO(N = 3):
    # given a number N, compute N+1 shape functions
    L = 1 
    nodePoints = np.linspace(0, 1, N+1)
    #print("nodePoints", nodePoints[1])
    # gather all but the last node point
    Ci = []
    for i,y in enumerate(nodePoints):
        si = nodePoints[i]
        nodePointsInterest = [x for j,x in enumerate(nodePoints) if j!=i]
        prod = 1

        # looks numerically not stable
        for sj in nodePointsInterest:
            prod *= (si - sj)
        C = (1/prod)
        Ci.append(C)
        #print(C)
        x = np.linspace(0,1,500)

        # i bet this root finding is what takes all the time
        p = C*Polynomial.fromroots(nodePointsInterest)
        plt.plot(x,p(x), label="%s-th shape function"%(i+1))
        print("polynomial", p)
    #plt.legend()
    plt.grid()
    plt.title("Shape Functions vs. Normalized Length (Monomial Method)")
    plt.show()
    idx = np.arange(len(Ci))
    plt.scatter(idx, Ci, marker="x")
    plt.title("Constants vs. Index")
    #plt.yscale('log')
    plt.show()

def computeShapeFunctionMATRIX(N=3):
    nodePoints = np.linspace(0, 1, N+1)
    bigMatrix = np.zeros((N+1, N+1))
    x = np.linspace(0,1,500)
    #print("BIG MATRIX", bigMatrix)
    counter = 0
    for node in nodePoints:
        polyList = np.ones((N+1))
        p = Polynomial(polyList)
        matrixRow = []
        for i in range(len(p.coef)):
            #element = p.coef[i]*(node**(i))
            element = p.coef[i]*np.power(node,i)
            matrixRow.append(element)
        #print(matrixRow)
        for i,element in enumerate(matrixRow):
            bigMatrix[counter][i] = element 
        counter+=1
    #print(bigMatrix)

    invBigMatrix = np.linalg.inv(bigMatrix)
    w,v = np.linalg.eig(invBigMatrix)
    print("eigenstuff", w)
    #print("inverted", invBigMatrix)
    shapeFunctions = invBigMatrix

    
    for j in range(N+1):
        coefList = []
        for i in range(N+1):
            #print(invBigMatrix[j][i])
            coefList.append(invBigMatrix[i][j])
        p = Polynomial(coefList)
        plt.plot(x,p(x))
    plt.title("Shape Functions vs. Normalized Length (Matrix Method)")
    plt.grid()
    plt.show()

def perturb1(N = 20):
    count = 0
    while count < 2:
        if count == 0:
            e = 0.0
            text = "unperturbed roots of 20th order poly"
        else:
            e = np.power(2.0,-23.0)
            #e = 1.0e-9
            text = "perturbed by 2^-23"
        w =  [1, -210 +e , 20615 , -1256850, + 53327946, 
            -1672280820, 40171771630 , -756111184500 , 
             11310276995381, -135585182899530 , 
             1307535010540395, -10142299865511450, 
             63030812099294896, -311333643161390640, 
             1206647803780373360, -3599979517947607200,
             8037811822645051776, -12870931245150988800,
             13803759753640704000, -8752948036761600000,
             2432902008176640000]
        w.reverse()
        w = [ float(i) for i in w]
        print("w", w)
        p = Polynomial(w)
        print("p",p)
        print("roots", p.roots())
        x = [ realpart for realpart in p.roots().real]
        y = [ imagpart for imagpart in p.roots().imag]
        plt.scatter(x,y, label = text)
        count += 1
    plt.legend()
    plt.grid()
    plt.xlabel("Real Part of Solution")
    plt.ylabel("Imag Part of Solution")
    plt.title("Perturbed Root Locations for 20th Order Wilkinson Polynomial")
    plt.show()

def run_benchmarks():
    case = 0
    while case <2:
        if case == 0:
            f = open("benchmarkMONO2.csv", "w")
        else:
            f = open("benchmarkMATRIX2.csv", "w")
            
        #makequadfigure()
        n = 10 
        for i in range(1000):
            t_start = time.time()
            for j in range(100):
                if case == 0:
                    computeShapeFunctionsMONO(n)
                else:
                    #computeShapeFucntionMATRIX(n)
                    computeShapeFunctionMATRIX(n)
            t_end = time.time()
            test_duration = t_end - t_start
            f.write("%s,\n"%(test_duration))

        f.close()
        case+=1

def benchmark2():
    i = 0
    bigN = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
    while i < 2:
        if i == 0:
            f = open("monon.csv","w")
        else:
            f = open("matrixn.csv","w")
        f.write("n,time\n")
        for n in bigN:
            t_start = time.time()
            for x in range(1000):
                if i == 0:
                    computeShapeFunctionsMONO(n)
                else:
                    computeShapeFunctionMATRIX(n)
            t_end = time.time()
            test_duration = t_end - t_start
            f.write("%s,%s\n"%(n,test_duration))
        i+=1
        f.close()



def plot_hist():
    import pandas as pd
    mono = pd.read_csv("benchmarkMONO2.csv")
    matrix = pd.read_csv("benchmarkMATRIX2.csv")
    n_bins = 20 
    plt.hist(mono["data"],bins=n_bins, label="monomial method")
    plt.hist(matrix["data"],bins=n_bins, label="matrix method")
    plt.xscale('log')
    plt.title("Benchmarks of the Monomial and Matrix Algorithms")
    plt.legend()
    plt.grid()
    plt.xlabel("time (sec)")
    plt.ylabel("n")
    plt.show()
    print("mono mean", mono.mean())
    print("mono std", mono.std())
    print("matrix mean", matrix.mean())
    print("matrix std", matrix.std())

def sixtyNine():
    n =69 
    # i want to know what hte 69th order shape function is
    a = np.array([1,1], dtype = np.float64)
    for i in range(n):
        b = np.convolve(a,np.array([1,1], dtype = np.float64))
        a = b
        print("%s  || %s"%(i+2,b))
    
    for j in range(n):
        for i in range(j):
            #print(i)
            i*=i/j
            b = i
        try:
            print("coeff", 1/b)
        except: pass
    return a,b

if __name__ == "__main__":
    #run_benchmarks()
    #plot_hist()
    n = 20 
    #r = 0
    #computeShapeFunctionsMONO(n)
    #computeShapeFunctionMATRIX(n)
    #benchmark2()
    perturb1()
    #a, b = sixtyNine()
    #print(1/b)
    #print(a)
