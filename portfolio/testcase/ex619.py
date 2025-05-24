#!/usr/bin/env python3

import sys
sys.path.append("..")
from lib import option as op
from lib import binomial as bo

def ex619():
	X = 80	
	R = 0.05
	U = 0.1
	D = -0.05
	S = 80
	N = 2

	#Compute the price of American call and put with strike price X with an expiry time N:
	C_A, P_A = op.am_option_binom_disc(R, U, D, S, X, N)
	print("American Option Prices:")
	print("C_A:",C_A,"P_A:",P_A[0].data)	
	
	#Print the value (payoff) of the put option for each time step:
	print("\n")
	print("Values for each time step:")
	for k in range(N):
		temp = bo.risky_security_binom_price_level(k, P_A)
		print("step "+str(k)+" :")
		for q in temp.keys():
			print("value:",q,"childs:",temp[q])

	print("step "+str(N)+" :")
	#Print the latest level
	low = int(2**2) - 1
	up = int(2**3)  - 1
	for q in range(low, up,1):
		print("value:",P_A[q].data)

if __name__ == "__main__":
	ex619()
