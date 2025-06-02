#!/usr/bin/env python3
import math
import random
from . import binomial as bo

'''
Module Description:
Continuous Time Model
C. Wibisono
Formalisms are based on Chapter 8 M. Capinski and T. Zastawniak
Mathematics for Finance
'''

def return_h(mu, sigma, T, N):
	'''
	Compute single step returns:
	C. Wibisono
	05/28 '25
	Function Argument(s):
	mu: (float) expected logarithmic return of risky security per unit time
	sigma: (float) volatility of the risky security
	T: (int) time measured in years
	N: (int) number of steps
	Return(s):
	U: (float) the rate of the return if the risky security price goes up
	D: (float) the rate of the return if the risky security price goes down
	'''
	
	h = T/N
	U_N = -1 + math.exp(mu*h + sigma*(math.pow(h,0.5)))  
	D_N = -1 + math.exp(mu*h - sigma*(math.pow(h,0.5)))  
	
	return U_N, D_N

def risky_security_binom_price_level(mu, sigma, S_0, T, N, p):
	'''
	Compute the distribution of risky security price at time T based on N-step binomial model.
	C. Wibisono
	05/28 '25
	Function Argument(s):
	mu: (float) expected logarithmic return of risky security per unit time
	sigma: (float) volatility of the risky security
	S_0 : (float) the initial price associated with the risky security
	T: (int) time measured in years
	N: (int) number of steps
	p: (float) the probability of the risky security price to go up.
	Return(s):
	arr: (dictionary consisting of risky security price as key and its probability at time step N as value)
	'''
	arr = {}
	
	#Compute the single step returns:
	U_N, D_N = return_h(mu, sigma, T, N)

	#Node to store the possible risky-security prices:
	s_node = bo.risky_security_binom_price(N, S_0, U_N, D_N)

	#Create nodes container for storing the probability of the possible risky security prices according to the binomial model:
	prob_node = []
	
	#The first element becomes a root of the tree object with probability 1.
	prob_node.append(bo.TreeNode(1))

	#Number of possible nodes created with time step N:
	dim = math.pow(2, N+1) - 1

	#Create nodes consisting of possible risky security probabilities:
	dim_temp = int(math.pow(2, N)) - 1
	for i in range(dim_temp):
		up = prob_node[i].data*(p)
		down = prob_node[i].data*(1-p)
		n_up = bo.TreeNode(up)
		n_down = bo.TreeNode(down)
		prob_node.append(n_up)
		prob_node.append(n_down)
		prob_node[i].add_child(n_up)
		prob_node[i].add_child(n_down)


	low = int(math.pow(2, N)) - 1
	upper = int(math.pow(2, N+1)) - 1

	for i in range(low, upper, 1):
		temp = round(s_node[i].data,5)
		if temp in arr.keys():
			arr[temp] = arr[temp] + prob_node[i].data #some different scenarios can lead to the same risky security prices
		else:
			arr[temp] = prob_node[i].data


	return arr

def normal(x, mu, sigma):
	'''
	Normal Distribution Function:
	Function Argument:
	mu: (float) mean/centroid.
	sigma: (float) standard deviation.
	Return:
	val: value of distribution at x.
	'''

	A = 1./math.pow((2*(math.pi)*(math.pow(sigma,2.))),0.5)
	B = -math.pow((x - mu),2.)/(2*math.pow(sigma,2.))
	C = math.exp(B)
	return A*C

def risky_security_black_scholes_price(mu, sigma, S_0, T):
	'''
	Compute the distribution of the risky security price at time T based on the Black-Scholes Model.
	C. Wibisono
	05/28 '25
	Function Argument(s):
	mu: (float) expected logarithmic return of risky security per unit time
	sigma: (float) volatility of the risky security
	S_0 : (float) the initial price associated with the risky security
	T: (int) time measured in years
	Return(s):
	arr: (dictionary consisting of risky security price (in terms of loge) as key and its probability density for the very infinitesimal timesteps)
	'''

	arr = {}
	mu_b = math.log(S_0) + mu*T
	sample_num = 1000000
	for i in range(sample_num):
		temp = random.gauss(0, T)
		temp_b = mu_b + temp*sigma
		temp_c = round(temp_b, 2)
		if temp_c in arr.keys():
			arr[temp_c] = arr[temp_c] + 1
		else:
			arr[temp_c] = 1

	
	return arr

def eu_call_bound_cdf(S_t, t, T, r, sigma, X):
	'''
	Compute the upper and lower bound for calculating the cumulative distribution function used for 
	calculating the European Call Option from the Black-Scholes Model.
	C. Wibisono
	06/01 '25
	Function Argument(s):
	S_t: (float) the risky security price at time t
	t: (int) the present time in which the asset is evaluated
	T: (int) exercised time.
	r: (float) continuosly compounded risk-free interest rate ---> exp(rt) instead of (1+R)^N where T=N*h
	sigma: (float) volatility of the risky security
	X: (float) strike price.
	Return(s):
	dmax: (float) the upper bound of the cdf
	dmin: (float) the lower bound of the cdf
	'''

	a = math.log(S_t/X)
	b1 = r + 0.5*math.pow(sigma,2.)
	b2 = r - 0.5*math.pow(sigma,2.)
	num1 = a + b1*(T-t)
	num2 = a + b2*(T-t)
	denum = sigma*math.pow(T-t,0.5)

	dmax = num1/denum
	dmin = num2/denum

	return dmax, dmin

def eu_option_bs(S_t, t, T, r, sigma, X):
	'''
	Compute the European Call and Put Options Price at time t with an exercise time T following the Black-Scholes Model.
	C. Wibisono
	06/01 '25
	Function Argument(s):
	S_t: (float) the risky security price at time t
	t: (int) the present time in which the asset is evaluated
	T: (int) exercised time.
	r: (float) continuosly compounded risk-free interest rate ---> exp(rt) instead of (1+R)^N where T=N*h
	sigma: (float) volatility of the risky security
	X: (float) strike price.
	Return(s):
	C_E: (float) European call price at time t.
	P_E: (float) European put price at time t.
	'''
	
	dmax, dmin = eu_call_bound_cdf(S_t, t, T, r, sigma, X)
	dmax = round(dmax,3)
	dmin = round(dmin,3)
	print("dmax:",dmax,"dmin:",dmin)
	x = []
	y = []
	normalize = 0
	for i in range(-3000,3001,1):
		temp = i*0.001
		y_temp = normal(temp,0,1.)
		x.append(temp)
		y.append(y_temp)
		#print("x:",temp,"y:",y_temp)
		normalize = normalize + y_temp
	N_max = 0
	N_min = 0
	dim = len(x)
	for k1 in range(dim):
		if x[k1] <= dmax:
			N_max = N_max + y[k1]
		else:
			break

	for k2 in range(dim):
		if x[k2] <= dmin:
			N_min = N_min + y[k2]
		else:
			break
	
	#Normalize the CDF:
	N_max = N_max/normalize
	N_min = N_min/normalize

	term1 = S_t*N_max
	term2 = X*(math.exp(-r*(T-t)))*N_min
	print("S_t:",S_t,"N_max:",N_max,"term1:", term1)
	print("Contract:",X*math.exp(-r*(T-t)),"N_min:",N_min,"term2:",term2)
	C_E = term1 - term2
	
	N_max_p = 0
	N_min_p = 0
	for k3 in range(dim):
		if x[k3] <= -dmax:
			N_max_p = N_max_p + y[k3]
		else:
			break

	for k4 in range(dim):
		if x[k4] <= dmin:
			N_min_p = N_min_p + y[k4]
		else:
			break
	
	#Normalize the CDF	
	N_max_p = N_max_p/normalize
	N_min_p = N_min_p/normalize

	term1p = X*(math.exp(-r*(T-t)))*N_min_p
	term2p = S_t*N_max_p
	P_E = term1p - term2p
	print("Contract:",X*math.exp(-r*(T-t)),"N_min_p:",N_min_p,"term2:",term1p)
	print("S_t:",S_t,"N_max_put:",N_max_p,"term1:", term2p)
	
	return C_E, P_E

