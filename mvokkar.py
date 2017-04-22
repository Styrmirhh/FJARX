import numpy as np
import pandas as pd


# def mvokkar(Close_Prices):
# 	bla = np.array(Close_Prices) # Setur close_price i fylki
# 	P = np.zeros(len(bla))
# 	for i in range(0, len(bla)):
# 		P[i]=(bla[i].sum())
# 	w = np.zeros([len(bla),5])
# 	x = np.zeros([len(bla),5])
# 	for j in range(0, len(bla)):
# 		w[j,...]=(bla[j]/P[j])
# 		for k in range(0, len(w[j])):
# 			x[(j,k)]=((w[(j,k)]*bla[(j,k)]))
# 	piff = x.sum(1)
# 	return piff

#Calculates an index for bond prices by sum(p[i]*p[i]/P) where P is sum(p[i])
#F:Close_Prices is a pandas dataframe
#E:index is a 1-dimensional dataframe, i.e. Series
#N: k = mvokkar(Close_Prices)
def mvokkar(Close_Prices):
	price_sum = Close_Prices.sum(axis = 1)
	price_percent = pd.DataFrame()
	for col in Close_Prices:
		price_percent[col] = Close_Prices[col].div(price_sum)
	price_percent_mult = pd.DataFrame()
	for col in Close_Prices:
		price_percent_mult[col] = Close_Prices[col].mul(price_percent[col])
	index = pd.DataFrame()
	index['Ix'] = price_percent_mult.sum(axis=1)
	return index
