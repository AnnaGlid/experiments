import random
import DecTree

class Agent:
    def __init__(self, all_attributes, number_of_attributes, dec_table):
        self.attributes_subset = random.sample(all_attributes, number_of_attributes)
        self.dec_tree = DecTree.DecTree(dec_table)


