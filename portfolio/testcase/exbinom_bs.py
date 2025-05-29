#!/usr/bin/env python3

import sys
sys.path.append("..")
from lib import blackscholes as bs
import math

if __name__ == "__main__":
	import matplotlib.pyplot as plt
	mu = 0
	sigma = 0.1
	S_0 = 1
	T = 10
	N = int(sys.argv[1])
	p = float(sys.argv[2])
	
	fig, ax = plt.subplots()
	z=0
	arr = bs.risky_security_binom_price_level(mu, sigma, S_0, T, N, p)
	arr_blackscholes = bs.risky_security_black_scholes_price(mu, sigma, S_0, T)
	dim = len(arr_blackscholes) 
	
	for i,j in arr.items():
		print(i,j)
		z = z + j
		ax.plot(i,j,'bo')#print(x,y)
	
	for x,y in arr_blackscholes.items():
		ax.plot(math.exp(x),0.00006*y,'r.')
		#print(x,y)
		#print(arr_blackscholes[i][0],arr_blackscholes[i][1])
	
	ax.set_xlim(0,10)
	ax.set_ylim(bottom=0)
	print("total probability:", z)
	#ax.set_ylim(bottom=0)
	plt.show()
