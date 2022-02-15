import Agent
import Rule

def algorythm_a(list_of_agents):
    list_of_dec_trees = [agent.dec_tree for agent in list_of_agents]
    rule_and_number = []    # list of tuples
    for tree_a in list_of_dec_trees:
        for rule_a in tree_a:
            num_of_trees = 1
            for tree_b in list_of_dec_trees:
                if list_of_dec_trees.index(tree_a) == list_of_dec_trees.index(tree_b):
                    continue    # if the same trees, go to the next tree_b
                for rule_b in tree_b:
                    if Rule.is_rule_true(rule_a, rule_b):
                        num_of_trees += 1
                        break   # the rule_b loop (next tree_b)
            rule_and_number.append((rule_a, num_of_trees))
    max_num_of_trees = 0
    rules_with_max_num_of_trees = []
    for index, tuple in enumerate(rule_and_number):
        rule = tuple[0]
        num_of_trees = tuple[1]
        if num_of_trees > max_num_of_trees:
            rules_with_max_num_of_trees.clear()
            max_num_of_trees = num_of_trees
        if num_of_trees == max_num_of_trees:
            rules_with_max_num_of_trees.append(rule)
    return max_num_of_trees, rules_with_max_num_of_trees


    

