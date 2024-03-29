import Rule
import DecTable
import random
'DecTree'
class DecTree:

    def __init__(self, dec_table):
        self.dec_table = dec_table
        self.rules = []
        DecTree.__obtain_rules(self, dec_table)

    def __obtain_rules(self, dec_table, rule=''):
        if  dec_table.table[dec_table.d].nunique()==0:
            # first case:
            # if there are no more rows left
            # i don't know what do to 
            rule += '{}={}'.format(dec_table.d, '?')
            if rule.count("=") > 1:
                self.rules.append(rule)
            return
        elif dec_table.table[dec_table.d].nunique() == 1:
            # second case:
            # if there is only one distinct decision in the subtable
            # the proper rule is appended to tree
            rule += '{}={}'.format(dec_table.d, dec_table.table[dec_table.d].iloc[0])
            if rule.count("=") > 1:
                self.rules.append(rule)
            return
        else:
            # third case:
            # there are two or more distinct decisions in the subtable
            # new random attribute is drawn and the table is divided
            random_attribute = random.choice(list(dec_table.attributes_subset))
            is_one = dec_table.table[random_attribute] == 1
            table_one = dec_table.table[is_one].drop(columns = [random_attribute])
            table_zero = dec_table.table[~ is_one].drop(columns = [random_attribute])
            dec_table_one = DecTable.DecTable.table_to_dectable(table_one)
            dec_table_zero = DecTable.DecTable.table_to_dectable(table_zero)
            rule_one = '{}{}={} '.format(rule, random_attribute, '1')
            rule_zero = '{}{}={} '.format(rule, random_attribute, '0')
            DecTree.__obtain_rules(self, dec_table_one, rule_one)
            DecTree.__obtain_rules(self, dec_table_zero, rule_zero)

    def show(self):
        self.dec_table.show()
        print()
        if self.rules is not None:
            for rule in self.rules:
                print(str(rule))