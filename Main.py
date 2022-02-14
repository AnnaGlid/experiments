import Agent
import SetS

m_values = [10, 20, 30, 40, 50]     # number of attributes
n_values = [10, 20, 30, 40, 50]     # number of agents
part = 1    # part 1, 2 and three to choose
number_of_iterations = 10      # number of Sets
results = dict()    # {(m,n,k): SetS}, SetS include all required information
                    # max_num_of_trees, length (whole rule) for a, h1, h2

for attributes_number in m_values:
    all_attributes = ['f{}'.format(i) for i in attributes_number]   # f1, f2, ... ,fm
    for agents_number in n_values:    
        for k in range(number_of_iterations):
            set_s = SetS.SetS(all_attributes, attributes_number, agents_number)
            results[(attributes_number, agents_number, k)] = set_s.copy()

'''
here goes writing results to file
'''

