import unittest
import sys
import os
# setting path
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
common_dir = os.path.join(parent_dir, 'ratesb_python', 'common')
sys.path.append(common_dir)

from results import Results

class TestResults(unittest.TestCase):
    def setUp(self):
        self.results = Results()
    
    def tearDown(self):
        self.results = None

    def test_add_message(self):
        self.results.add_message("reaction_name", 1, "message")
        self.assertEqual(self.results.count_errors(), 0)
        self.assertEqual(self.results.count_warnings(), 1)
        self.assertEqual(self.results.results, {"reaction_name": [{"code": 1, "message": "message", "is_warning": True}]})
        self.results.add_message("reaction_name", 2, "message", is_warning=False)
        self.assertEqual(self.results.count_errors(), 1)
        self.assertEqual(self.results.count_warnings(), 1)
        self.assertEqual(self.results.results, {"reaction_name": [{"code": 1, "message": "message", "is_warning": True}, {"code": 2, "message": "message", "is_warning": False}]})
    
    def test_clear_results(self):
        self.results.add_message("reaction_name", 1, "message")
        self.results.clear_results()
        self.assertEqual(self.results.count_errors(), 0)
        self.assertEqual(self.results.count_warnings(), 0)
        self.assertEqual(self.results.results, {})
    
    def test_get_warnings(self):
        self.results.add_message("reaction_name", 1, "message")
        self.results.add_message("reaction_name", 2, "message", is_warning=False)
        self.assertEqual(self.results.get_warnings(), {"reaction_name": [{"code": 1, "message": "message", "is_warning": True}]})
    
    def test_get_errors(self):
        self.results.add_message("reaction_name", 1, "message")
        self.results.add_message("reaction_name", 2, "message", is_warning=False)
        self.assertEqual(self.results.get_errors(), {"reaction_name": [{"code": 2, "message": "message", "is_warning": False}]})
        
    def test_get_messages_by_reaction(self):
        self.results.add_message("reaction_name", 1, "message")
        self.results.add_message("reaction_name", 2, "message", is_warning=False)
        self.assertEqual(self.results.get_messages_by_reaction("reaction_name"), [{"code": 1, "message": "message", "is_warning": True}, {"code": 2, "message": "message", "is_warning": False}])
        self.assertEqual(self.results.get_messages_by_reaction("reaction_name2"), [])
    
    def test_remove_messages_by_reaction(self):
        self.results.add_message("reaction_name", 1, "message")
        self.results.add_message("reaction_name", 2, "message", is_warning=False)
        self.results.remove_messages_by_reaction("reaction_name")
        self.assertEqual(self.results.count_errors(), 0)
        self.assertEqual(self.results.count_warnings(), 0)
        self.assertEqual(self.results.results, {})
    
    def test_count_messages(self):
        self.results.add_message("reaction_name", 1, "message")
        self.results.add_message("reaction_name", 2, "message", is_warning=False)
        self.assertEqual(self.results.count_messages(), 2)
    
if __name__ == '__main__':
    unittest.main()