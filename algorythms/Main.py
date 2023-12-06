import SetS
import os


def iteration_number():
    number = 0
    for attributes_number in m_values:
        for agents_number in n_values:    
            for k in range(number_of_iterations):
                number += 1
    return number

def show_percent_done(now, all):
    print(' %.2f done'%(now/all*100))
        

part = 1    # part 1, 2 and 3 to choose!!
n_values = [10, 20, 30, 40, 50]     # number of agents
number_of_iterations = 10      # number of Sets
results = dict()    # {(m,n,k): SetS}, SetS include all required information
                    # max_num_of_trees, length (whole rule) for a, h1, h2
if part == 1:
    m_values = [10, 20, 30, 40, 50]     # number of attributes
elif part == 2:
    m_values = [5, 10, 15, 20, 25]
else:
    m_values = [20, 40, 60, 80, 100]
file_path = r'D:\repo_inz2\temp\wyniki.txt'


n_values = [20]
m_values =[6]
number_of_iterations = 10


whole = iteration_number()
i = 0

for attributes_number in m_values:
    all_attributes = ['f{}'.format(i) for i in range(attributes_number)]   # f1, f2, ... ,fm
    for agents_number in n_values:    
        for k in range(number_of_iterations):
            set_s = SetS.SetS(all_attributes, attributes_number, agents_number, part)
            results[(attributes_number, agents_number, k)] = set_s
            i += 1
            show_percent_done(i, whole)

'''
here goes writing results to file
'''
folder_path = file_path[:file_path.rfind('\\')]
if not os.path.exists(folder_path):
    os.makedirs( folder_path )

with open(file_path, 'w') as f:
    for key, setS in results.items():
        m = key[0]
        n = key[1]
        k = key[2]
        print('m: {}, n:{}, k:{}\n'.format(m,n,k))

        print('Tables:\n')
        for agent in setS.agents_list:
            agent.dec_tree.show()
            print()
        
        print('\nRules and number of trees for which the rule is true:')
        for tuple in setS.rule_and_number:
            print(tuple)

        print('Algorythm A:')
        print('Max nr of trees: ', setS.max_num_of_trees_a)
        print('Length: ', setS.rule_length_a)
        print('Rule: ', setS.true_rules_a[0])
        print()

        print('Algorythm h1:')
        print('Max nr of trees: ', setS.max_num_of_trees_h1)
        print('Length: ', setS.rule_length_h1)
        print('Rule: ', setS.true_rules_h1[0])
        print()

        print('Algorythm h2:')
        print('Max nr of trees: ', setS.max_num_of_trees_h2)
        print('Length: ', setS.rule_length_h2)
        print('Rule: ', setS.true_rules_h2[0])
        print('=================================================\n')

