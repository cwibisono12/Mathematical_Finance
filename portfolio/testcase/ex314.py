#!/usr/bin/env python3

import sys
sys.path.append("..")
from lib import optimize as op
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
import numpy as np


plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
plt.rcParams['figure.dpi'] = 150

def cml(mu_mp, sigma_mp, R, sigma):
	#Compute the expected return according to the CML.
	mu = R + (mu_mp -R)*sigma/sigma_mp

	return mu

def ex314():
	sigma = [0.25, 0.28, 0.20]
	m = [0.20, 0.13, 0.17]
	rho = [[1, 0.30, 0.15],[0.30,1,0.],[0.15,0,1.]]
	R = 0.05
	mu_v = np.arange(0,0.9,0.01)

	#Compute Covariance Matrix:
	Cov= op.cov_construct(rho,sigma)

	#Compute the weight, expected return, and risk of the market portfolio:
	w_eff_mp, mu_mp, sigma_mp = op.eff_frontier_mp(m,Cov,R)
	
	#Print the output:
	print("weight of Efficient Frontier:")
	print(w_eff_mp)
	print("Value of Portfolio with Eff_Frontier:")
	print("Expected Return:",mu_mp, "Risk:",sigma_mp)

	
	#Define The Axes:
	fig, ax = plt.subplots()
	ax.tick_params(direction='in',axis='both',which='major',bottom='True',left='True',right='True',top='True',length=9,width=0.75)
	ax.tick_params(direction='in',axis='both',which='minor',bottom='True',left='True',right='True',top='True',length=6,width=0.75)
	
	#Compute the vectors a and b associated with the minimum variance line:
	a, b = op.eff_frontier_vector(m,Cov)
	
	n = len(mu_v)
	sigma_v = []
	dim = len(m)
	
	#Compute the risk from the vectors:
	for j in range(n):
		w_eff = []
		for k in range(dim):
			temp = mu_v[j]*a[k] + b[k]
			w_eff.append(temp)
		
		mu2_v, sigma2_v = op.value(m,Cov,w_eff)
		sigma_v.append(sigma2_v)
		del w_eff

	#Compute the portfolios along the CML line:
	sigma_CML = np.arange(0,0.9,0.01)
	mu_CML=np.zeros(n)
	for k in range(n):
		mu_CML[k] = cml(mu_mp,sigma_mp, R, sigma_CML[k])
	
	#Plot the CML line along with the minimum variance line associated with risky securities:
	ax.plot(sigma_v,mu_v,color='m',linewidth = 0.85, label='Markowitchz Line')
	ax.plot(sigma_CML,mu_CML,color='b',linewidth = 0.85, label='CML Line')
	ax.plot(sigma_mp,mu_mp,'r*',label='Market Portfolio')
	ax.set_ylabel(r'Expected Return $\mu$',style='normal',fontweight='bold')
	ax.set_xlabel(r'Risk $\sigma$',style='normal',fontweight='bold')
	ax.set_xlim(0,1)
	ax.set_ylim(0,1)
	ax.legend()
	
	plt.show()
if __name__ == "__main__":
	ex314()
