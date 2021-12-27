import unittest
#from pathlib import Path
import os, sys
#parentdir = Path(__file__).parents[1]
sys.path.append('..')
import json
import pandas as pd

from src.compile_word_counts import count_them
from src.compute_pony_lang import count_dict



class TasksTest(unittest.TestCase):
    
    def setUp(self):
        dir = os.path.dirname(__file__)
        self.mock_dialog = os.path.join(dir, 'fixtures', 'mock_dialog.csv')
        self.true_word_counts = os.path.join(dir, 'fixtures', 'word_counts.true.json')
        self.true_tf_idfs = os.path.join(dir, 'fixtures', 'tf_idfs.true.json')
        
       
        
    def test_task1(self):
        # use  self.mock_dialog and self.true_word_counts; REMOVE self.assertTrue(True) and write your own assertion, i.e. self.assertEquals(...)
        with open(self.true_word_counts,'r') as f:
            fix1 = json.load(f)
        mock = pd.read_csv(self.mock_dialog)
        mock = mock[['pony','dialog']]
        test_case = count_them(mock)
        self.assertEqual(fix1,test_case)
    
    def test_task2(self):
        # use self.true_word_counts self.true_tf_idfs; REMOVE self.assertTrue(True) and write your own assertion, i.e. self.assertEquals(...)
        with open(self.true_tf_idfs, "r") as f:
            fix2 = json.load(f)
        mock = pd.read_csv(self.mock_dialog)
        mock = mock[['pony','dialog']]
        test_case = count_them(mock)
        self.assertEqual(fix2,count_dict(test_case,1))
    
    
        
    
if __name__ == '__main__':
    unittest.main()