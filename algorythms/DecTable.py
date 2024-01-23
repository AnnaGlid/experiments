import pandas as pd
import numpy as np
import random

class DecTable:
    global decision_sign
    decision_sign = 'd'  # stands for decision, used in DaTaFrame object header

    def __init__(self, attributes_number, rows_number, attributes_subset, table=None):
        self.d = decision_sign
        self.decision_values = [0,1]
        self.attribute_values = [0,1]        
        self.attributes_number = attributes_number
        self.rows_number = rows_number
        self.attributes_subset = attributes_subset
        if table is None:
            self.table = DecTable.__table_fill(self)
        else:
            self.table = table

    @staticmethod
    def csv_table_to_dectable(csv_content: str):
        ''' Turns file like "f1,f2,f3\n0,1,2\n2,4,3" to DecTable'''
        lines = csv_content.split('\n')
        for i in range(len(lines)):
            if lines[i].startswith(','):
                lines[i] = lines[i][1:]
            if lines[i].endswith(','):
                lines[i] = lines[i][:-1]
                
        header_line = next(filter(lambda x: any([sign.isalpha() for sign in x]), lines))
        lines.remove(header_line)
        data = []
        for line in lines:
            elements = [int(el) if el.isnumeric() else el 
                        for el in line.split(',')]
            data.append(elements)        
        table = pd.DataFrame(
            columns = header_line.strip().split(','),
            data=data
        )
        return DecTable.table_to_dectable(table=table)

    @staticmethod
    def table_to_dectable(table):
        attributes_number = len(table.columns) - 1  # minus decision
        rows_number = len(table)
        attributes_subset = list(table.columns) 
        attributes_subset.remove(decision_sign) # minus decision
        return DecTable(attributes_number, 
            rows_number, attributes_subset, table)

    def __table_fill(self):
        """ 
        This method ensures that no row will be duplicated 
        or contradictory in the final decision table.
        """
        header = [attribute for attribute in self.attributes_subset]
        header.append(self.d) 
        rows_list = []
        for i in range(self.rows_number):
            rows_list.append(DecTable.__generate_random_row(self, rows_list))

        decisions_set = set()
        while(True):
            decisions_set.clear()
            for i in range(self.rows_number):
                decision = random.choice(self.decision_values)
                rows_list[i].append(decision)
                decisions_set.add(decision)
            if len(decisions_set) < 2:
                # if each row in whole table
                # got the same decision:
                # delete decision, append decision once again
                for i in range(self.rows_number):
                    rows_list[i].pop(-1)
            else:
                break
        return pd.DataFrame(np.array(rows_list, dtype=object),  columns=header)
            
    def __generate_random_row(self, rows_list):
        """
        Each row contains only attributes values, without decision value.
        """
        row = [random.choice(self.attribute_values) for i in range(len(self.attributes_subset))]
        if row not in rows_list:
            return row
        else:
            return DecTable.__generate_random_row(self,rows_list)

    def show(self):
        print(self.table)


    def __str__(self):
        return str(self.table)
    
    def get_table_str(self, with_index=True):
        return self.table.to_string(index=with_index)

    

