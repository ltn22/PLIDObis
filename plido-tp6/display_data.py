import numpy as np
import matplotlib.pyplot as plt

sigma = 2      # Niveau de bruit de mesure des capteurs (écart-type)
pente = 5       # Vitesse d'évolution de la métrique (par période)

n = 100         # Nombre de points par période
nb_periodes = 8


# Génération des données
Y = [10+i*pente/n + np.random.normal(0,sigma) for i in range(0, n*nb_periodes)]
# Séparation en périodes
data = [Y[k*n:(k+1)*n] for k in range(nb_periodes)]

# Tracé
fig, ax = plt.subplots(2, 1)
ax[0].plot(Y,'+')
ax[1].boxplot (data)

# Détection
if np.quantile(data[0],.75)<np.quantile(data[-1],.25):
    print('=> augmentation détectée entre la première et la dernière période')
elif np.quantile(data[-1],.75)<np.quantile(data[0],.25):
    print('=> diminution détectée entre la première et la dernière période')
else:
    print('=> pas de changement détecté')
plt.show()
