try:
    from . import AlgorythmA, Rule
except:
    import AlgorythmA, Rule

class Heuristics:
    def __init__(self, rule_and_number):    
        # rule_and_number - list of tuples
        self.decision_rules_dict = Heuristics.__create_decision_rules_dict(self, 
            rule_and_number)
        # decision_rules_dict - {decision: [(rule without decision, num_of_trees),...]}
        
    def heuristic1(self):
        obtained_rules = []
        for decision, list_of_tuples in self.decision_rules_dict.items():
            list_of_tuples_copy = list_of_tuples.copy()
            created_rule = ''
            while list_of_tuples_copy:  # not empty
                max_num, rules_with_max_num = AlgorythmA.algorythm_a(rule_and_number=list_of_tuples_copy)
                chosen_rule = Rule.choose_shortest_rules(rules_with_max_num)[0][0]
                created_rule = Rule.construct_rule_h1(created_rule, chosen_rule)
                Rule.delete_incompatible_rules_h1(list_of_tuples_copy, created_rule)
            created_rule = Rule.append_decision(created_rule, decision)
            obtained_rules.append(created_rule)
        return obtained_rules

    def heuristic2(self):
        obtained_rules = []
        for decision, list_of_tuples in self.decision_rules_dict.items():
            list_of_rules = [tuple[0] for tuple in list_of_tuples]
            created_rule = ''
            while list_of_rules:
                most_common_attribute = Rule.most_common_attribute(list_of_rules, created_rule)
                created_rule = Rule.append_attribute(created_rule, most_common_attribute)
                Rule.delete_incompatible_rules_h2(list_of_rules, created_rule)
            created_rule = Rule.append_decision(created_rule, decision)
            obtained_rules.append(created_rule)
        return obtained_rules


    def __create_decision_rules_dict(self, rule_and_number):
        result = dict()
        for index, tuple in enumerate(rule_and_number):
            rule = tuple[0]
            number = tuple[1]
            decision = Rule.decision(rule)
            rule = Rule.delete_decision(rule)
            if decision not in result:
                result[decision] = []                
            result[decision].append((rule, number))
        return result




