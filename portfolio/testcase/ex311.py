#!/usr/bin/env python3

import sys
sys.path.append("..")
from lib import optimize as op
	
def ex311():
	sigma = [0.25, 0.28, 0.20]
	m = [0.20, 0.13, 0.17]
	rho = [[1, 0.30, 0.15],[0.30,1,0.],[0.15,0,1.]]

	#Compute Covariance Matrix:
	Cov= op.cov_construct(rho,sigma)
	#Compute the weight of MVP:
	w_mvp = op.mvp(Cov)
	#Compute the Return and Risk associated with MVP:
	mu_v, sigma_v = op.value(m,Cov,w_mvp)
	#Print the output:
	print("weight_MVP:")
	print(w_mvp)
	print("Value of Portfolio with MVP:")
	print("Expected Return:",mu_v,"Risk:",sigma_v)
	

if __name__ == "__main__":
	ex311()
