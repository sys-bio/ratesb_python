import unittest
import sys
import os
import sympy as sp
# setting path
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
common_dir = os.path.join(parent_dir, 'ratesb_python', 'common')
sys.path.append(common_dir)

from util import get_model_str, get_json_str, check_equal, check_kinetics_derivative, add_underscore_to_ids, remove_underscore_from_ids

class TestUtil(unittest.TestCase):
    def test_get_model_str(self):
        model_str = get_model_str(os.path.join(current_dir, "test_models", "test_util.ant"), False)
        self.assertEqual(model_str, "model test_util()\n    J0: S1 -> S2; k1*S1;\n    S1 = 1.0;\n    S2 = 0.0;\n    k1 = 0.1;\nend")
        try:
            model_str = get_model_str(os.path.join(current_dir, "test_models", "test_util.ant"), True)
        except ValueError as e:
            self.assertEqual(str(e), "Invalid SBML model.")
        else:
            self.fail("ValueError not raised.")
        
    
    def test_get_json_str(self):
        json_str = get_json_str(os.path.join(current_dir, "test_models", "test_util.json"))
        self.assertEqual(json_str, '{"J0": {"type": "MASS_ACTION", "parameters": ["k1"], "reactants": ["S1"], "products": ["S2"]}}')
        try:
            json_str = get_json_str(os.path.join(current_dir, "test_models", "test_util3.json"))
        except ValueError as e:
            self.assertEqual(str(e), "Invalid rate law file path.")
        else:
            self.fail("ValueError not raised.")
    
    def test_check_equal(self):
        x, y, z = sp.symbols('x y z')
        expr1 = x + y + z
        expr2 = x + z + y
        expr3 = x + y + z + 1
        expr4 = x + y + 1.1 * z
        expr5 = x + y + z + 1.1
        expr6 = x + y + z + 1.1 * z
        expr7 = x + y + z + 1.1 * x
        expr8 = x - y + z + 2.0 * y
        
        self.assertTrue(check_equal(expr1, expr2))
        self.assertTrue(check_equal(expr1, expr8))
        self.assertTrue(check_equal(expr2, expr8))
        
        self.assertFalse(check_equal(expr1, expr3))
        self.assertFalse(check_equal(expr1, expr4))
        self.assertFalse(check_equal(expr1, expr5))
        self.assertFalse(check_equal(expr1, expr6))
        self.assertFalse(check_equal(expr1, expr7))
        self.assertFalse(check_equal(expr2, expr3))
        self.assertFalse(check_equal(expr2, expr4))
        self.assertFalse(check_equal(expr2, expr5))
        self.assertFalse(check_equal(expr2, expr6))
        self.assertFalse(check_equal(expr2, expr7))
        self.assertFalse(check_equal(expr3, expr4))
        self.assertFalse(check_equal(expr3, expr5))
        self.assertFalse(check_equal(expr3, expr6))
        self.assertFalse(check_equal(expr3, expr7))
        self.assertFalse(check_equal(expr4, expr5))
        self.assertFalse(check_equal(expr4, expr6))
        self.assertFalse(check_equal(expr4, expr7))
        self.assertFalse(check_equal(expr5, expr6))
        self.assertFalse(check_equal(expr5, expr7))
        self.assertFalse(check_equal(expr6, expr7))
    
    def test_check_kinetics_derivative(self):
        expr1 = "x + y + z"
        expr2 = "x + z - 2 * y"
        expr3 = "1 / x"
        expr4 = "x * y * z"
        expr5 = "x * y / (1 + y)"
        symbols = ["x", "y", "z"]
        
        self.assertTrue(check_kinetics_derivative(expr1, symbols, symbols))
        self.assertFalse(check_kinetics_derivative(expr1, symbols, symbols, False))
        self.assertFalse(check_kinetics_derivative(expr2, symbols, symbols))
        self.assertFalse(check_kinetics_derivative(expr2, symbols, symbols, False))
        self.assertTrue(check_kinetics_derivative(expr3, symbols, ["x"], False))
        self.assertFalse(check_kinetics_derivative(expr3, symbols, ["x"]))
        self.assertTrue(check_kinetics_derivative(expr4, symbols, symbols))
        self.assertFalse(check_kinetics_derivative(expr4, symbols, symbols, False))
        self.assertTrue(check_kinetics_derivative(expr5, symbols, ["x", "y"]))
        self.assertFalse(check_kinetics_derivative(expr5, symbols, ["x", "y"], False))
    
    def test_add_underscore_to_ids(self):
        ids_list = ["x", "y", "z"]
        kinetics = "x + y + z"
        ids_to_add = []
        kinetics = add_underscore_to_ids(ids_list, kinetics, ids_to_add)
        self.assertEqual(kinetics, "___x + ___y + ___z")
        self.assertEqual(ids_to_add, ["___x", "___y", "___z"])
        self.assertEqual(ids_list, ["x", "y", "z"])
    
    def test_remove_underscore_from_ids(self):
        ids_list = ["x", "y", "z"]
        kinetics = "___x + ___y + ___z"
        kinetics = remove_underscore_from_ids(ids_list, kinetics)
        self.assertEqual(kinetics, "x + y + z")
        self.assertEqual(ids_list, ["x", "y", "z"])

if __name__ == "__main__":
    unittest.main()