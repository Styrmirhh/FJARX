import numpy as np
import cvxopt as cvx



def noshort_alloc(r,C,rc):
	P = C
	q = np.zeros(P.shape[0])