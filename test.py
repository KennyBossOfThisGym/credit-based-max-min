#! /usr/bin/python
# Calculate weighted max min fair allocations

import copy
# INPUT : Desired Rates, Weights, capacity
desired={1:10, 2:14, 3:7, 4:40, 5:20,6:17,7:30}
weights={1:0,2:0,3:0,4:0,5:0,6:0,7:0}
total_capacity=100

# OUTPUT: Allocations.
final_share=dict()

# book-keeping
current_share=dict()
for user in desired :
	current_share[user]=0
capacity = total_capacity

# core algm
while  ( len(weights) > 0 ) and ( capacity > 0 ) :
	unit_share   = capacity;
	user_list = weights.keys()
	for user in user_list :
		fair_share = unit_share * weights[ user ];
		current_share[ user ] += fair_share
		if current_share[ user ] >= desired[ user ] :
			spare_capacity = (current_share[ user ] - desired[ user ]);
			final_share[ user ] = desired[ user ]
			del current_share[ user ]
			del weights[ user ]
			capacity = capacity + spare_capacity - fair_share;
		else :
			capacity = capacity - fair_share ;

# finalize allocations
for share in current_share :
	final_share[share]=current_share[share]

# print
for share in final_share :
	bottleneck=True
	if final_share[share] == desired[share] :
		bottleneck=False
	print "user ", share,"weight %.5f"%weight_copy[share],"desired %7.0f"%desired[share],"allocated %7.0f"%final_share[share]," bottleneck ",bottleneck

# aggregate stats
print "=============TOTAL STATS===================="
print "capacity", total_capacity
print "demand", sum(desired.values())
print "amount allocated", sum(final_share.values())

