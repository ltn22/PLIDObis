import numpy as np
import matplotlib.pyplot as plt

dat_csv = np.loadtxt('courbe_1.csv',delimiter = ',')

fig = plt.figure(figsize=(8,5))
#plt.plot(x_a,y_a,'o-')
plt.plot(dat_csv[0],dat_csv[1],'+')
plt.xlabel('Temps')
plt.ylabel('Température')
plt.title("Courbe de température ")  
plt.show()

