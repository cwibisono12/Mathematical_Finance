#!/usr/bin/env python3
import math

'''
Module Description:
Binomial Model
C. Wibisono
Formalisms are based on Chapter 6 M. Capinski and T. Zastawniak
Mathematics for Finance
'''

def m_order(S, U, D, N, X):
	'''
	Compute the least order m for use in Cox-Ross-Rubinstein Formula for Option Pricing
	C. Wibisono
	05/19 '25
	Function Argument(s):
	S: (float) the risky security price at time 0
	U: (float) the rate of return if the risky security price goes up
	D: (float) the rate of return if the risky security price goes down
	N: (int) the number of time step where the option is to be exercised
	X: (float) the strike price of an option
	Return:
	m: (int) the order before the value exceeds the strike price
	'''
	
	k = 0
	while(1):
		temp = S*(math.pow(1+U,k))*(math.pow(1+D,N-k))
		if temp > X:
			return k
		else:
			k = k + 1
	

def p_star(R, U, D):
	'''
	Compute the value of risk-neutral probability with a risk-free rate security R
	C. Wibisono
	05/19 '25
	Function Argument(s):
	R: (float) the rate of risk-free security as a form of money market account
	U: (float) the rate of return if the risky security price goes up
	D: (float) the rate of return if the risky security price goes down
	Return:
	p: (float) the risk-neutral probability 
	'''

	a = R - D
	b = U - D
	p = a/b
	return p

def call_payoff(S, X):
	'''
	Compute the payoff associated with the call option at any time.
	No dividend is paid.
	C. Wibisono
	05/20 '25
	Function Argument(s):
	S: (float) risky security price
	X: (float) strike price
	Return:
	val: (float) the payoff
	'''

	if S > X:
		val = S - X
	else:
		val = 0

	return val

def put_payoff(S, X):
	'''
	Compute the payoff associated with the put option at any time.
	No dividend is paid.
	C. Wibisono
	05/20 '25
	Function Argument(s):
	S: (float) risky security price
	X: (float) strike price
	Return:
	val: (float) the payoff
	'''

	if S > X:
		val = 0
	else:
		val = X - S

	return val


def cbd(m, N, p):
	'''
	Compute the cumulative binomial distribution with N trials
	with probability of success p for a given trial.
	C. Wibisono
	05/19 '25
	Function Argument(s):
	m: (int) the index to count satisfying a condition for binomial model of an option pricing
	N: (int) the number of trial (time-step)
	p: (float) the probability of success for each trial
	Return:
	val: (float) the cumulative binomial distribution
	'''
	
	val = 0
	for k in range(m+1):
		temp = (math.comb(N,k))*(math.pow(p,k))*(math.pow(1-p,N-k))
		val = val + temp

	return val


class TreeNode:
	'''
	Create a tree object. This data structure is used to create
	possible representation of risky security prices for each time step within the binomial model.
	'''

	def __init__(self, data):
		'''
		Instantiate a node
		'''
		self.data = data
		self.children = []

	def add_child(self, child):
		'''
		Add a child for a given node
		'''
		self.children.append(child)


def risky_security_binom_price(N, S_0, U, D):
	'''
	Compute the risky security prices up to expiry time N to be used in conjunction with the American Option.
	C. Wibisono
	05/20 '25
	Function Argument(s):
	N: (int) the number of trial (time-step) or expiry time
	S_0: (float) the initial price associated with the risky security
	U: (float) the rate of the return if the risky security price goes up
	D: (float) the rate of the return if the risky security price goes down
	Return:
	node: (list) array of TreeNode objects (see TreeNode object class to retrive the class member)
	'''
	
	#Create nodes container for storing the possible risky security prices according to binomial model.
	node = []

	#The first element becomes a root of the tree object
	node.append(TreeNode(S_0))

	#In the visual representation we will form as many as 2^(N+1) - 1 nodes.
	dim = math.pow(2,N+1) -1 

	#Create nodes consisting of possibles risky security prices:
	dim_temp = int(math.pow(2,N))-1 	
	for i in range(dim_temp):
		up = node[i].data*(1+U)
		down = node[i].data*(1+D)
		n_up = TreeNode(up)
		n_down =  TreeNode(down)
		node.append(n_up)
		node.append(n_down)
		node[i].add_child(n_up)
		node[i].add_child(n_down) 

	return node	

def risky_security_binom_price_level(level, node):
	'''
	List the risky security prices at time level.
	C. Wibisono
	05/20 '25
	Function Argument(s):
	level: (int) the time step when the nodes are retrieved.
	node: (list of TreeNode objects) the array of TreeNode objects from the risky_security_binom_price
	return:
	arr: (dict consisting of risky security price and its childs at time level)
	'''
	arr = {}
	low = int(math.pow(2, level)) - 1
	up = int(math.pow(2,level+1))-1
	dim = len(node)
	
	for i in range(low, up, 1):
		if i < dim- (up - low) -1:
			arr[node[i].data] = [node[i].children[0].data, node[i].children[1].data]
		else:
			arr[node[i].data] = [0,0]

	return arr



if __name__ == "__main__":
	import sys
	N =int(sys.argv[1])
	level = int(sys.argv[2])
	ans = risky_security_binom_price(N,60,0.1,-0.05)
	n = len(ans)
	print("number_of_nodes:",n,"compute:",int(math.pow(2,N+1))-1)
	print("nodes for level: "+str(level))
	low = int(math.pow(2,level))-1
	up = int(math.pow(2,level+1))-1
	
	#Retrieve the nodes for a given time step (level)
	for i in range(low,up,1):
		print(ans[i].data, ans[i].children[0].data, ans[i].children[1].data)
