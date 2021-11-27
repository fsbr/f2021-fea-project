import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial

mono = pd.read_csv("monon.csv")
matrix = pd.read_csv("matrixn.csv")

monopoly, monores = Polynomial.fit(mono["n"], mono["time"], 2, full = True)
matrixpoly, matrixres = Polynomial.fit(matrix["n"], matrix["time"], 2, full = True)
print("matrixpoly",matrixpoly)
 
x = np.linspace(0,25,500)
plt.plot(mono["n"], mono["time"],label="mono")
plt.plot(x,monopoly(x))
plt.plot(x,matrixpoly(x))
plt.plot(matrix["n"], matrix["time"],label="matrix")
plt.title("Algorithm Run Times vs Shape Function Order")
plt.xlabel("Shape Function Order")
#plt.yscale("log")
plt.grid()
plt.legend()
plt.ylabel("runtime (s)")
plt.show()
