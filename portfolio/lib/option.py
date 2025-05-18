#!/usr/bin/env python3
import numpy as np
from . import contract as co

'''
Module Description:
Options Pricing Module to prevent arbitrage profit
C. Wibisono
Formalisms are based on Chapter 5 M. Capinski and T. Zastawniak
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
	with the strike price X and the dividend paid continously somewhere 
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

