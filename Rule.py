
def is_rule_true(rule_a, rule_b):
    if __decision(rule_a) != __decision(rule_b):
        return False
    if __rule_length(rule_a) < __rule_length(rule_b):
        return False
    if __attributes_set(rule_b).issubset(__attributes_set(rule_a)):
        return True
    else:
        return False

def __decision(rule):
    # decision is at the end of a rule
    return rule[-1]

def __rule_length(rule):
    # return the number of attributes in a rule
    # minus one because of the decision
    return rule.count('=') - 1 
    
def __attributes_set(rule):
    rule = rule[:rule.find('d')-1]  
    # minus one because of the space before decision
    return set(rule.split(' '))

def choose_shortest_rules(rules_list):
    min_length = 100
    result = []
    for rule in rules_list:
        if __rule_length(rule) < min_length:
            result.clear()
            min_length = __rule_length(rule)
        if __rule_length(rule) == min_length:
            result.append(rule)
    return result
