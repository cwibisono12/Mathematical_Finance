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

def ex313():
	sigma = [0.25, 0.28, 0.20]
	m = [0.20, 0.13, 0.17]
	rho = [[1, 0.30, 0.15],[0.30,1,0.],[0.15,0,1.]]
	mu_v = np.arange(0,0.9,0.001)
	m12 = [0.20,0.13]
	m23 = [0.13,0.17]
	m13 = [0.20,0.17]
	sigma12 = [0.25, 0.28]
	sigma23 = [0.28,0.20]
	sigma13 = [0.25, 0.20]
	rho12 = [[1, 0.30],[0.30,1]]
	rho23 = [[1,0],[0,1]]
	rho13= [[1,0.15],[0.15,1]]

	#Compute the Covariance Matrix:
	Cov= op.cov_construct(rho,sigma)
	
	#Compute the Covariance Matrices for each pair of security:
	Cov12 = op.cov_construct(rho12,sigma12)
	Cov23 = op.cov_construct(rho23,sigma23)
	Cov13 = op.cov_construct(rho13,sigma13)

	#Compute the vectors a and b associated with the minimum variance line:
	a, b = op.eff_frontier_vector(m,Cov)

	#Compute the vectors a and b associated with the minimum variance line of each pair pf security:
	a12, b12 = op.eff_frontier_vector(m12,Cov12)
	a23, b23 = op.eff_frontier_vector(m23,Cov23)
	a13, b13 = op.eff_frontier_vector(m13,Cov13)

	#Define The Axes:
	fig, ax = plt.subplots()
	ax.tick_params(direction='in',axis='both',which='major',bottom='True',left='True',right='True',top='True',length=9,width=0.75)
	ax.tick_params(direction='in',axis='both',which='minor',bottom='True',left='True',right='True',top='True',length=6,width=0.75)
	
	n = len(mu_v)

	sigma_v = []
	sigma12_v = []
	sigma23_v = []
	sigma13_v = []

	dim = len(m)
	dimij = 2

	#Compute the risk from the vectors:
	for j in range(n):
		w_eff2 = []
		w12_eff2 = []
		w23_eff2 = []
		w13_eff2 = []
		for k in range(dim):
			temp = mu_v[j]*a[k] + b[k]
			w_eff2.append(temp)

		for l in range(2):
			temp12 = mu_v[j]*a12[l] + b12[l]
			temp23 = mu_v[j]*a23[l] + b23[l]
			temp13 = mu_v[j]*a13[l] + b13[l]
			w12_eff2.append(temp12)
			w23_eff2.append(temp23)
			w13_eff2.append(temp13)

		mu2_v, sigma2_v = op.value(m,Cov,w_eff2)
		mu12_v, sigma12_v2 = op.value(m12,Cov12,w12_eff2)
		mu23_v, sigma23_v2 = op.value(m23,Cov23,w23_eff2)
		mu13_v, sigma13_v2 = op.value(m13,Cov13,w13_eff2)
		sigma_v.append(sigma2_v)
		sigma12_v.append(sigma12_v2)
		sigma23_v.append(sigma23_v2)
		sigma13_v.append(sigma13_v2)
	
		del w_eff2
		del w12_eff2
		del w23_eff2
		del w13_eff2

	ax.plot(sigma_v,mu_v,color='k',linewidth = 1.0, label='Markowitchz Line (total)')
	ax.plot(sigma12_v,mu_v,color='r',linewidth = 0.85, label='Markowitchz Line (12)')
	ax.plot(sigma23_v,mu_v,color='b',linewidth = 0.85, label='Markowitchz Line (23)')
	ax.plot(sigma13_v,mu_v,color='g',linewidth = 0.85, label='Markowitchz Line (13)')
	for i in range(3):
		ax.plot(sigma[i],m[i],'m*',label = 'security point')
	
	ax.set_xlim(0.1,0.4)
	ax.set_ylim(0.05,0.35)
	ax.set_ylabel(r'Expected Return $\mu$',style='normal',fontweight='bold')
	ax.set_xlabel(r'Risk $\sigma$',style='normal',fontweight='bold')
	ax.legend()

	plt.show()

if __name__ == "__main__":
	ex313()
