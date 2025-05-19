#!/usr/bin/env python3

import sys
sys.path.append("..")
from lib import option as op
	
def ex67():
	X = 60	
	R = 0.05
	U = 0.3
	D = -0.1
	S = 50
	N = 3

	#Compute the price of a European call and put with strike price X exercised after N time steps:
	C_E, P_E = op.eu_option_binom_disc(R, U, D, S, X, N)
	print("European Option Prices:")
	print("C_E:",C_E,"P_E:",P_E)	
	
if __name__ == "__main__":
	ex67()
