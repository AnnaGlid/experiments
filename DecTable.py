import pandas as pd
import numpy as np
import random

class DecTable:

    def __init__(self, attributes_number, rows_number, attributes_subset):
        self.attributes_number = attributes_number
        self.rows_number = rows_number
        self.attributes_subset = attributes_subset
        self.decision_values = [0,1]
        self.attribute_values = [0,1]
        self.table = DecTable.__table_fill(self)

    def __table_fill(self):
        """ 
        This method ensures that no row will be duplicated 
        or contradictory in the final decision table.
        """

        header = [attribute for attribute in self.attributes_subset]
        header.append('d') # 'd' stands for decision

        rows_list = []
        for i in range(self.rows_number):
            rows_list.append(DecTable.__generate_random_row(self, rows_list))
        for i in range(self.rows_number):
            rows_list[i].append(random.choice(self.decision_values))

        return pd.DataFrame(np.array(rows_list, dtype=object),  columns=header)
            
    def __generate_random_row(self, rows_list):
        """
        Each row contains only attributes values, without decision value.
        """
        row = [random.choice(self.attribute_values) for i in range(self.attributes_number)]
        if row not in rows_list:
            return row
        else:
            return DecTable.__generate_random_row(self,rows_list)

    def show(self):
        print(self.table)

