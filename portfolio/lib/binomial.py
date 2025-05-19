#!/usr/bin/env python3
import math

'''
Module Description:
Binomial Model
C. Wibisono
Formalisms are based on Chapter 6 M. Capinski and T. Zastawniak
Mathematics for Finance
'''

def m_order(S, U, D, N, X):
	'''
	Compute the least order m for use in Cox-Ross-Rubinstein Formula for Option Pricing
	C. Wibisono
	05/19 '25
	Function Argument(s):
	S: (float) the risky security price at time 0
	U: (float) the rate of return if the risky security price goes up
	D: (float) the rate of return if the risky security price goes down
	N: (int) the number of time step where the option is to be exercised
	X: (float) the strike price of an option
	Return:
	m: (int) the order before the value exceeds the strike price
	'''
	
	k = 0
	while(1):
		temp = S*(math.pow(1+U,k))*(math.pow(1+D,N-k))
		if temp > X:
			return k
		else:
			k = k + 1
	

def p_star(R, U, D):
	'''
	Compute the value of risk-neutral probability with a risk-free rate security R
	C. Wibisono
	05/19 '25
	Function Argument(s):
	R: (float) the rate of risk-free security as a form of money market account
	U: (float) the rate of return if the risky security price goes up
	D: (float) the rate of return if the risky security price goes down
	Return:
	p: (float) the risk-neutral probability 
	'''

	a = R - D
	b = U - D
	p = a/b
	return p


def cbd(m, N, p):
	'''
	Compute the cumulative binomial distribution with N trials
	with probability of sucess p for a given trial.
	C. Wibisono
	05/19 '25
	Function Argument(s):
	m: (int) the index to counts satisfying a condition
	N: (int) the number of trial (time-step)
	p: (float) the probability of sucess for wach trial
	Return:
	val: (float) the cumulative binomial distribution
	'''
	
	val = 0
	for k in range(m+1):
		temp = (math.comb(N,k))*(math.pow(p,k))*(math.pow(1-p,N-k))
		val = val + temp

	return val

 
