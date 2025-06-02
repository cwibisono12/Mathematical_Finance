#!/usr/bin/env python3

import sys
sys.path.append("..")
from lib import blackscholes as bs
import math

if __name__ == "__main__":
	time = int(sys.argv[1])
	t = time/365.
	sigma = 0.3
	S_t = 60
	T = 90./365.
	X = 60
	r = 0.08
	C_E, P_E = bs.eu_option_bs(S_t, t, T, r, sigma, X)
	greek_params = bs.eu_call_sensitivity(S_t, T, r, sigma, X)
	print("call price:", C_E, "put_price:",P_E)
	print("Call Sensitivity:",greek_params)
