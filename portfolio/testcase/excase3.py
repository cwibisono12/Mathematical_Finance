#!/usr/bin/env python3

import sys
sys.path.append("..")
from lib import optimize as op
from lib import saving as sv
from ex314 import cml 

import matplotlib.pyplot as plt
import matplotlib.ticker as tck
import numpy as np

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
plt.rcParams['figure.dpi'] = 150	

def excase3():
	'''
	Portfolio Construction consisting of a risk-free security (e.g saving) and multiple 
	risk securities (e.g stocks).
	
	Problem Statement:
	Design several possible portfolios for the pension scheme that consists of a risk-free security and multiple 
	risk securities. 
	
	Requirement(s):
	Investor would like to have the accumulated capital to be payable for N2 years with the growth rate g
	in which after N1 years of investing, will receive frac amounts of income at year N1.
	The investor income also has the growth rate g and the interest rate associated with the saving is r.

	Restriction(s):
	No short selling of any risky securities are permitted during the time of investment.
	'''

	sigma = [0.15, 0.22, 0.26]
	m = [0.08, 0.10, 0.14]
	rho = [[1, 0.50, -0.3],[0.5,1,0.3],[-0.3,0.3,1.]]
	mu_v = np.arange(0,0.9,0.001)
	R = 0.05	

	m12 = [0.08,0.10]
	m23 = [0.10,0.14]
	m13 = [0.08,0.14]
	sigma12 = [0.15, 0.22]
	sigma23 = [0.22,0.26]
	sigma13 = [0.15, 0.26]
	rho12 = [[1, 0.50],[0.50,1]]
	rho23 = [[1,0.3],[0.3,1]]
	rho13= [[1,-0.3],[-0.3,1]]

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


	#Compute the weight associated with the Minimum Variance Portfolio:
	w_mvp = op.mvp(Cov)
	#Print the weight of MVP:
	print("MVP weight:",w_mvp)
	
	#Compute the expected return and risk associated with the MVP:
	mu_mvp, sigma_mvp = op.value(m,Cov,w_mvp)
	#Print the Expected Return and Risk:
	print("Expected Return %(MVP):",mu_mvp*100,"Risk %(MVP):",100*sigma_mvp)
	print("\n")
	#Compute the weight associated with the Market Portfolio:
	w_mp, mu_mp,sigma_mp = op.eff_frontier_mp(m,Cov,R) 
	#Print the weight of the Market Portfolio::
	print("Market Portfolio weight:",w_mp)

	#Print the Expected Return and Risk:
	print("Expected Return %(MP):",100*mu_mp,"Risk %(MP):",100*sigma_mp)
	print("\n")
	#As one of the weight is negative, we are not permitted to use the w_mp values as it 
	#will violate the investment restriction in which no short selling is permitted.
	
	
	#Define The Axes:
	fig, ax = plt.subplots()
	ax.tick_params(direction='in',axis='both',which='major',bottom='True',left='True',right='True',top='True',length=9,width=0.75)
	ax.tick_params(direction='in',axis='both',which='minor',bottom='True',left='True',right='True',top='True',length=6,width=0.75)
	
	n = len(mu_v)

	sigma_v = []
	sigma12_v = []
	sigma23_v = []
	sigma13_v = []
	sigmacomb_mp = np.arange(0,0.9,0.01)
	dim2 = len(sigmacomb_mp)
	mucomb_mp = []

	#Compute portfolios along the CML line:
	for i in range(dim2):
		mucomb_mp.append(cml(mu_mp,sigma_mp,R,sigmacomb_mp[i]))

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

	#Find the maximum gradient of new CML associated with no short-selling:
	max_grad_new_CML = 0
	ind_max_CML = 0
	for i in range(n):
		temp = (mu_v[i] - R)/sigma13_v[i]
		if temp > max_grad_new_CML:
			max_grad_new_CML = temp
			ind_max_CML = i

	#Compute the weight associated with the Market Portfolio with the new CML line with no short-selling:
	w_mp_new = []
	dim3 = len(a13)
	for i in range(dim3):
		w_mp_new.append(a13[i]*mu_v[ind_max_CML]+b13[i])
	print("\n") 
	#Print the weight associated with the new CML line with no short-selling:
	print("Market Portfolio weight (no short-selling):",w_mp_new)

	#Print the risk and expected return associated with the new CML line with no short-selling:
	print("Expected Return: %(MP with no short-selling)",100*mu_v[ind_max_CML],"Risk %(new CML with no short selling):",100*sigma13_v[ind_max_CML])
	
	print("\n")
	#Construct the new CML line:
	mucomb_mp_new = []
	for i in range(dim2):
		mucomb_mp_new.append(cml(mu_v[ind_max_CML],sigma13_v[ind_max_CML],R,sigmacomb_mp[i]))


	#Report the Possible Portfolios for several desired risk based on the new Efficient Frontier (new CML line with no-short selling):
	print("====================\n\n\n")
	print("Possible Portfolios with Desired Risk:")
	risk = [0, 0.025, 0.05, 0.075, 0.1]
	dimrisk = len(risk)
	ex_return = []
	for k in range(dimrisk):
		temp = cml(mu_v[ind_max_CML],sigma13_v[ind_max_CML],R,risk[k])
		ex_return.append(temp)
	
	#Compute the weight for a given risk associated with the new efficient frontier such that the proportion
	#of a risk-free security can be determined:
	fracsav = []
	for k in range(dimrisk):
		temp_b = sum(op.minline(a13,b13,ex_return[k]))
		temp_c = 1 - temp_b
		fracsav.append(temp_c) #determine the fraction of income to be invested
	#Dictionary of pair of risk, return, and income fraction to be invested:
	arr = {}
	for k in range(dimrisk):
		arr[100*risk[k]] = (100*ex_return[k], 100*fracsav[k])

	print(arr)


	ax.plot(sigma_v,mu_v,color='k',linewidth = 1.0, label='Markowitchz Line (total)')
	ax.plot(sigmacomb_mp,mucomb_mp,color='m',linewidth = 1.0, label='CML line')
	ax.plot(sigmacomb_mp,mucomb_mp_new,color='m',linestyle='--',linewidth = 1.0, label='CML line (with no short selling)')
	ax.plot(sigma12_v,mu_v,color='r',linewidth = 0.85,linestyle='-.', label='Markowitchz Line (12)')
	ax.plot(sigma23_v,mu_v,color='b',linewidth = 0.85,linestyle='-.', label='Markowitchz Line (23)')
	ax.plot(sigma13_v,mu_v,color='g',linewidth = 0.85,linestyle='-.', label='Markowitchz Line (13)')
	for i in range(3):
		ax.plot(sigma[i],m[i],'m*',label = 'security point')

	ax.plot(sigma_mp,mu_mp,'b+',label='Market Portfolio')	
	ax.plot(sigma13_v[ind_max_CML],mu_v[ind_max_CML],'r+',label='Market Portfolio (no short selling)')	
	ax.set_xlim(0.1,0.4)
	ax.set_ylim(0.02,0.18)
	ax.set_ylabel(r'Expected Return $\mu$',style='normal',fontweight='bold')
	ax.set_xlabel(r'Risk $\sigma$',style='normal',fontweight='bold')
	ax.legend()

	plt.show()

if __name__ == "__main__":
	excase3()
