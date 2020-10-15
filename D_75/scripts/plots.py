#!/usr/bin/python3.5
import numpy as np
import matplotlib.pyplot as plt
from fairness import Jane,Jane_single,Nowicki
import pickle
host = 1
iterations = 30
J_credit = []
J_minmax = []
J_single_credit = []
J_single_minmax = []
N_credit = []
N_minmax = []

def satisfaction_plot(Sc_dict,S_dict,iterations,host):
	Sc_medium_credit = []
	S_medium_minmax = []
	plotlist = np.ndarray(shape=(len(Sc_dict), len(Sc_dict[1])))
	plotlist_minmax = np.ndarray(shape=(len(S_dict), len(S_dict[1])))
		


	for key in sorted(list(Sc_dict.keys())):
		plotlist[key-1] = Sc_dict[key]

	for key in sorted(list(S_dict.keys())):
		plotlist_minmax[key-1] = S_dict[key]

	#for key in sorted(list(Sc_dict.keys())):

	#print (plotlist)
	plt.title('Host Satisfaction plot')
	plt.plot(range(1, iterations+1),plotlist[:,host-1],'ko-',label="credit-minmax")
	plt.plot(range(1, iterations+1),plotlist_minmax[:,host-1],'rv-',label="minmax")
	plt.xlabel('iteration(n)')
	plt.ylabel('Satisfaction[0,1]')
	plt.legend(loc='best', ncol=2, shadow=True, fancybox=True)
	plt.axis([1,iterations+1, 0, 2])

	#plt.show()
	plt.savefig('satisfaction_plot.png')
	plt.show()
	plt.clf()

	for key in sorted(list(Sc_dict.keys())):
		Sc_medium_credit.append(sum(Sc_dict[key])/len(Sc_dict[key]))
	for key in sorted(list(Sc_dict.keys())):
		S_medium_minmax.append(sum(S_dict[key])/len(S_dict[key]))

	plt.title('Mean Satisfaction plot')
	plt.plot(range(1, iterations+1),Sc_medium_credit,'ko-',label="credit-minmax")
	plt.plot(range(1, iterations+1),S_medium_minmax,'rv-',label="minmax")
	plt.xlabel('iteration(n)')
	plt.ylabel('Satisfaction[0,1]')
	plt.legend(loc='best', ncol=2, shadow=True, fancybox=True)
	plt.axis([1,iterations+1, 0, 2])

	#plt.show()
	plt.savefig('satisfaction_mean_plot.png')
	plt.show()
	plt.clf()






def demand_plot(demands_dict,iterations,host):
	demands_median = []
	demandslist = np.ndarray(shape=(len(demands_dict), len(demands_dict[1])))
	for key in sorted(list(demands_dict.keys())):
		demandslist[key-1] = demands_dict[key]

	plt.title('Demands plot')
	plt.plot(range(1, iterations+1),demandslist[:,host-1],'mo-',label="Demands")
	plt.xlabel('iteration(n)')
	plt.ylabel('Demands(%)')
	plt.legend(loc='best', ncol=2, shadow=True, fancybox=True)
	plt.axis([1,iterations+1, 0, 100])

	#plt.show()
	plt.savefig('demand_plot.png')
	plt.show()

	for key in sorted(list(demands_dict.keys())):
		demands_median.append(sum(demands_dict[key])/len(demands_dict[key]))


	plt.title('Mean Demands plot')
	plt.plot(range(1, iterations+1),demands_median,'mo-',label="Mean Demands")
	plt.xlabel('iteration(n)')
	plt.ylabel('Demands(%)')
	plt.legend(loc='best', ncol=2, shadow=True, fancybox=True)
	plt.axis([1,iterations+1, 0, 100])
	plt.savefig('demand_mean_plot.png')
	plt.show()
	plt.clf()
def allocation_plot(Wcredit_dict,Wminmax_dict,iterations,host):
	alloc_median = []
	Wcredit_list = np.ndarray(shape=(len(demands_dict), len(Wcredit_dict[1])))
	Wminmax_list = np.ndarray(shape=(len(demands_dict), len(Wminmax_dict	[1])))
	for key in sorted(list(Wcredit_dict.keys())):
		Wcredit_list[key-1] = Wcredit_dict[key]
	for key in sorted(list(Wminmax_dict.keys())):
		Wminmax_list[key-1] = Wminmax_dict[key]

	plt.title('Allocation plot')
	plt.plot(range(1, iterations+1),Wcredit_list[:,host-1],'bo-',label="credit-minmax allocation")
	plt.plot(range(1, iterations+1),Wminmax_list[:,host-1],'yv-',label="minmax allocation")
	plt.xlabel('iteration(n)')
	plt.ylabel('Allocation[0,100]')
	plt.legend(loc='best', ncol=2, shadow=True, fancybox=True)
	plt.axis([1,iterations+1, 0, 20])

	#plt.show()
	plt.savefig('allocation_plot.png')
	plt.show()
	plt.clf()


	for key in sorted(list(Wcredit_dict.keys())):
		alloc_median.append(sum(Wcredit_dict[key])/len(Wcredit_dict[key]))

	plt.title('Mean Allocation plot')
	plt.plot(range(1, iterations+1),alloc_median,'bo-',label="Mean allocation")
	#plt.plot(range(1, iterations+1),100/len(Wminmax_dict[1]),'yv-',label="Medium minmax allocation")
	plt.xlabel('iteration(n)')
	plt.ylabel('Allocation[0,100]')
	plt.legend(loc='best', ncol=2, shadow=True, fancybox=True)
	plt.axis([1,iterations+1, 0, 20])
	plt.savefig('allocation_mean_plot.png')
	plt.show()
	plt.clf()
	
def Jain_plot(J_credit,J_minmax,J_single_credit,J_single_minmax,iterations):

	jain_mean_credit = []
	jain_mean_minmax = []
	for i in J_credit:
		jain_mean_credit.append(sum(J_credit)/len(J_credit))
	for i in J_minmax:
		jain_mean_minmax.append(sum(J_minmax)/len(J_minmax))


	plt.title('Jaine plot')
	plt.plot(range(1, iterations+1),J_credit,'bo-',label="Jaine for credit min-max")
	plt.plot(range(1, iterations+1),J_minmax,'yv-',label="Jaine for min-max")
	plt.plot(range(1, iterations+1),jain_mean_credit,'b--',label="Mean Jaine (cr. min-max)")
	plt.plot(range(1, iterations+1),jain_mean_minmax,'y--',label="Mean Jaine (min-max)")
	plt.xlabel('iteration(n)')
	plt.ylabel('Jaine[0,1]')
	plt.legend(loc='best', ncol=2, shadow=True, fancybox=True)
	plt.axis([1,iterations+1, 0, 1.2])

	#plt.show()
	plt.savefig('jaine_plot.png')
	plt.show()
	plt.clf()


	plt.title('Single host fairness plot')
	plt.plot(range(1, iterations+1),J_single_credit,'bo-',label="Single host fairness (cr. min-max)")
	plt.plot(range(1, iterations+1),J_single_minmax,'yv-',label="Single host fairness (min-max)")
	plt.xlabel('iteration(n)')
	plt.ylabel('Single host fairness ')
	plt.legend(loc='best', ncol=2, shadow=True, fancybox=True)
	plt.axis([1,iterations+1, 0, 2])

	#plt.show()
	plt.savefig('jaine_single_plot.png')
	plt.show()
	plt.clf()
def Nowicki_plot(N_credit,N_minmax,iterations):

	nowicki_mean_credit= []
	nowicki_mean_minmax= []

	for i in N_credit:
		nowicki_mean_credit.append(sum(N_credit)/len(N_credit))
	for i in N_minmax:
		nowicki_mean_minmax.append(sum(N_minmax)/len(N_minmax))
	
	plt.title('Nowicki plot')
	plt.plot(range(1, iterations+1),N_credit,'bo-',label="Nowicki for credit min-max")
	plt.plot(range(1, iterations+1),N_minmax,'yv-',label="Nowicki for min-max")
	plt.plot(range(1, iterations+1),nowicki_mean_credit,'b--',label="Mean Nowicki (cr. min-max)")
	plt.plot(range(1, iterations+1),nowicki_mean_minmax,'y--',label="Mean Nowicki (min-max)")

	plt.xlabel('iteration(n)')
	plt.ylabel('Nowicki[0,1]')
	plt.legend(loc='best', ncol=2, shadow=True, fancybox=True)
	plt.axis([1,iterations+1, 0, 1.2])

	#plt.show()
	plt.savefig('nowicki_plot.png')
	plt.show()
	plt.clf()



with open("Sc_dict.p", 'rb') as f:
	Sc_dict = pickle.load(f)
with open("S_dict.p", 'rb') as f:
	S_dict = pickle.load(f)

with open("demands_dict.p", 'rb') as f:
	demands_dict = pickle.load(f)          

with open("Wcredit_dict.p", 'rb') as f:
	Wcredit_dict = pickle.load(f) 
with open("Wminmax_dict.p", 'rb') as f:
	Wminmax_dict = pickle.load(f)     

for key in sorted(list(Wcredit_dict.keys())):
	J_credit.append(Jane(Wcredit_dict[key])) 
	J_single_credit.append(Jane_single(Wcredit_dict[key],host))
	N_credit.append(Nowicki(Wcredit_dict[key]))


for key in sorted(list(Wminmax_dict.keys())):
	J_minmax.append(Jane(Wminmax_dict[key]))
	J_single_minmax.append(Jane_single(Wminmax_dict[key],host))
	N_minmax.append(Nowicki(Wminmax_dict[key]))



satisfaction_plot(Sc_dict,S_dict,iterations,host)
demand_plot(demands_dict,iterations,host)
allocation_plot(Wcredit_dict,Wminmax_dict,iterations,host)
Jain_plot(J_credit,J_minmax,J_single_credit,J_single_minmax,iterations)
Nowicki_plot(N_credit,N_minmax,iterations)



print (sum(J_credit))
print (sum(J_minmax))
#print (demands_dict)
