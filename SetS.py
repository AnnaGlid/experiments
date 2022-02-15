import Agent
import AlgorythmA
import Rule

class SetS:
    def __init__(self, all_attributes, attributes_number, agents_number, part):
        self.all_attributes = all_attributes
        self.attributes_number = attributes_number
        self.agents_number = agents_number
        self.part = part
        self.agents_list = SetS.__create_list_of_agents(self)

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

    def __create_list_of_agents(self):
        agents_list = []
        for agent in range(self.agents_number):
            agents_list.append(Agent.Agent(self.all_attributes, 
                self.attributes_number,  self.part))
        return agents_list

    def __final_algorythm_a(self):
        max_num_of_trees, rules_with_max_num_of_trees = AlgorythmA.algorythm_a(self.agents_list)
        self.max_num_of_trees_a = max_num_of_trees
        self.true_rules_a, self.rule_length_a = Rule.choose_shortest_rules(rules_with_max_num_of_trees)
        
    