import os
import math
import random
import sympy as sp

def get_model_str(model_reference, is_sbml):
    """
    Get the string representation of the model from model_reference
    
    Args:
        model_reference (str): path to the model
        is_sbml (bool): whether the model is in SBML format

    Raises:
        ValueError: The input xml file is not a valid SBML file.

    Returns:
        str: string representation of the model
    """
    # Get model_str from model_reference
    model_str = ""
    if os.path.isfile(model_reference):
        with open(model_reference, 'r') as fd:
            lines = fd.readlines()
            model_str = ''.join(lines)
    if is_sbml and "<sbml" not in model_str:
        # Antimony
        raise ValueError("Invalid SBML model.")
    return model_str

def get_json_str(json_reference):
    """
    Get the string representation of the json from json_reference
    """
    json_str = ""
    if os.path.isfile(json_reference):
        with open(json_reference, 'r') as fd:
            lines = fd.readlines()
        json_str = ''.join(lines)
    else:
        raise ValueError("Invalid rate law file path.")
    return json_str

def checkSBMLDocument(document): 
    if (document.getNumErrors() > 0):
        print("SBML Document Error")
    
def check_equal(expr1, expr2, n=4, sample_min=1, sample_max=10):
    """check if two sympy expressions are equal by plugging random numbers
    into each symbols in both expressions and test if they are equal

    Args:
        Expr1 (sympy.Expr): first sympy expression to compare
        Expr2 (sympy.Expr): second sympy expression to compare
        n (int, optional): number of test to perform. Defaults to 20.
        sample_min (int, optional): the minimum of random number. Defaults to 1.
        sample_max (int, optional): the maximum of random number. Defaults to 10.
    
    Returns:
        bool: if the two expressions are equal
    """
    # Regroup all free symbols from both expressions
    free_symbols = list(set(expr1.free_symbols) | set(expr2.free_symbols))
    
    # Precompile expressions to numerical functions for faster evaluation
    expr1_func = sp.lambdify(free_symbols, expr1, "numpy")
    expr2_func = sp.lambdify(free_symbols, expr2, "numpy")

    for i in range(n):
        your_values = [random.uniform(sample_min, sample_max) for _ in range(len(free_symbols))]
        
        # Evaluate both expressions with the generated values
        expr1_num = expr1_func(*your_values)
        expr2_num = expr2_func(*your_values)
        
        # Check for numerical closeness
        if not math.isclose(expr1_num, expr2_num, rel_tol=1e-9):
            return False
    return True

def check_kinetics_derivative(kinetics, ids_list, species_list, is_positive_derivative=True):
    """check if the derivative to ids_list of a kinetics are always strictly positive where variables are positive

    Args:
        kinetics (str): kinetics expression
        ids_list (List): all ids in expression
        species_list (List): all species in expression
        is_positive_derivative (bool, optional): if we are checking the derivative is positive, checking negative otherwise. Defaults to True.

    Returns:
        bool: if every symbol's derivative if strictly positive if is_positive_derivative, strictively negative if not is_positive_derivative
    """
    for symbol in ids_list:
        if symbol not in species_list:
            kinetics = kinetics.replace(symbol, "1")
    for species in species_list:
        curr_kinetics = kinetics
        for other_species in species_list:
            if other_species != species:
                curr_kinetics = curr_kinetics.replace(other_species, "1")
        if is_positive_derivative:
            prev = -math.inf
        else:
            prev = math.inf
        for i in range(1, 1001, 10):
            expr = curr_kinetics.replace(species, str(i/100))
            curr = eval(expr)
            if is_positive_derivative:
                if curr <= prev:
                    return False
            else:
                if curr >= prev:
                    return False
            prev = curr
    return True


def add_underscore_to_ids(ids_list, kinetics, ids_to_add):
    """Add "___" to the ids in the ids_list, without changing the original ids_list
        add the new ids to the ids_to_add list
        change the ids in the kinetics to the new ids
    Args:
        ids_list (List): list of ids
        kinetics (str): kinetics expression
        ids_to_add (List): empty list to add the new ids
    
    Returns:
        str: kinetics expression with new ids
    """
    for symbol in ids_list:
        new_id = "___" + symbol
        ids_to_add.append(new_id)
        kinetics = kinetics.replace(symbol, new_id)
    return kinetics

def remove_underscore_from_ids(ids_list, kinetics):
    """Remove "___" from the ids in the kinetics
        ids_list should not contain "___"
    Args:
        ids_list (List): list of ids without "___"
        kinetics (str): kinetics expression
    
    Returns:
        str: kinetics expression with new ids
    """
    
    for symbol in ids_list:
        # assert symbol does not start with "___"
        assert symbol[:3] != "___"
        kinetics = kinetics.replace("___" + symbol, symbol)
    return kinetics