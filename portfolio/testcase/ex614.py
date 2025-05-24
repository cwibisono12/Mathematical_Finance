#!/usr/bin/env python3
import math
import sys
sys.path.append("..")
from lib import option as op
from lib import binomial as bo
	
def ex14(timestep):
	'''
	Hedging American Options for the option writer by replicating strategy.
	'''
	X = 100	
	R = 0.1
	U = 0.2
	D = -0.1
	S = 100
	N = 3

	#Compute the possible values of risky security prices over time based on binomial model:
	node_s = bo.risky_security_binom_price(N, S, U, D)

	#Compute the possible values of put option:
	C_A, node_h = op.am_option_binom_disc(R, U, D, S, X, N)
	
	#Compute the risky security position:
	x_node = op.am_option_hedge_stock(node_s, node_h)

	#Compute the money-market position:
	y_node = op.am_option_hedge_market(x_node, node_s, node_h[0].data, R)
	
	#Print the possible position:
	low = int(math.pow(2,timestep-1)) - 1
	up = int(math.pow(2,timestep)) - 1
	
	print("Hedging American Option")
	print("List of possible portfolio for step: "+str(timestep))
	#Retrieve the stock as well as money market position.
	for i in range(low,up,1):
		print("stock:",x_node[i].data,"money-market:",y_node[i].data)
	
	
if __name__ == "__main__":
	timestep = int(sys.argv[1]) #Evaluate the risky security price at a given time step
	ex14(timestep)
