import bondspanda
import numpy as np
import markovitzlagrange as mv
import numpy as np
import markovitzlagrange as mv
import pyfront as pf
import seaborn as sns


def mvokkar(Close_Prices)
	bla = np.array(Close_Prices) # Setur close_price i fylki
	P = np.zeros(len(bla))
	for i in range(0, len(bla)):
		P[i]=(bla[i].sum())
	print(P)
	w = np.zeros([len(bla),5])
	x = np.zeros([len(bla),5])
	for j in range(0, len(bla)):
		w[j,...]=(bla[j]/P[j])
		print(w[j,...])
		for k in range(0, len(w[j])):
			print(w[(j,k)])
			x[(j,k)]=((w[(j,k)]*bla[(j,k)]))
			print(x[(j,k)])
	piff = x.sum(1)
	return piff