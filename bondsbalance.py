import numpy as np
import pandas as pd
import cvxopt
import markovitzlagrange as mv


#F: a eru vigtir nuverandi safns, returns eru medalavoxtun hvers brefs, rc er upprunaleg avoxtunarkrafa og cov er covariance fylki brefanna
#E: k er annadhvort a eda b eftir tvi hvort breyta tarf safni eda ekki
#N: new_port = rebalance_check(a,returns,cov,rc)
def rebalance_check(a,returns,cov,rc):
	a_ret = np.sqrt(np.dot(np.dot(a.T,cov),a))
	a_std = np.dot(a.T,returns)
	b = mv.noshort_alloc(returns, cov, rc)
	k = a
	print(b['status'])
	if b['status'] == 'optimal':
		b = np.array(b['x'])
		b_ret = np.sqrt(np.dot(np.dot(b.T,cov),b))
		b_std = np.dot(b.T,returns)
		a_sharp = a_ret/a_std
		b_sharp = b_ret/b_std
		check = a_sharp/b_sharp
		if (check < 0.95):
			k = b
		elif (check > 1.05):
			k = b
	return k


	