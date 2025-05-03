#!/usr/bin/env python3
import numpy as np

'''
Module Description:
C. Wibisono
Portfolio Management Module:
Formalisms are based on Chapter 3 M.Capinski and T.Zastawniak
Mathematics for Finance
'''

def cov_construct(rho, sigma):
	'''
	Construct Covariant Matrix between a pair of securities
	Function Argument(s):
	rho: list(2D arr) correlation between returns
	sigma: risk for each return
	Return:
	C: list(2D arr) covariant matrix between returns
	'''
	dim = len(sigma)
	C = []
	for k1 in range(dim):
		C.append([])
		for k2 in range(dim):
			C[k1].append(0)

	for k1 in range(dim):
		for k2 in range(dim):
			C[k1][k2] = rho[k1][k2]*sigma[k1]*sigma[k2]

	return C

def matinv(C):
	mat = np.array(C)
	#det = np.linalg.det(mat)
	mat_inv = np.linalg.inv(mat)
	return mat_inv


def mvp(C):
	'''
	Minimum Variance Portfolio:
	C. Wibisono
	04/29 '25
	Function Argument(s):
	C: covariance matrix between returns
	Return:
	w: arr(1D returns of portfolio weight)
	'''
	Cinv = matinv(C)
	dim = len(Cinv)
	u = []
	temp_a = [] #uC^-1
	for k in range(dim):
		u.append(1)
		temp_a.append(0)
	
	denum = 0 #uC^-1u^T
	for k0 in range(dim):
		for k1 in range(dim):
			temp_a[k0] = temp_a[k0] + (u[k1])*(Cinv[k1][k0])		
		denum = denum + temp_a[k0]

	weight_mvp = []
	for k3 in range(dim):
		weight_mvp.append(temp_a[k3]/denum)

	return weight_mvp

def value(m,C,w):
	'''
	Compute the expected return and risk given a weight for the portfolio:
	C. Wibisono
	04/29 '25
	Function Argument(s):
	m: list (1D arr of expected returns for each security)
	C: list (2D arr consisting of covariance matrix between a pair of securities)
	w: weight of each portfolio
	Return(s):
	mu_v: (float) expected_return
	sigma_v: (float) risk
	'''

	dim = len(m)
	mu_v = 0
	sigma_v = 0
	for k in range(dim):
		mu_v = mu_v + m[k]*w[k]

	wC = []
	for k in range(dim):
		wC.append(0)

	for k0 in range(dim):
		for k1 in range(dim):
			wC[k0] = wC[k0] +(w[k1]*(C[k1][k0]))
		sigma_v = sigma_v + wC[k0]*w[k0]

	sigma_v = (sigma_v)**0.5

	return mu_v, sigma_v

def eff_frontier(m,C,mu_v):
	'''
	Compute the weight associated with the minimum variance line for a given expected return mu_v:
	C. Wibisono
	04/29 '25
	Function Argument(s):
	m: list (1D arr of expected return for each security)
	C: list (2D arr consisting of covariance matrix between a pair of securities)
	mu_v: (float) expected return
	Return(s):
	w_eff: weight associated with the minimum variance line
	sigma_v: the lowest risk for a given expected return mu_v
	'''
	M=[[0,0],[0,0]]
	Cinv = matinv(C)
	dim = len(m)
	u = []
	w_eff = []
	mCinv = []
	uCinv = []
	for q in range(dim):
		u.append(1)
		mCinv.append(0)
		uCinv.append(0)

	for k0 in range(dim):
		for k1 in range(dim):
			mCinv[k0] = mCinv[k0] + (m[k1]*Cinv[k1][k0])
			uCinv[k0] = uCinv[k0] + (u[k1]*Cinv[k1][k0])

		M[0][0] = M[0][0] + mCinv[k0]*m[k0]
		M[0][1] = M[0][1] + uCinv[k0]*m[k0]
		M[1][0] = M[1][0] + mCinv[k0]*u[k0]
		M[1][1] = M[1][1] + uCinv[k0]*u[k0]

	Minv = matinv(M)
	tempb = [mu_v, 1]

	mult_lambda =[0,0]
	for k0 in range(2):
		for k1 in range(2):
			mult_lambda[k0] = mult_lambda[k0] +(2*Minv[k0][k1]*tempb[k1])  						
	
	for k in range(dim):
		temp = 0.5*(mult_lambda[0]*mCinv[k] + mult_lambda[1]*uCinv[k])
		w_eff.append(temp)


	mu_b, sigma_v = value(m,C,w_eff)

	return w_eff, sigma_v
	
def eff_frontier_vector(m,C):
	'''
	The weigth associated with the minimum variance line can be expressed as linear combination of expected return.
	Compute the a and b vectors with the minimum variance line:
	C. Wibisono
	04/29 '25
	Function Argument(s):
	m: list (1D arr of expected return for each security)
	C: list (2D arr consisting of covariance matrix between a pair of securities)
	Return(s):
	a: list (1D arr)
	b: list (1D arr)
	'''
	M=[[0,0],[0,0]]
	Cinv = matinv(C)
	dim = len(m)
	u = []
	w_eff = []
	mCinv = []
	uCinv = []
	for q in range(dim):
		u.append(1)
		mCinv.append(0)
		uCinv.append(0)

	for k0 in range(dim):
		for k1 in range(dim):
			mCinv[k0] = mCinv[k0] + (m[k1]*Cinv[k1][k0])
			uCinv[k0] = uCinv[k0] + (u[k1]*Cinv[k1][k0])

		M[0][0] = M[0][0] + mCinv[k0]*m[k0]
		M[0][1] = M[0][1] + uCinv[k0]*m[k0]
		M[1][0] = M[1][0] + mCinv[k0]*u[k0]
		M[1][1] = M[1][1] + uCinv[k0]*u[k0]

	Minv = matinv(M)


	a = []
	b = []
	for k in range(dim):
		temp_a = Minv[0][0]*mCinv[k] + Minv[1][0]*uCinv[k]
		temp_b = Minv[0][1]*mCinv[k] + Minv[1][1]*uCinv[k]
		a.append(temp_a)
		b.append(temp_b)	

	return a, b


def eff_frontier_mp(m,C,R):
	'''
	Compute the weight associated with the market portfolio along the capital market line (CML).
	C. Wibisono
	04/30 '25
	Function Argument(s):
	m: list (1D arr of expected return for each security)
	C: list (2D arr consisting of covariance matrix between a pair of securities)
	R: (float) return of a risk-free security
	Return(s):
	w_eff_mp: weight associated with the market portfolio
	mu_v: the expected return of the market portfolio
	sigma_v: the risk of the market portfolio
	'''
	Cinv = matinv(C)
	dim = len(m)
	u = []
	w_eff_mp = []
	mCinv = []
	uCinv = []
	denum = 0
	for q in range(dim):
		u.append(1)
		mCinv.append(0)
		uCinv.append(0)

	for k0 in range(dim):
		for k1 in range(dim):
			mCinv[k0] = mCinv[k0] + (m[k1]*Cinv[k1][k0])
			uCinv[k0] = uCinv[k0] + (u[k1]*Cinv[k1][k0])
		a = mCinv[k0]
		b = R*uCinv[k0]
		temp = a - b
		denum = denum + temp 

	for k in range(dim):
		temp_2 = (mCinv[k] -R*uCinv[k])/denum
		w_eff_mp.append(temp_2)

	


	mu_b, sigma_b = value(m,C,w_eff_mp)

	return w_eff_mp, mu_b, sigma_b

def minline(a,b,mu_v):
	'''
	Compute the weight associated with the minimum variance line given vectors a and b.
	C. Wibisono
	05/01 '25
	Function Argument(s):
	a: list(1D arr of vector a obtained from minimizing the variance line)
	b: list(1D arr of vector b obtained from minimizing the variance line)
	mu_v: (float) expected return
	Return:
	w: list (1D arr of weight factor of the portfolio lies along the minimum variance line)
	'''
	w = []
	dim = len(a)
	for k in range(dim):
		w.append(mu_v*a[k]+b[k])

	return w

def frac_rf(sigma_mp, sigma_p, R):
	'''
	Compute the fraction (weight) associated with risk-free security in a portfolio
	consisting of a risk free and risky assets along the Capital Market Line (CML).
	C. Wibisono
	05/03 '25
	Function Argument(s):
	sigma_mp: (float) risk associated with market portfolio
	sigma_p: (float) desired risk
	R: (float) return rate associated with a risk-free security
	Return:
	frac: (float) fraction of a risk-free security to be invested in a portfolio.
	'''
	#fraction of risky securities: (note that when the desired risk at the market portfolio,
	#which is the tangent line of the CML line that intersect with the minimum variance line 
	#of risky securities, the fraction of a risk-free is zero).
	x = sigma_p/sigma_mp

	#fraction of a risk-free security:
	frac = 1 - x
	
	return frac
