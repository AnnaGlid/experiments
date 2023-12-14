import random
from .DecTree import DecTree
from .DecTable import DecTable

class Agent:
    def __init__(self, all_attributes, attributes_number, part):
        self.part = part
        self.attributes_number = attributes_number
        self.columns_number = Agent.__number_of_columns(self)
        self.rows_number = Agent.__number_of_rows(self)

        self.attributes_subset = random.sample(all_attributes, self.columns_number)
        dec_table = DecTable(self.columns_number, 
            self.rows_number, self.attributes_subset)
        self.dec_tree = DecTree(dec_table)

    def __number_of_columns(self):
        if self.part == 1:
            return self.attributes_number // 2
        elif self.part == 2:
            return self.attributes_number
        else:   # self.part == 3
            return self.attributes_number // 4

    def __number_of_rows(self):
            if self.part == 1:
                return self.attributes_number
            elif self.part == 2:
                return self.attributes_number * 2
            else:   # self.part == 3
                return self.attributes_number // 2
