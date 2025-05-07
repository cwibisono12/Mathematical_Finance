#!/usr/bin/env python3

import sys
sys.path.append("..")
from lib import contract as co
	
def ex414():	
	r = 0.08
	t = 0.
	T = 3/12.
	S = [100,102,101,105] 

	#Compute the marking to market values over the period of delivery time of the future contracts:	
	future_price, m2m_val = co.future_m2m_val(r,t,T,S)
	
	print("Marking to Market Values:")
	dim = len(m2m_val)
	for k in range(dim+1):
		if k == 0:
			print("t-months:",str(int(t+k))+'/'+str(12),"future-price:",future_price[k],"amount:",'-')
		else:
			print("t-months:",str(int(t+k))+'/'+str(12),"future-price:",future_price[k],"amount:",m2m_val[k-1])
if __name__ == "__main__":
	ex414()
