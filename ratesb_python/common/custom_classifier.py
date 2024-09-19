from itertools import combinations, chain
import json

import sys
import os
current_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(parent_dir)

from common import util
import re
import sympy

# timeout if rate law is too complex
TIMEOUT = 10000

class _CustomClassifier:
    """Custom Classifier for rate laws.

    This classifier validates, classifies and operates helper methods on rate laws.
    
    Attributes:
        rate_law_classifications_path (str): The path to the rate law classifications.
        custom_classifications (list): A list of custom classifications.
        warning_message (str): A message warning about potential issues.
    """
    def __init__(self, rate_law_classifications_path):
        """Constructs all the necessary attributes for the custom classifier object.

        Args:
            rate_law_classifications_path (str): The path to the rate law classifications.
        """
        self.rate_law_classifications_path = rate_law_classifications_path
        self.custom_classifications = []
        self.warning_message = ""
        self.validate()
        
    def validate(self):
        """Validates the rate law classifications file.
        
        It checks if the file is a JSON file, loads the file, and validates its contents.
        """
        splitted_path = os.path.splitext(self.rate_law_classifications_path)
        ext = splitted_path[1]
        if ext != '.json':
            raise ValueError("Invalid file format, accepting .json")
        else:
            # read the file and load the data
            with open(self.rate_law_classifications_path, 'r') as file:
                json_str = file.read()
                unchecked_custom_classifications = json.loads(json_str)

            # This list will be used to collect all warnings
            warnings = []

            # Iterate through each item in the loaded data
            for index, item in enumerate(unchecked_custom_classifications):
                # Perform similar checks as in the JavaScript version
                if (not isinstance(item, dict) or
                    'name' not in item or not isinstance(item['name'], str) or
                    'expression' not in item or not isinstance(item['expression'], str) or
                    'optional_symbols' not in item or not isinstance(item['optional_symbols'], list) or
                    'power_limited_species' not in item or not isinstance(item['power_limited_species'], list)):
                    
                    if 'name' in item and isinstance(item['name'], str):
                        warnings.append(f"Rate law {item['name']} does not follow the correct structure.")
                    else:
                        warnings.append(f"Item at index {index} does not follow the correct structure.")
                    continue

                # Check the mathematical expression validity
                replaced_expression = re.sub(r'(compartment|parameter|reactant1|reactant2|reactant3|product1|product2|product3|enzyme|\*\*|\^)', '1', item['expression'])
                replaced_expression = replaced_expression.replace("**", "^")
                try:
                    # We need a similar library as 'math' in JS for Python, let's use 'eval' here
                    eval(replaced_expression)
                except:
                    warnings.append(f"Rate law {item['name']} has an invalid expression.")
                    continue
                
                valid_optional_symbols = ["compartment", "parameter", "reactant1", "reactant2", "reactant3", "product1", "product2", "product3", "enzyme"]
                
                is_error = False
                for symbol in item["optional_symbols"]:
                    if not isinstance(symbol, str):
                        warnings.append(f"optional_symbols in rate law {item['name']} should be a list of strings.")
                        is_error = True
                        break
                    if symbol not in valid_optional_symbols:
                        warnings.append(f"Invalid item in optional_symbols in rate law {item['name']}, should only contain {', '.join(valid_optional_symbols)}.")
                        is_error = True
                        break
                if is_error:
                    continue
                    
                
                valid_power_limited_species = ["reactant1", "reactant2", "reactant3", "product1", "product2", "product3", "enzyme"]
                
                for symbol in item["power_limited_species"]:
                    if not isinstance(symbol, str):
                        warnings.append(f"power_limited_species in rate law {item['name']} should be a list of strings.")
                        is_error = True
                        break
                    if symbol not in valid_power_limited_species:
                        warnings.append(f"Invalid item in power_limited_species in rate law {item['name']}, should only contain {', '.join(valid_power_limited_species)}.")
                        is_error = True
                        break
                if is_error:
                    continue
                self.custom_classifications.append(item)

            if warnings:
                self.warning_message = 'Some items in your JSON file were invalid and have been removed.\nDetails:\n'
                self.warning_message += '\n'.join(warnings)

    def permute(self, arr):
        """Generates all permutations of a list.

        Args:
            arr (list): The list for which permutations are to be generated.

        Returns:
            list: A list of all permutations.
        """
        if len(arr) == 1:
            return [arr]
        permutations = []
        for i in range(len(arr)):
            remaining = arr[:i] + arr[i+1:]
            subPermutations = self.permute(remaining)
            mappedPermutations = [[arr[i]] + subPermutation for subPermutation in subPermutations]
            permutations.extend(mappedPermutations)
        return permutations

    def replace_occurrences(self, reactants_in_kinetic_law, products_in_kinetic_law, enzyme_list, compartment_in_kinetic_law, parameters_in_kinetic_law_only, kinetics_sim):
        """Replaces the occurrences of different elements in the kinetics_sim with standard terms.

        Args:
            reactants_in_kinetic_law (list): List of reactants in the kinetic law.
            products_in_kinetic_law (list): List of products in the kinetic law.
            enzyme_list (list): List of enzymes in the kinetic law.
            compartment_in_kinetic_law (list): List of compartments in the kinetic law.
            parameters_in_kinetic_law_only (list): List of parameters only present in the kinetic law.
            kinetics_sim (str): The kinetics simulation string.

        Returns:
            list: List of replaced kinetics.
        """
        permuted_reactants = self.permute(reactants_in_kinetic_law) or [[]]
        permuted_products = self.permute(products_in_kinetic_law) or [[]]
        
        ret = []
        symbol_pattern = re.compile(r'\W')
        for reactant_perm in permuted_reactants:
            for product_perm in permuted_products:
                symbols = re.split(symbol_pattern, kinetics_sim)
                replaced_symbols = []
                for symbol in symbols:
                    if symbol in reactant_perm:
                        index = reactant_perm.index(symbol) + 1
                        replaced_symbols.append('reactant' + str(index))
                    elif symbol in product_perm:
                        index = product_perm.index(symbol) + 1
                        replaced_symbols.append('product' + str(index))
                    elif symbol in enzyme_list:
                        replaced_symbols.append('enzyme')
                    elif symbol in compartment_in_kinetic_law:
                        replaced_symbols.append('compartment')
                    elif symbol in parameters_in_kinetic_law_only:
                        replaced_symbols.append('parameter')
                    else:
                        replaced_symbols.append(symbol)
                non_alphanumeric_chars = re.findall(symbol_pattern, kinetics_sim)
                replaced_string = ''.join([symbol + (non_alphanumeric_chars[i] if i < len(non_alphanumeric_chars) else '') for i, symbol in enumerate(replaced_symbols)])
                ret.append(replaced_string)
        return ret

    def custom_classify(self, is_default = False, **kwargs):
        """Classify the provided data according to the rate laws defined in the file.

        Args:
            reactant_list (list): List of all reactants involved in the reaction.
            product_list (list): List of all products generated by the reaction.
            kinetics_sim (str): A string representing the kinetics of the reaction.
            species_in_kinetic_law (list): List of species involved in the kinetics.
            parameters_in_kinetic_law_only (list): List of parameters present only in the kinetics law.
            compartment_in_kinetic_law (list): List of compartments present in the kinetics law.

        Returns:
            list: A list of dictionaries containing the name of the rate law and the result of the comparison.
        """
        reactant_list = kwargs["reactant_list"]
        product_list = kwargs["product_list"]
        kinetics = kwargs["kinetics"]
        species_in_kinetic_law = kwargs["species_in_kinetic_law"]
        parameters_in_kinetic_law_only = kwargs["parameters_in_kinetic_law_only"]
        compartment_in_kinetic_law = kwargs["compartment_in_kinetic_law"]

        reactants_in_kinetic_law = [species for species in species_in_kinetic_law if species in reactant_list]
        products_in_kinetic_law = [species for species in species_in_kinetic_law if species in product_list]

        ret = {}
        enzyme_list = [species for species in species_in_kinetic_law if species not in reactant_list and species not in product_list]
        replaced_kinetics_list = self.replace_occurrences(reactants_in_kinetic_law, products_in_kinetic_law, enzyme_list, compartment_in_kinetic_law, parameters_in_kinetic_law_only, kinetics)
        any_true = False
        for item in self.custom_classifications:
            if any_true and is_default:
                ret[item['name']] = False
                continue
            kinetics_expression = item['expression'].replace("^", "**")
            optional_symbols = item['optional_symbols']
            all_expr = self.get_all_expr(kinetics_expression, optional_symbols)
            all_expr = [sympy.sympify(expr) for expr in all_expr]
            power_limited_species = item['power_limited_species']
            classified_true = False
            try:
                for replaced_kinetics in replaced_kinetics_list:
                    replaced_kinetics_sympify = self.lower_powers(sympy.sympify(replaced_kinetics), power_limited_species)
                    replaced_kinetics_sympify = self.remove_constant_multiplier(replaced_kinetics_sympify)
                    comparison_result = any(util.check_equal(expr, replaced_kinetics_sympify) for expr in all_expr)
                    if comparison_result:
                        ret[item['name']] = True
                        classified_true = True
                        any_true = True
                        break
            except:
                ret[item['name']] = False
                continue
            if not classified_true:
                ret[item['name']] = False
        return ret

    def lower_powers(self, expr, keep=[]):
        """Lowers the power of certain elements in the expression.

        Args:
            expr (sympy.Expr): The expression from which to lower powers.
            keep (list): A list of elements whose power is to be kept as is.

        Returns:
            sympy.Expr: The expression with lowered powers.
        """
        def replace_if_applicable(base, exp):
            """Checks the exponent and base conditions, and returns the base if the conditions meet.
            
            Args:
                base (sympy.Expr): The base part of the expression.
                exp (sympy.Expr): The exponent part of the expression.

            Returns:
                sympy.Expr: The base if conditions are met, otherwise returns the expression as is.
            """
            if exp.is_integer and exp > 1 and base.is_symbol and str(base) not in keep:
                return base
            else:
                return sympy.Pow(base, exp)
        return expr.replace(sympy.Pow, replace_if_applicable)
    
    def remove_constant_multiplier(self, expr):
        """
        Removes constant multipliers from the expression.
        e.g. 2 * x + 3 * y + 4 * z -> x + y + z
        """
        # Split the expression into terms
        expanded_expr = sympy.expand(expr)
        terms = expanded_expr.as_ordered_terms()

        # Process each term to remove constant multipliers while preserving signs
        new_terms = []
        for term in terms:
            # Extract coefficient and rest of the term
            coeff, rest = term.as_coeff_Mul()
            # Preserve sign and remove the multiplier
            new_term = sympy.sign(coeff) * rest
            new_terms.append(new_term)

        # Combine the processed terms back into an expression
        return sympy.Add(*new_terms)

    def get_all_expr(self, expr, optional_symbols):
        """Generates all possible expressions by replacing the optional symbols with 1.

        Args:
            expr (str): The initial expression.
            optional_symbols (list): A list of optional symbols in the expression.

        Returns:
            list: A list of all possible expressions.
        """
        all_combinations = list(chain(*map(lambda x: combinations(optional_symbols, x), range(0, len(optional_symbols)+1))))
        all_expr = []
        all_expr.append(expr)
        def generate_combinations(parts, index, current, add_expr):
            if index == len(parts) - 1:
                add_expr.append(current + parts[index])
                return

            # Add part with the symbol
            generate_combinations(parts, index + 1, current + parts[index] + sym, add_expr)
            
            # Add part with '1' replacing the symbol
            generate_combinations(parts, index + 1, current + parts[index] + "1", add_expr)
        for combo in all_combinations:
            temp_exprs = []
            temp_exprs.append(expr)
            for sym in optional_symbols:
                if sym not in combo:
                    if expr.count(sym) > 1:
                        new_temp_exprs = []
                        for i in range(len(temp_exprs)):
                            parts = temp_exprs[i].split(sym)
                            generate_combinations(parts, 0, "", new_temp_exprs)
                        temp_exprs = new_temp_exprs
                    else:
                        for i in range(len(temp_exprs)):
                            temp_exprs[i] = temp_exprs[i].replace(sym, "1")
                all_expr.extend(temp_exprs)
        return list(set(all_expr))
