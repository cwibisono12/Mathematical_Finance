#!/usr/bin/env python3

import sys
sys.path.append("..")
from lib import option as op
	
def ex54():
	X = 24	
	r = 7.48
	t = 0.
	T = 6/12.
	C_E = 5.09
	P_E = 7.78
	S = 20.37

	#Check whether there is an arbitrage opportunity associated with the given European call and put option prices
	val = op.eu_put_call(r,T,S,X,C_E,P_E)
	if val == True:
		print("arbitrage opportunity exist")
	else:
		print("safe from arbitrage")
	
if __name__ == "__main__":
	ex54()
