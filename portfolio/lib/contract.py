#!/usr/bin/env python3
import numpy as np

'''
Module Description:
Forward and Future Contracts Pricing Module:
The forward and future pricing module is used to prevent arbitrage profit.
Future Contract is used to eliminate risk associated with the loss party.
C. Wibisono
Formalisms are based on Chapter 4 M. Capinski and T. Zastawniak
Mathematics for Finance
'''

def bond(r,t,T):
	'''
	Zero coupun bond maturing at time T measured with respect to the reference time t.
	C. Wibisono	
	05/04 '25
	Function Argument(s):
	r: risk-free interest rate
	t: the time when the forward contract is initiated.
	T: delivery time when the asset needs to be purchased/sold.
	Return:
	b: the price of a unit zero coupun bond.
	'''

	b = 1./np.exp(r*(T-t))
	return b

def fow_price(r,t,T,S):
	'''
	Forward Contract Pricing at time t with delivery time T.
	C. Wibisono
	05/04 '25
	Function Argument(s):
	r: risk-free interest rate
	t: the time when the forward contract is initiated.
	T: delivery time
	S: the risky securiy price at time t
	Return:
	fow: forward pricing at time t
	'''

	fow = S/bond(r,t,T)
	return fow

def fow_price_div(r,t,T,S,r_div):
	'''
	Forward Contract Pricing with dividend paid continously
	C. Wibisono
	05/04 '25
	Function Argument(s):
	r: risk-free interest rate
	t: the time when the forward contract is initiated.
	T: delivery time
	S: the risky securiy price at time t
	r_div: rate in which dividend is paid by the risky asset holders.
	Return:
	fow: forward pricing at time t
	'''
	
	fow = S*(np.exp(-r_div*(T-t)))/bond(r,t,T)
	return fow


def fow_price_div_disc(r,t,t_div,T,S,div):
	'''
	Forward Contract Pricing with dividend paid at a discrete time t_div
	C. Wibisono
	05/04 '25
	Function Argument(s):
	r: risk-free interest rate
	t: the time when the forward contract is initiated.
	t_div: the time when the dividend is paid
	T: delivery time
	S: the risky securiy price at time t
	div: the amount of dividend to be received by the risky asset holders at time t_div
	Return:
	fow: forward pricing at time t
	'''
	if t_div > t and t_div < T:	
		fow = (S - bond(r,t,t_div)*div)/bond(r,t,T)
	else:
		fow = S/bond(r,t,T)
	return fow


def fow_value_div_disc(r,t,t_div,T,S_0,S_t,div):
	'''
	The Value of the forward contract at time t
	C. Wibisono
	05/04 '25
	Function Argument(s):
	r: risk-free interest rate
	t: the time when the value of the forward contract is measured.
	t_div: the time when the dividend is paid
	T: delivery time
	S_0: the risky security price at time 0
	S_t: the risky security price at time t
	div: the amount of dividend to be received by the risky asset holders at time t_div
	Return:
	val: value of the forward contract
	'''
	
	final = fow_price_div_disc(r,t,t_div,T,S_t,div)
	initial = fow_price_div_disc(r,0,t_div,T,S_0,div)
	val = (final - initial)*bond(r,t,T)

	return val

def fow_value_dev(r,t,T,S,X):
	'''
	The Value of the forward contract at time t with delivery price X with no dividend paid 
	C. Wibisono
	05/18 '25
	Function Argument(s):
	r: risk-free interest rate
	t: the time when the value of the forward contract is measured.
	T: delivery time
	S: the risky security price at time t
	X: delivery price
	Return:
	val: value of the forward contract
	'''
	
	final = fow_price(r,t,T,S)
	initial = X
	val = (final - initial)*bond(r,t,T)

	return val

def future_m2m_val(r,t,T,S):
	'''
	Compute Marking to Market (m2m) values (cash-flow) for the future contract starting at t 
	with delivery time T.
	C. Wibisono
	05/06 '25
	Function Argument(s):
	r: risk-free interest rate
	t: the time when the value of the future contract is initiated.
	T: delivery time (in year)
	S: the risky security price from t to T [list]
	Return:
	m2m_val: (list) marking to market values for each time step owned by holders.
	'''

	m2m_val = []
	dim = len(S)
	time = []
	future_price = []
	for i in range(dim):
		time.append((t+i)/12.)
	for i in range(dim): 
		temp_forw_f = S[i]/bond(r,time[i],T)
		future_price.append(temp_forw_f)
		if i == dim - 1:
			temp_forw_f = S[i]
		if i == 0:
			continue
		else:
			temp_forw_i = S[i-1]/bond(r,time[i-1],T)
			temp = temp_forw_f - temp_forw_i
			m2m_val.append(temp)

	return future_price, m2m_val
			
