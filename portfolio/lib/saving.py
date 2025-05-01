#!/usr/bin/env python3


'''
Module Description:
Risk-Free Asset Module
C. Wibisono
Formalism is based on Chapter 2 M.Capinski and T.Zastawniak
Mathematics for Finance
'''

def GAF(r,g,N):
	'''
	Compute the Growing Annuity Factor (GAF)
	Function Argument(s):
	r: (float) risk-free interest rate
	g: (float) income growth rate
	N: (int) Number of years
	Return:
	g_af: (float) growing annuity factor
	'''
	a = (1+g)/(r-g)
	b = (((1+g)**N)/((1+r)**N))
	g_af = a*(1-b)
	return g_af


def income_paid(r,g,N1,frac,N2):
	'''
	Compute the fraction of the income paid per year
	such that at year N1, can receive frac amount of income at year N1
	payable for N2 years 
	Function Argument(s):
	r: (float) risk-free interest rate
	g: (float) income growth rate
	N1: (int) Number of years of the income paid to the saving
	frac: (float) desired fraction of income at year N1
	N2: (int) Number of years the capital will be received
	Return:
	x: (float) fraction of the income paid to the saving
	'''
	
	#The amount of the acummulated capital at year N1:
	initial = ((1+r)**N1)*GAF(r,g,N1)

	#The amount of the capital to be received at year N1:
	final = frac*((1+g)**N1)*GAF(r,g,N2)

	#Final fraction of income paid to the saving:
	x = final/initial

	return x


