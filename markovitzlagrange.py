import numpy as np
import cvxopt as cvx


#N: weight = walloc(r,C,rc)
#F: r inniheldur meanreturns, C er covariance-fylki, rc er ávöxtunarkrafan
#E: w skilar út vigtum skv skorðum


def walloc(r,C,rc):
	k = C.shape
	e=np.ones(k[1])
	Cinv=np.linalg.inv(C)
	etr=np.transpose(e)
	rtr=np.transpose(r)

	u1a=np.dot(Cinv,e)
	u1b=np.dot(np.dot(rtr,Cinv),r)
	u1c=rc*np.dot(np.dot(etr,Cinv),r)
	u1=u1a*(u1b - u1c)

	u2a=np.dot(Cinv,r)
	u2b=np.dot(np.dot(rtr,Cinv),e)
	u2c=rc*np.dot(np.dot(etr,Cinv),e)
	u2=u2a*(u2b-u2c)

	l1a=np.dot(np.dot(etr,Cinv),e)
	l1b=np.dot(np.dot(rtr,Cinv),r)
	l1=l1a*l1b

	l2a=np.dot(np.dot(etr,Cinv),r)
	l2b=np.dot(np.dot(rtr,Cinv),e)
	l2=l2a*l2b

	u=u1-u2
	l=l1-l2
	w=u/l
	return w


def noshort_exposurelim_alloc(r,C,rc,exlim):
	n = C.shape[0]
	C = cvx.matrix(C)
	#print(C)
	P = 2*C
	q = cvx.matrix(0.0, (n,1))
	#print(q)
	G = cvx.matrix(0.0, (2*n,n))
	G[cvx.matrix([0,11,22,33,44])] = -1.0
	G[cvx.matrix([5,16,27,38,49])] = 1.0
	#print(G)
	h = cvx.matrix(0.0, (2*n,1))
	h[n::] = exlim
	#print(h)
	A = cvx.matrix(1.0, (2,n))
	A[0,:] = r
	b = cvx.matrix(1.0, (2,1))
	b[0,0] = rc
	sol= cvx.solvers.qp(P, q,G,h,A,b)
	return sol



def short_exposurelim_alloc(r,C,rc,exlim):
	n = C.shape[0]
	C = cvx.matrix(C)
	P = 2*C
	q = cvx.matrix(0.0, (n,1))
	#print(q)
	G = cvx.matrix(0.0, (n,n))
	G[::n+1] = 1.0
	#print(G)
	h = cvx.matrix(exlim, (n,1))
	#print(h)
	A = cvx.matrix(1.0, (2,n))
	A[0,:] = r
	b = cvx.matrix(1.0, (2,1))
	b[0,0] = rc
	sol= cvx.solvers.qp(P, q,G,h,A,b)
	return sol



def noshort_alloc(r,C,rc):
	n = C.shape[0]
	C = cvx.matrix(C)
	P = 2*C
	q = cvx.matrix(0.0, (n,1))
	#print(q)
	G = cvx.matrix(0.0, (n,n))
	G[::n+1] = -1.0
	#print(G)
	h = cvx.matrix(0.0, (n,1))
	#print(h)
	A = cvx.matrix(1.0, (2,n))
	A[0,:] = r
	b = cvx.matrix(1.0, (2,1))
	b[0,0] = rc
	sol= cvx.solvers.qp(P, q,G,h,A,b)
	return sol

