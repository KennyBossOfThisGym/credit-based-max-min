# masters-project-max-min
This project is a set of emulation and postprocessing scripts, which are used to calculate and analyze credit-based max-min fairness algorithm inside of isolated environments (my masters degree project).
# Credit-based Max-min fairness
Requires docker container with mysql + n number of empty containers for network emulation

Adjust following values in main.py and start:\
iteration_time = 30 #iteration time in seconds\
credit_edges = [100,300] #calibrate credits gap\
iterations = 30 # continious recalculation iterations number

