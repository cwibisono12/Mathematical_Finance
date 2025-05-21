#!/usr/bin/env python3
import numpy as np
from . import contract as co
from . import binomial as bo

'''
Module Description:
Options Pricing Module to prevent arbitrage profit
C. Wibisono
Formalisms are based on Chapter 5 and 6 M. Capinski and T. Zastawniak
Mathematics for Finance
'''

def eu_put_call(r,T,S,X,C_E,P_E):
	'''
	Check whether there is an arbitrage profit for the European call and put options
	with the same strike price X.
	C. Wibisono
	05/18 '25
	Function Argument(s):
	r: risk-free interest rate
	T: exercise time when the asset is purchased or sold
	S: the risky security price at time 0
	X: the strike price at the exercise time
	C_E: European call price
	P_E: European put price
	Return:
	val: (bool) indicates whether arbitrage profit exists
	'''

	a = C_E - P_E
	b = S - X*co.bond(r,0,T)
	if a > b:
		return True
	if a < b:
		return True
	else:
		return False


def eu_put_call_div_cont(r,T,S,X,r_div,C_E,P_E):
	'''
	Check whether there is an arbitrage profit for the European call and put options
	with the same strike price X and dividend paid continously with rate r_div.
	C. Wibisono
	05/18 '25
	Function Argument(s):
	r: risk-free interest rate
	T: exercise time when the asset is purchased or sold
	S: the risky security price at time 0
	X: the strike price at the exercise time
	r_div: the rate of dividend to be paid to the option holder
	C_E: European call price
	P_E: European put price
	Return:
	val: (bool) indicates whether arbitrage profit exists
	'''

	a = C_E - P_E
	b = (S*co.bond(r_div,0,T)) - (X*co.bond(r,0,T))
	if a > b:
		return True
	if a < b:
		return True
	else:
		return False


def eu_put_call_div_disc(r,T,S,X,div_0,C_E,P_E):
	'''
	Check whether there is an arbitrage profit for the European call and put options
	with the same strike price X and dividend paid somewhere between the present and exercise time T
	with an amount div_0.
	C. Wibisono
	05/18 '25
	Function Argument(s):
	r: risk-free interest rate
	T: exercise time when the asset is purchased or sold
	S: the risky security price at time 0
	X: the strike price at the exercise time
	div_0: the amount of dividend to be paid to the option holder
	C_E: European call price
	P_E: European put price
	Return:
	val: (bool) indicates whether arbitrage profit exists
	'''

	a = C_E - P_E
	b = (S - div_0) - (X*co.bond(r,0,T))
	if a > b:
		return True
	if a < b:
		return True
	else:
		return False

def am_put_call(r,T,S,X,C_A,P_A):
	'''
	Check whether there is an arbitrage profit for the American call and put options
	with the same strike price X.
	C. Wibisono
	05/18 '25
	Function Argument(s):
	r: risk-free interest rate
	T: exercise time when the asset is purchased or sold
	S: the risky security price at time 0
	X: the strike price at the exercise time
	C_A: American call price
	P_A: American put price
	Return:
	val: (bool) indicates whether arbitrage profit exists
	'''

	a = C_A - P_A
	b_high = S - X*co.bond(r,0,T)
	b_low = S - X
	if a > b_high:
		return True
	if a < b_low:
		return True
	else:
		return False


def am_put_call_div_cont(r,T,S,X,r_div,C_A,P_A):
	'''
	Check whether there is an arbitrage profit for the American call and put options
	with the same strike price X and the dividend paid continously with the rate r_div.
	C. Wibisono
	05/18 '25
	Function Argument(s):
	r: risk-free interest rate
	T: exercise time when the asset is purchased or sold
	S: the risky security price at time 0
	X: the strike price at the exercise time
	r_div: the rate of the dividend to paid to the option holder
	C_A: American call price
	P_A: American put price
	Return:
	val: (bool) indicates whether arbitrage profit exists
	'''

	a = C_A - P_A
	b_high = S - X*co.bond(r,0,T)
	b_low = S*co.bond(r_div,0,T) - X
	if a > b_high:
		return True
	if a < b_low:
		return True
	else:
		return False


def am_put_call_div_disc(r,T,S,X,div_0,C_A,P_A):
	'''
	Check whether there is an arbitrage profit for the American call and put options
	with the same strike price X and the dividend paid somewhere between the present and the exercise time T
	with an amount div_0
	C. Wibisono
	05/18 '25
	Function Argument(s):
	r: risk-free interest rate
	T: exercise time when the asset is purchased or sold
	S: the risky security price at time 0
	X: the strike price at the exercise time
	div_0: the amount of the dividend to paid to the option holder
	C_A: American call price
	P_A: American put price
	Return:
	val: (bool) indicates whether arbitrage profit exists
	'''

	a = C_A - P_A
	b_high = S - X*co.bond(r,0,T)
	b_low = (S - div_0) - X
	if a > b_high:
		return True
	if a < b_low:
		return True
	else:
		return False

def eu_put_call_bounds(r,T,S,X):
	'''
	Compute the lower and upper bounds associated with the European option prices
	with the strike price X.
	C. Wibisono
	05/18 '25
	Function Argument(s):
	r: risk-free interest rate
	T: exercise time when the asset is purchased or sold
	S: the risky security price at time 0
	X: the strike price at the exercise time
	Return:
	eu_op: (dict) European call and put option prices lower and upper bounds
	'''

	eu_op = {}
	a1 = S - X*co.bond(r,0,T)
	if a1 > 0:
		C_E_low = a1
	else:
		C_E_low = 0 
	C_E_up = S

	eu_op['C_E'] = (C_E_low, C_E_up)

	a2 = -S + X*co.bond(r,0,T)
	b = X*co.bond(r,0,T)
	if a2 > 0:
		P_E_low = a2
	else:
		P_E_low = 0
	P_E_up = b

	eu_op['P_E'] = (P_E_low, P_E_up)
	
	return eu_op


def eu_put_call_bounds_div_disc(r,T,S,X,div_0):
	'''
	Compute the lower and upper bounds associated with the European option prices
	with the strike price X and the dividend paid somewhere 
	between the present and exercise time T with an amount div_0.
	C. Wibisono
	05/18 '25
	Function Argument(s):
	r: risk-free interest rate
	T: exercise time when the asset is purchased or sold
	S: the risky security price at time 0
	X: the strike price at the exercise time
	div_0: the amount of the dividend paid to the option holder
	Return:
	eu_op: (dict) European call and put option prices lower and upper bounds
	'''

	eu_op = {}
	a1 = S - div_0 - X*co.bond(r,0,T)
	if a1 > 0:
		C_E_low = a1
	else:
		C_E_low = 0 
	C_E_up = S - div_0

	eu_op['C_E'] = (C_E_low, C_E_up)

	a2 = -S + div_0 + X*co.bond(r,0,T)
	b = X*co.bond(r,0,T)
	if a2 > 0:
		P_E_low = a2
	else:
		P_E_low = 0
	P_E_up = b

	eu_op['P_E'] = (P_E_low, P_E_up)
	
	return eu_op
	

def am_put_call_bounds(r,T,S,X):
	'''
	Compute the lower and upper bounds associated with the American option prices
	with the strike price X.
	C. Wibisono
	05/18 '25
	Function Argument(s):
	r: risk-free interest rate
	T: exercise time when the asset is purchased or sold
	S: the risky security price at time 0
	X: the strike price at the exercise time
	Return:
	am_op: (dict) American call and put option prices lower and upper bounds
	'''

	am_op = {}
	a1 = [0, S - X*co.bond(r,0,T)]
	C_A_low = max(a1)
	C_A_up = S 

	am_op['C_A'] = (C_A_low, C_A_up)

	a2 =[0, -S + X]
	b = X
	P_A_low = max(a2)
	P_A_up = b


	am_op['P_A'] = (P_A_low, P_A_up)
	
	return am_op

def am_put_call_bounds_div_disc(r,T,S,X,div_0):
	'''
	Compute the lower and upper bounds associated with the American option prices
	with the strike price X and the dividend paid somewhere 
	between the present and exercise time T with an amount div_0.
	C. Wibisono
	05/18 '25
	Function Argument(s):
	r: risk-free interest rate
	T: exercise time when the asset is purchased or sold
	S: the risky security price at time 0
	X: the strike price at the exercise time
	div_0: the amount of the dividend paid to the option holder
	Return:
	am_op: (dict) American call and put option prices lower and upper bounds
	'''

	am_op = {}
	a1 = [0, S - div_0 - X*co.bond(r,0,T), S-X]
	C_A_low = max(a1)
	C_A_up = S 

	am_op['C_A'] = (C_A_low, C_A_up)

	a2 =[0, -S + div_0 + X*co.bond(r,0,T), -S + X]
	b = X
	P_A_low = max(a2)
	P_A_up = b


	am_op['P_A'] = (P_A_low, P_A_up)
	
	return am_op


def eu_option_binom_disc(R, U, D, S, X, N):
	'''
	Compute the European call and put option prices based on
	Cox-Ross-Rubinstein Formula following the binomial model exercised after N time step.
	C. Wibisono
	05/19 '25
	Function Argument(s):
	R: (float) the rate of risk-free security as a form of money market account 
	U: (float) the rate of return if the risky security price goes up
	D: (float) the rate of return if the risky security price goes down
	S: (float) the risky security price at time 0
	X: (float) the strike price at the exercise time
	N: (int) the amount of time steps to exercise the asset
	Return:
	C_E: (float) the european call option price
	P_E: (float) the european put option price
	'''

	m = bo.m_order(S, U, D, N, X)
	q = ((1+ U)/(1+R))*bo.p_star(R, U, D)
	
	c1 = S*(1-bo.cbd(m-1, N, q))
	c2 = (X/((1+R)**N))*(1-bo.cbd(m-1,N,bo.p_star(R,U,D)))
	C_E = c1 - c2

	p1 = -S*bo.cbd(m-1,N,q)
	p2 = (X/((1+R)**N))*bo.cbd(m-1,N,bo.p_star(R,U,D))
	P_E = p1 + p2

	return C_E, P_E

def am_option_binom_disc(R, U, D, S, X, N):
	'''
	Compute the American call and put option prices following the binomial model with expiray time N.
	Note that the option can be exercised somewhere between present (time 0) up to expiry time N.
	C. Wibisono
	05/20 '25
	Function Argument(s):
	R: (float) the rate of risk-free security as a form of money market account
	U: (float) the rate of return if the risky security price goes up
	D: (float) the rate of return if the risky security price goes down
	S: (float) the risky security price at time 0
	X: (float) the strike price
	N: (int) the amount of time when the option is expired (maximum amount of time that the option can be exercised)
	Return:
	C_A: (float) the american call option price
	P_A: (list of TreeNode objects) the american put option prices for each time step up to expiry time N
	'''
	
	#With no dividend is paid, the american call option will be equal to european call option price.
	C_A, P_E = eu_option_binom_disc(R, U, D, S, X, N)

	#Compute the American Put Option Price:
	#===================================================================
	#Risk-Neutral Probability:
	pstar = bo.p_star(R, U, D)

	#Compute the possible nodes for the risky-security prices:
	node = bo.risky_security_binom_price(N, S, U, D)

	#Number of total nodes:
	dim = len(node)

	#Create another nodes representing the value of option at each time-step:
	dim_temp = int(2**N) -1
	H_node = [None] * dim

	#Start pricing from the backward:
	low = int(2**N) - 1
	up = int(2**(N+1)) -1
	
	for i in range(low,up,1):
		temp = bo.put_payoff(node[i].data,X)
		H_node[i] = bo.TreeNode(temp)

	#Compute the value of american option for each level:
	for i in range(N-1,-1,-1):
		ind_low = int(2**i) - 1
		ind_up = int(2**(i+1)) - 1

		k = 0
		for j in range(ind_low,ind_up,1):
			temp_b1 = bo.put_payoff(node[j].data,X)
			temp_b2_1 = pstar*bo.put_payoff(node[j].children[0].data, X)	
			temp_b2_2 = (1-pstar)*bo.put_payoff(node[j].children[1].data, X)	
			temp_b2 = (1./(1.+R))*(temp_b2_1 + temp_b2_2)
			
		
			if temp_b1 < temp_b2:
				H_node[j] = bo.TreeNode(temp_b2)
				H_node[j].add_child(H_node[k+ind_up])
				H_node[j].add_child(H_node[k+1+ind_up])
			else:
				H_node[j] = bo.TreeNode(temp_b1)
				H_node[j].add_child(H_node[k+ind_up])
				H_node[j].add_child(H_node[k+1+ind_up])

			k = k + 2


	return C_A, H_node
