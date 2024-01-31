from django.test import TestCase
import sys 
sys.path.append('..')
from algorythms import MainInz
from random import randint
from algorythms.DecTree import DecTree


class AlgorythmsTestCase(TestCase):

    def test_generate_tables(self):
        tables_num = randint(5,20)
        rows_num = randint(5,20)
        attributes_num = randint(5,20)
        tables = MainInz.generate_n_tables(
            tables_num=tables_num,
            rows_num=rows_num,
            attributes_num=attributes_num
        )    
        self.assertEqual(len(tables), tables_num)
        for table in tables:
            self.assertEqual(len(table.table), rows_num)
            self.assertEqual(len(table.table.columns), attributes_num + 1)
            table.table.drop(table.table.columns[[-1]], axis=1, inplace=True)
            self.assertFalse(table.table.duplicated().any()) # check for consistency

    def test_tables_consistency(self):
        tables_num = randint(10,30)
        rows_num = randint(10,30)
        attributes_num = randint(10,30)
        tables = MainInz.generate_n_tables(
            tables_num=tables_num,
            rows_num=rows_num,
            attributes_num=attributes_num
        )  
        for table in tables:
            table.table.drop(table.table.columns[[-1]], axis=1, inplace=True)
            self.assertFalse(table.table.duplicated().any()) # check for consistency        
       
    def test_generate_trees(self):
        tables_num = randint(5,20)
        rows_num = randint(5,20)
        attributes_num = randint(5,20)        
        tables = MainInz.generate_n_tables(
            tables_num=tables_num,
            rows_num=rows_num,
            attributes_num=attributes_num
        )            
        for table in tables:
            tree = DecTree(table)
            rules = tree.rules
            self.assertGreater(len(rules), 0)
            max_length = max([rule.count('=')-1 for rule in rules])
            self.assertGreaterEqual(attributes_num, max_length)
            for rule in rules:
                self.assertGreater(rule.count('='), 0)

    def test_algorythm_a(self):
        tables_num = randint(5,20)
        rows_num = randint(5,20)
        attributes_num = randint(5,20)        
        tables = MainInz.generate_n_tables(
            tables_num=tables_num,
            rows_num=rows_num,
            attributes_num=attributes_num
        ) 
        trees = [DecTree(table) for table in tables]               
        max_nr_trees, rules_h = MainInz.heuristic1(trees)
        self.assertGreater(max_nr_trees, 0)
        self.assertGreater(len(rules_h), 0)        

    def test_algorythm_a(self):
        tables_num = randint(5,20)
        rows_num = randint(5,20)
        attributes_num = randint(5,20)        
        tables = MainInz.generate_n_tables(
            tables_num=tables_num,
            rows_num=rows_num,
            attributes_num=attributes_num
        ) 
        trees = [DecTree(table) for table in tables]               
        max_nr_trees, rules_a = MainInz.algorythm_a(trees)
        self.assertGreater(max_nr_trees, 0)
        self.assertGreater(len(rules_a), 0)        



    

    
