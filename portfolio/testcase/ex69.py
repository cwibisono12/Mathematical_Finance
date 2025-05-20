#!/usr/bin/env python3

import sys
sys.path.append("..")
from lib import option as op
	
def ex69():
	X = 62	
	R = 0.03
	U = 0.1
	D = -0.05
	S = 60
	N = 3

	#Compute the price of American call and put with strike price X with an expiry time N:
	C_A, P_A = op.am_option_binom_disc(R, U, D, S, X, N)
	print("American Option Prices:")
	print("C_A:",C_A,"P_A:",P_A)	
	
if __name__ == "__main__":
	ex69()
