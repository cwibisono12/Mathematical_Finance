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
	b = S - X/co.bond(r,0,T)
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
	b = (S/co.bond(r_div,0,T)) - (X/co.bond(r,0,T))
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
	b = (S - div_0) - (X/co.bond(r,0,T))
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
	b_high = S - X/co.bond(r,0,T)
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
	b_high = S - X/co.bond(r,0,T)
	b_low = S/co.bond(r_div,0,T) - X
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
	b_high = S - X/co.bond(r,0,T)
	b_low = (S - div_0) - X
	if a > b_high:
		return True
	if a < b_low:
		return True
	else:
		return False
