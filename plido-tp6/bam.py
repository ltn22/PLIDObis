import numpy as np
import matplotlib.pyplot as plt


fig, ax = plt.subplots(4, 2)

X = [i for i in range(0,1000)]

Y = [i for i in range(0, 3)]

Y[0] = [5 for i in range(0, 1000)] # constant
Y[1] = [i/100.0 for i in range(0,1000)] # linear
Y[2] = [i%10 for i in range(0, 1000)]

for i in range(0, 3):
    name = 'courbe_{}.csv'.format(i+1)
    dat_csv = np.loadtxt(name, delimiter = ',')

    ax[i, 0].plot(X, Y[i],'+')
    ax[i, 1].boxplot (Y[i])
plt.show()
