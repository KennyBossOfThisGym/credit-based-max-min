#!/usr/bin/python3.5
import collections
import numpy as np
from sympy.solvers import solve
from sympy import Symbol
import copy

#from sympy import Symbol, solve
def credit_min_max(Demands,hostname_list,credits,credit_edges,iteration_period):

	#credit_edges = [200,400]
	global_sum = 0
	#create dict for hosts with following structure host:[demands,credits,k]
	hostdict_1 = dict(zip(hostname_list,np.column_stack((Demands, credits, np.empty(len(hostname_list), dtype=object)))))

	
	#create dict for hosts with following structure host:[W,credits,k]
	W_dict={}
	summer = 0
	k_sum = 0
	Wf1 = 100/len(hostname_list)

	if sum(Demands) < 100:
		print ("###### CREDIT-MIN-MAX ######")
		for key in sorted(list(hostdict_1.keys())):
			print("host: " + str(key) + " | " + ("demands: " + str(hostdict_1[key][0])))

		print('')

		for key in sorted(list(hostdict_1.keys())):
		 	print ("host: " + str(key) +' | ' + "allocated: " + str(float("{0:.2f}".format(hostdict_1[key][0]))))
		 	global_sum += hostdict_1[key][0]	
		
		print('')
		# for host,credit in zip(sorted(list(W_dict.keys())),new_credits):
		# 	print("host: " + str(host) + " | " + ("credits: " + str(credit)))
		
		print ("Sum= " + str(global_sum))
		return hostdict_1,credits

	else:
	 #satisfy hosts with low demands, write them down into another dics
		for hostname in hostname_list:
		 	if hostdict_1[hostname][0] <= Wf1:
		 		W_dict[hostname] =  hostdict_1[hostname]
		 		del hostdict_1[hostname]
		#return W_dict
	# calculate additional free resource for allocation
		val = W_dict.items()
		for k in W_dict:
			summer += W_dict[k][0]
		S = len(list(W_dict.keys()))*Wf1 - summer
		#print (S)

	# create cofficients base on credits amount

		for key in hostdict_1:
			if hostdict_1[key][1] < credit_edges[0]:
				hostdict_1[key][2] = 1
				k_sum += hostdict_1[key][2]
			elif (hostdict_1[key][1] >= credit_edges[0] and hostdict_1[key][1] < credit_edges[1]):
		 		hostdict_1[key][2] = 4
		 		k_sum += hostdict_1[key][2]
			else:
		 		hostdict_1[key][2] = 8
		 		k_sum += hostdict_1[key][2]
	# find e and g
		e = Symbol("e")
		e = solve (e*k_sum-S,e)[0]


		#print (e)
		for key in list(hostdict_1.keys()):
			#print (Wf1 + hostdict_1[key][2]*e - hostdict_1[key][0])
			if hostdict_1[key][0] < (Wf1 + hostdict_1[key][2]*e):
		 		S -= hostdict_1[key][0] - Wf1
		 		k_sum += -hostdict_1[key][2]
		 		W_dict[key] =  hostdict_1[key]
		 		del hostdict_1[key]
		
		e = Symbol("e")
		e = solve (e*k_sum-S,e)[0]
		#print (S)

		for key in list(hostdict_1.keys()):
		 	hostdict_1[key][0] = (Wf1 + hostdict_1[key][2]*e)
		 	W_dict[key] =  hostdict_1[key]
		 	del hostdict_1[key]

		new_credits = generate_credits(Wf1,W_dict,credits,iteration_period)
		

		### printing

		print ("###### CREDIT-MIN-MAX ######")
		for host,demand in zip(sorted(list(W_dict.keys())),Demands):
			print("host: " + str(host) + " | " + ("demands: " + str(demand)))

		print('')

		for key in sorted(list(W_dict.keys())):
		 	print ("host: " + str(key) +' | ' + "allocated: " + str(float("{0:.2f}".format(W_dict[key][0]))))
		 	global_sum += W_dict[key][0]	
		
		print('')
		for host,credit in zip(sorted(list(W_dict.keys())),new_credits):
			print("host: " + str(host) + " | " + ("credits: " + str(credit)))
		
		print ("Sum= " + str(global_sum))
		return W_dict,new_credits

	# Count new credits 

def generate_credits(W_f,W_dict,credits,iteration_period):
	new_credits = []
	#print (zip(list(W_dict.keys(),credits)))
	for (key,credit) in zip(sorted(list(W_dict.keys())),credits):
		new_value = credit + (W_f - W_dict[key][0])*iteration_period
		if new_value > 0:
			new_credits.append(new_value)
		else:
			new_credits.append(0)
#
	return new_credits



def min_max(Demands,hostname_list):
	hostdict=dict(zip(hostname_list,Demands))
	total_capacity = 100
	if sum(Demands) < 100:
		print ("###### MIN-MAX ######")
		for key in sorted(list(hostdict.keys())):
	 		print ("host: " + key + " demands " + str(hostdict[key]) + " allocated " + str(float("{0:.2f}".format(hostdict[key]))))

		# aggregate stats
		print ("=============TOTAL STATS====================")
		print ("capacity", total_capacity)
		print ("demand", sum(hostdict.values()))
		print ("amount allocated", sum(hostdict.values()))
		return hostdict
	else:
		output_demands = dict(hostdict)
	# OUTPUT: Allocations.
		final_share=dict()

	# book-keeping
		current_share=dict()
		for user in hostdict:
			current_share[user]=0
		capacity = total_capacity

	# core algm
		while  capacity > 0.00001:
		 	for key in list(hostdict.keys()):
		 		fair_share = capacity/len(list(hostdict.keys()))
		 		#current_share[user] = current_share.get(user, 0) + fair_share
		 		if hostdict[key] <= fair_share:
		 			final_share[key] = hostdict[key]
		 			capacity -= hostdict[key]
		 			del hostdict[key] 
		 			#print("capacity" + str(capacity))
		 		elif current_share[key] == fair_share:
		 			final_share[key] = current_share[key]
		 			capacity -= current_share[key]
		 			del hostdict[key] 
		 		else:
		 			#capacity = capacity - fair_share 
		 			current_share[key] = fair_share
		 			#print ("key " + str(key) + " share " + str(final_share[key]))


		
	# finalize allocations
		#for share in current_share:
		#	final_share[share]=current_share[share]
		print ("###### MIN-MAX ######")
		for key in sorted(list(final_share.keys())):
	 		print ("host: " + key + " demands " + str(output_demands[key]) + " allocated " + str(float("{0:.2f}".format(final_share[key]))))

		# aggregate stats
		print ("=============TOTAL STATS====================")
		print ("capacity", total_capacity)
		print ("demand", sum(hostdict.values()))
		print ("amount allocated", sum(final_share.values()))

		return final_share


# Demands = [45,8,50,12,10,12,40]
# hosts = ['1','2','3','4','5','6','7']
# credits =[510,0,252,0,186,0,0]

# credit_min_max(Demands,hosts,credits)
#min_max(Demands,hosts)