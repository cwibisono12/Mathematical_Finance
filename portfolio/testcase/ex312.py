#!/usr/bin/env python3

import sys
sys.path.append("..")
from lib import optimize as op
	
def ex312():
	sigma = [0.25, 0.28, 0.20]
	m = [0.20, 0.13, 0.17]
	rho = [[1, 0.30, 0.15],[0.30,1,0.],[0.15,0,1.]]
	mu_v = 0.2

	#Compute Covariance Matrix:
	Cov= op.cov_construct(rho,sigma)
	#Compute the weight and risk of efficient_frontier associated with the minimum variance line for a given mu_v
	w_eff, sigma_v = op.eff_frontier(m,Cov,mu_v)
	#Print the output:
	print("weight of Efficient Frontier:")
	print(w_eff)
	print("Value of Portfolio with Eff_Frontier:")
	print("Expected Return:",mu_v,"Risk:",sigma_v)
	#Compute the vectors a and b associated with the minimum variance line:
	a, b = op.eff_frontier_vector(m,Cov)

	#Compute the risk from the vectors:
	w_eff2 = []
	dim = len(m)
	for k in range(dim):
		temp = mu_v*a[k] + b[k]
		w_eff2.append(temp)
	mu2_v, sigma2_v = op.value(m,Cov,w_eff2)
	print("Risk from the Vectors:")
	print("Risk:",sigma2_v)	

if __name__ == "__main__":
	ex312()
