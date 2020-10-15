#!/usr/bin/python3.5
import subprocess
import numpy as np
import functools

def Jane(W):
	J = ((sum(W))**2)/(len(W)*sum([i**2 for i in W]))
	return J
def Jane_single(W,host):
	fairness_limit = sum([i**2 for i in W])/sum(W)
	J =  W[host-1]/fairness_limit
	return J

def Ginni(W):
	mad = np.abs(np.subtract.outer(W, W)).mean()
	rmad = mad/np.mean(W)
	G = 0.5 * rmad
	return G
def Nowicki(W):
	N = (len(W)*functools.reduce(lambda W1, W2: W1*W2, W))/sum([i**len(W) for i in W])
	return  N

def Satisfaction(W,Demand):
	S = W/Demand
	return S



# W_c = [268486,284157,330158,308714,333687,345431,343106,348846,349762,295199]
#W = [10,10,10,10,10,10,10,10,10,10]
# #print (W)
# print(Ginni(W_c))
#print(Ginni(W))