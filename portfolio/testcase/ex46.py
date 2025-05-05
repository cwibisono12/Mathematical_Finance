#!/usr/bin/env python3

import sys
sys.path.append("..")
from lib import contract as co
	
def ex46():
	S_0 = 45 #stock price at the beginning of the year
	Sa_t = 49 #stock price (scenario_a) at time t
	Sb_t = 51 #stock price (scenario_b) at time t
	r = 0.06 #the risk-free return 
	T = 1 #delivery time (in year)
	t_div = 0.5 #time when dividend is paid
	t = 0.75 #the time to measure the value of forward contract
	div = 2 #the amount of dividend to be paid to the asset holders
	rho = [[1, 0.30, 0.15],[0.30,1,0.],[0.15,0,1.]]

	#Compute the value of the forward contract at time t
	value_a = co.fow_value_div_disc(r,t,t_div,T,S_0,Sa_t,div)
	value_b = co.fow_value_div_disc(r,t,t_div,T,S_0,Sb_t,div)
	fow_price = co.fow_price_div_disc(r,0,t_div,T,S_0,div)
	fow_price_a = co.fow_price_div_disc(r,t,t_div,T,Sa_t,div)
	fow_price_b = co.fow_price_div_disc(r,t,t_div,T,Sb_t,div)
	
	#Print the value of the forward contract
	print("initial forward price:",fow_price,"final price_a:",fow_price_a,"final_price_b:",fow_price_b)
	print("value of forward contract after "+str(t*12)+' '+'months')
	print("Scenario_a:",value_a)
	print("Scenario_b:",value_b)

if __name__ == "__main__":
	ex46()
