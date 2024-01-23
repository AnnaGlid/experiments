try:    
    from .DecTable import DecTable
    from .DecTree import DecTree
    from . import AlgorythmA
    from . import Rule
    from .Heuristics import Heuristics
    from .TreesVis import TreeVis
except:
    from DecTable import DecTable
    from DecTree import DecTree
    import AlgorythmA
    import Rule
    from Heuristics import Heuristics
    from TreesVis import TreeVis


# import consts
import os
import random


def iterations_number(m_values: list, n_values: list, iters: int):
    number = 0
    for attributes_number in m_values:
        for agents_number in n_values:    
            for k in range(iters):
                number += 1
    return number

def show_percent_done(now, all):
    print(' %.2f done'%(now/all*100))
        
results = dict()    # {(m,n,k): SetS}, SetS include all required information
                    # max_num_of_trees, length (whole rule) for a, h1, h2


def generate_tables(m_values: list, n_values: list, iters: int, file_path: None|str=None, save: bool=False):
    i = 0
    dec_tables = []
    whole = iterations_number(m_values=m_values, n_values=n_values, iters=iters)
    # if save:
    #     file_path = file_path if file_path != None else TABLES_PATH
    for attributes_number in m_values:
        all_attributes = ['f{}'.format(i) for i in range(attributes_number)]   # f1, f2, ... ,fm
        columns_number = attributes_number // 2 # DEPENDS
        for agents_number in n_values:    
            for k in range(iters):
                dec_tables.append(DecTable(
                    attributes_number=attributes_number,
                    rows_number=attributes_number,
                    attributes_subset=random.sample(all_attributes, columns_number)
                ))
                # set_s = SetS.SetS(all_attributes, attributes_number, agents_number)
                # results[(attributes_number, agents_number, k)] = set_s
                i += 1
                show_percent_done(i, whole)    
    return dec_tables

def generate_n_tables(tables_num: int, attributes_num: int, rows_num: int) -> list[DecTable]:
    tables = []
    for j in range(tables_num):
        tables.append(
            DecTable(attributes_number=attributes_num,
                     rows_number=rows_num,
                     attributes_subset=[f'f{i}' for i in range(1, attributes_num+1)])
            )
    return tables

def algorythm_a(list_of_trees: list[DecTree])->tuple[int, list]:
    all_rules = []
    for tree in list_of_trees:
        all_rules.extend(tree.rules)
    rule_and_number = AlgorythmA.calculate_each_rule(list_of_rules=all_rules, list_of_trees=list_of_trees)
    return AlgorythmA.algorythm_a(rule_and_number=rule_and_number)
    
def calculate_support(tables: list, rule: str)-> int:
    return Rule.calculate_support_for_tables(tables=tables, rule=rule)

def heuristic1(list_of_trees: list[DecTree]):
    all_rules = []
    for tree in list_of_trees:
        all_rules.extend(tree.rules)
    rule_and_number = AlgorythmA.calculate_each_rule(list_of_rules=all_rules, list_of_trees=list_of_trees)
    heu = Heuristics(rule_and_number)
    rules_h =  heu.heuristic1()
    rule_and_number_h = AlgorythmA.calculate_each_rule(list_of_rules=rules_h, list_of_trees=list_of_trees)
    return AlgorythmA.algorythm_a(rule_and_number=rule_and_number_h)

def save_trees_to_file(list_of_trees: list[DecTree], folder_path: str):
    ''' Save each tree to png (visualisation) as filenames "1.png", "2.png", etc'''
    folder_path = f'{folder_path}/' if not folder_path.endswith('/') else folder_path
    for idx, tree in enumerate(list_of_trees):
        rules = tree.rules
        vis = TreeVis(rules, 'd')
        vis.construct_tree()
        vis.draw(show=False, save=True, path=f'{folder_path}{idx+1}.png')


#region old
'''
here goes writing results to file
'''
file_path = "DEBUG"
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

# generate_tables(
#     [5,10],
#     [5, 10],
#     5
# )
        
#endregion