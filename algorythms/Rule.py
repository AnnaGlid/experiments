d = 'd'

def is_rule_true(rule_a, rule_b):
    if decision(rule_a) != decision(rule_b):
        return False
    if __rule_length(rule_a) < __rule_length(rule_b):
        return False
    if attributes_set(rule_b).issubset(attributes_set(rule_a)):
        return True
    else:
        return False

def decision(rule):
    # decision is at the end of a rule (0 or 1)
    return rule[-1]

def delete_decision(rule):
    return rule[:rule.find(d)-1]
    # minus one because of the space before decision

def __rule_length(rule):
    # return the number of attributes in a rule
    # minus one because of the decision
    return rule.count('=') - 1 
    
def attributes_set(rule):
    if rule.find(d) > -1:
        rule = delete_decision(rule)  
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
    return result, min_length

def append_attribute(rule, attribute):
    return '{}{} '.format(rule, attribute)

def append_decision(rule, decision):
    return '{}{}={}'.format(rule, d, decision)

def construct_rule_h1(created_rule, chosen_rule):
    result = created_rule
    created_rule_set = attributes_set(created_rule)
    chosen_rule_set = attributes_set(chosen_rule)
    for attribute in chosen_rule_set:
        if attribute not in created_rule_set:
            result = append_attribute(result, attribute)
    return result

def delete_incompatible_rules_h1(list_of_tuples, created_rule):
    tuples_to_delete = []
    for index, tuple in enumerate(list_of_tuples):
        rule = tuple[0]
        if __is_incompatible(created_rule, rule):
            tuples_to_delete.append(tuple)
    for tuple in tuples_to_delete:
        list_of_tuples.remove(tuple)

def delete_incompatible_rules_h2(list_of_rules, created_rule):
    rules_to_delete = []
    for rule in list_of_rules:
        if __is_incompatible(created_rule, rule):
            rules_to_delete.append(rule)
    for rule in rules_to_delete:
        list_of_rules.remove(rule)

def __is_incompatible(created_rule, rule):
    if attributes_set(rule).issubset(attributes_set(created_rule)):
        return True
    created_rule_dict = __rule_to_dict(created_rule.strip())
    rule_dict = __rule_to_dict(rule)
    for key, value in created_rule_dict.items():
        if key in rule_dict and rule_dict[key] != value:
            return True
    return False

def __rule_to_dict(rule):
    result = dict()
    for attribute in attributes_set(rule):
        key, value = attribute.split('=')
        result[key] = value
    return result

def most_common_attribute(list_of_rules, created_rule):
    attributes_num_dict = dict()
    max_num = 0
    max_attribute = 'error'
    for rule in list_of_rules:
        list_of_attributes = list(attributes_set(rule))
        for attribute in list_of_attributes:
            if attribute in attributes_set(created_rule):
                continue
            if attribute in attributes_num_dict:
                attributes_num_dict[attribute] += 1
            else:
                attributes_num_dict[attribute] = 1
            if attributes_num_dict[attribute] > max_num:
                max_num = attributes_num_dict[attribute]
                max_attribute = attribute
    return max_attribute
            






