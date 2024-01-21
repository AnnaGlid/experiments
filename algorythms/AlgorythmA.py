try:
    from . import Rule
except:
    import Rule

def calculate_each_rule(list_of_rules: list,  list_of_agents:list|None=None, list_of_trees:list|None=None):
    """
    This method returns a list of tuples:
    (rule, number of trees for which the rule is true)
    """
    list_of_dec_trees = [agent.dec_tree for agent in list_of_agents] if list_of_agents else list_of_trees
    rule_and_number = []    # list of tuples
    
    for rule_a in list_of_rules:
        num_of_trees = 0
        for tree_b in list_of_dec_trees:
            for rule_b in tree_b.rules:
                if Rule.is_rule_true(rule_a, rule_b):
                    num_of_trees += 1
                    break   # the rule_b loop (next tree_b)
        rule_and_number.append((rule_a, num_of_trees))
    return rule_and_number

def algorythm_a(list_of_agents=None, list_of_rules=None, rule_and_number=None)->tuple[int, list]:
    # rule_and_number is a list of tuples
    if rule_and_number is None:        
        if list_of_agents is None or list_of_rules is None:
            raise ValueError("If rule_and_number is None, list_of_agents and list_of_rules cannot be None")
        else:
            rule_and_number = calculate_each_rule(list_of_agents, list_of_rules)

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


    

