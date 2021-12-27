import unittest
from pathlib import Path
import os, sys

parentdir = Path(__file__).parents[1]
sys.path.append('..')
from src.clean import ISO_check_UTC_convert, check_author, check_count_convert, open_and_load, title_check,check_tags

class CleanTest(unittest.TestCase):
    def setUp(self):  
       self.fixture1 = open_and_load('fixtures/test_1.json')
       self.fixture2 = open_and_load('fixtures/test_2.json')
       self.fixture3 = open_and_load('fixtures/test_3.json')
       self.fixture4 = open_and_load('fixtures/test_4.json')
       self.fixture5 = open_and_load('fixtures/test_5.json')
       self.fixture6 = open_and_load('fixtures/test_6.json')
       self.number_of_elements_tags = len(self.fixture6[0]['tags'])
       
    
   
    def test_creation_date(self):
        self.assertEqual(ISO_check_UTC_convert(self.fixture2),[])

    def test_invalid_dictionaries(self):
        self.assertEqual(self.fixture3,[])

    def test_author(self):
        self.assertEqual(check_author(self.fixture4),[])

    def test_total_count(self):
        self.assertEqual(check_count_convert(self.fixture5),[])

    def test_tags(self):
        self.assertNotEqual(len(check_tags(self.fixture6)[0]['tags']),self.number_of_elements_tags)
    
    def test_title_check(self):
        self.assertEqual(title_check(self.fixture1),[])

         


        
    
if __name__ == '__main__':
    unittest.main()