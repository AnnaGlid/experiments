from .Agent import Agent
from . import AlgorythmA, Rule, Heuristics

class SetS:
    def __init__(self, all_attributes, attributes_number, agents_number, part):
        self.all_attributes = all_attributes
        self.attributes_number = attributes_number
        self.agents_number = agents_number
        self.part = part
        self.agents_list = SetS.__create_list_of_agents(self)
        self.rule_and_number = AlgorythmA.calculate_each_rule(self.agents_list, 
            SetS.__list_of_rules_from_agents(self))

        self.max_num_of_trees_a = None
        self.true_rules_a = None
        self.rule_length_a = None
        SetS.__final_algorythm_a(self)  # three properties above are filled
            
        self.max_num_of_trees_h1 = None
        self.true_rules_h1 = None
        self.rule_length_h1 =None
        self.max_num_of_trees_h2 = None
        self.true_rules_h2 = None
        self.rule_length_h2 =None
        SetS.__final_heuristics(self)

    def __create_list_of_agents(self):
        agents_list = []
        for agent in range(self.agents_number):
            agents_list.append(Agent(self.all_attributes, 
                self.attributes_number,  self.part))
        return agents_list

    def __list_of_rules_from_agents(self):
        list_of_rules =[]
        for agent in self.agents_list:
            for rule in agent.dec_tree.rules:
                list_of_rules.append(rule)
        return list_of_rules

    def __final_algorythm_a(self):
        max_num_of_trees, rules_with_max_num_of_trees = AlgorythmA.algorythm_a(rule_and_number = self.rule_and_number)

        self.max_num_of_trees_a = max_num_of_trees
        self.true_rules_a, self.rule_length_a = Rule.choose_shortest_rules(rules_with_max_num_of_trees)
    
    def __final_heuristics(self):
        heuristic = Heuristics.Heuristics(self.rule_and_number)
        list_of_rules = heuristic.heuristic1()
        max_num_of_trees, rules_with_max_num_of_trees = AlgorythmA.algorythm_a(self.agents_list,list_of_rules)
        self.max_num_of_trees_h1 = max_num_of_trees
        self.true_rules_h1, self.rule_length_h1 = Rule.choose_shortest_rules(rules_with_max_num_of_trees)

        list_of_rules = heuristic.heuristic2()
        max_num_of_trees, rules_with_max_num_of_trees = AlgorythmA.algorythm_a(self.agents_list,list_of_rules)
        self.max_num_of_trees_h2 = max_num_of_trees
        self.true_rules_h2, self.rule_length_h2 = Rule.choose_shortest_rules(rules_with_max_num_of_trees)


        
    