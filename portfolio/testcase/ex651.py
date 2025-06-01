#!/usr/bin/env python3
import math
import sys
sys.path.append("..")
from lib import option as op
from lib import binomial as bo
	
def ex651(timestep):
	'''
	Compute European Call and Put Options per time step up to expiry time.
	'''
	X = 105	
	R = 0.1
	U = 0.2
	D = -0.1
	S = 100
	N = 3

	#Compute the possible values of risky security prices over time based on binomial model:
	node_s = bo.risky_security_binom_price(N, S, U, D)

	#Compute the possible values of European Call and Put Options per time step:
	C_E, P_E = op.eu_option_binom_disc_level(R, U, D, S, X, N)
	
	#Compute the European Call and Put Options at time 0:
	C_E_0, P_E_0 = op.eu_option_binom_disc(R, U, D, S, X, N)
		
	#Print the possible position:
	low = int(math.pow(2,timestep)) - 1
	up = int(math.pow(2,timestep+1)) - 1
	
	print("European Options Price at time 0")
	print("stock:",node_s[0].data,"call:",C_E_0,"put:",P_E_0)
	print("List of possible portfolio for step: "+str(timestep))
	#Retrieve the stock as well as money market position.
	for i in range(low,up,1):
		print("stock:",node_s[i].data,"call:",C_E[i].data,"put:",P_E[i].data)
	
	
if __name__ == "__main__":
	timestep = int(sys.argv[1])
	ex651(timestep)
