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

