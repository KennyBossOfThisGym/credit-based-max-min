#!/usr/bin/python3.5

from controller_init import init
from mysql_conn import db_connect
from ssh_conn import ssh_connect
from algorythm import  credit_min_max, min_max
from collector import collect_demands
from fairness import Satisfaction,Ginni
import pickle
#from plots import satisfaction_plot
iteration_time = 30 #iteration time in seconds
credit_edges = [100,300] #calibrate credits gap
iterations = 30 # continious recalculation iterations number 
Sc_dict = {}
S_dict = {}
demands_dict = {}
Wcredit_dict = {}
Wminmax_dict = {}
# 1st step 
init()

# 2nd step
def run_algorythm(iteration_time,credit_edges,iterator):
	
	Sc_dict = {}
	S_dict = {}
	Wcredit_list = []
	Wminmax_list = []
	Sc_list = []
	S_list = []
	cursor,db = db_connect()
	cursor.execute("SELECT D from credit_minmax")
	Demands = [item[0] for item in cursor.fetchall()]
	cursor.execute("SELECT hostname from credit_minmax")
	hostname_list = [item[0] for item in cursor.fetchall()]
	cursor.execute("SELECT credits from credit_minmax")
	credits = [item[0] for item in cursor.fetchall()]
	cursor.execute("SELECT sum_W from credit_minmax")
	sum_W = [item[0] for item in cursor.fetchall()]


	Allocate_dict,new_credits=credit_min_max(Demands,hostname_list,credits,credit_edges,iteration_time)
	
	for key, sumator in zip(sorted(list(Allocate_dict.keys())),sum_W):
		sumator += Allocate_dict[key][0]
		cursor.execute("UPDATE  credit_minmax SET sum_W=%s WHERE hostname=%s",(sumator,key))
	
	for key,credit in zip(sorted(list(Allocate_dict.keys())),new_credits):
		cursor.execute("UPDATE  credit_minmax SET current_W=%s, credits=%s WHERE hostname=%s",(Allocate_dict[key][0],credit,key))
	
	for key,credit in zip(sorted(list(Allocate_dict.keys())),new_credits):
		cursor.execute("UPDATE  credit_minmax SET current_W=%s, credits=%s WHERE hostname=%s",(Allocate_dict[key][0],credit,key))
	
	for key,demand in zip(sorted(list(Allocate_dict.keys())),Demands):
		Sc_list.append(Satisfaction(Allocate_dict[key][0],demand))

	for key in sorted(list(Allocate_dict.keys())):
		Wcredit_list.append(Allocate_dict[key][0]) 

	#Sc_dict[iterator] = Sc_list
	#print (S_dict)
	

	## here the casual min-max starts for same data
	cursor.execute("SELECT D from minmax")
	Demands = [item[0] for item in cursor.fetchall()]
	cursor.execute("SELECT hostname from minmax")
	hostname_list = [item[0] for item in cursor.fetchall()]
	cursor.execute("SELECT sum_W from minmax")
	sum_W = [item[0] for item in cursor.fetchall()]
   

	Allocate_minmax_dict = min_max(Demands,hostname_list)
	
	#min-max updates
	for key in sorted(list(Allocate_minmax_dict.keys())):
		cursor.execute("UPDATE  minmax SET current_W=%s WHERE hostname=%s",(Allocate_minmax_dict[key],key))

	for key, sumator in zip(sorted(list(Allocate_minmax_dict.keys())),sum_W):
		sumator +=  Allocate_minmax_dict[key]
		cursor.execute("UPDATE  minmax SET sum_W=%s WHERE hostname=%s",(sumator,key))

	#print (Demands)
	for key,demand in zip(sorted(list(Allocate_minmax_dict.keys())),Demands):
			S_list.append(Satisfaction(Allocate_minmax_dict[key],demand))

	for key in sorted(list(Allocate_minmax_dict.keys())):
		Wminmax_list.append(Allocate_minmax_dict[key]) 
	
	#S_dict[iterator] = S_list
	db.commit()	
	print ("Credit minmax satisfactions: " + str(Sc_list))
	print ("Minmax satisfactions: " + str(S_list))
	return Sc_list,S_list, Demands, Wcredit_list,Wminmax_list


### count final Ginni fairness
def count_fairness():
	cursor,db = db_connect()
	cursor.execute("SELECT sum_W from credit_minmax")
	Ginni_fairness_credit = Ginni(sorted([item[0] for item in cursor.fetchall()]))

	cursor.execute("SELECT sum_W from minmax")
	Ginni_fairness = Ginni(sorted([item[0] for item in cursor.fetchall()]))

	print (Ginni_fairness_credit)
	print (Ginni_fairness)

### iterate algorythm
for iterator in range(1,iterations+1):
	collect_demands()
	print (' ')
	print ("iteration: " + str(iterator))
	Sc_dict[iterator], S_dict[iterator], demands_dict[iterator],Wcredit_dict[iterator], Wminmax_dict[iterator] = run_algorythm(iteration_time,credit_edges,iterator)
	


#print (Sc_dict)
count_fairness()

with open ("Sc_dict.p","wb") as f:
	pickle.dump(Sc_dict, f, protocol=pickle.HIGHEST_PROTOCOL)

with open ("S_dict.p","wb") as f:
	pickle.dump(S_dict, f, protocol=pickle.HIGHEST_PROTOCOL)

with open ("demands_dict.p","wb") as f:
	pickle.dump(demands_dict, f, protocol=pickle.HIGHEST_PROTOCOL)	

with open ("Wcredit_dict.p","wb") as f:
	pickle.dump(Wcredit_dict, f, protocol=pickle.HIGHEST_PROTOCOL)	 
with open ("Wminmax_dict.p","wb") as f:
	 pickle.dump(Wminmax_dict, f, protocol=pickle.HIGHEST_PROTOCOL)	 


#print (demands_dict)
#print (sorted(Allocate_dict.keys()))



	
	
