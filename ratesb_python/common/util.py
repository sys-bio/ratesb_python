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
    
def check_equal(expr1, expr2, n=10, sample_min=1, sample_max=10):
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
    free_symbols = set(expr1.free_symbols) | set(expr2.free_symbols)
    
    # Numeric (brute force) equality testing n-times
    prev_frac = None
    for i in range(n):
        your_values = [random.uniform(sample_min, sample_max) for _ in range(len(free_symbols))]
        expr1_num=expr1
        expr2_num=expr2
        for symbol,number in zip(free_symbols, your_values):
            expr1_num=expr1_num.subs(symbol, sp.Float(number))
            expr2_num=expr2_num.subs(symbol, sp.Float(number))
        expr1_num=float(expr1_num)
        expr2_num=float(expr2_num)
        if not math.isclose(expr1_num, expr2_num) and (prev_frac is not None and prev_frac != expr1_num/expr2_num):
            return False
        prev_frac = expr1_num/expr2_num
    return True

def check_symbols_derivative(expr, symbols, is_positive_derivative=True):
    """check if the derivative to symbols of a expression are always strictly positive where variables are positive

    Args:
        expr (sympy.Expr): sympy expression to evaluate
        symbols (List): list of symbols to check derivative
        ids_list (List): all symbols in expression
        is_positive_derivative (bool, optional): if we are checking the derivative is positive, checking negative otherwise. Defaults to True.

    Returns:
        bool: if every symbol's derivative if strictly positive if is_positive_derivative, strictively negative if not is_positive_derivative
    """
    # Numeric (brute force) equality testing n-times
    for symbol in symbols:
        temp_expr = expr
        for other_symbol in expr.free_symbols:
            if str(other_symbol) != symbol:
                temp_expr = temp_expr.subs(other_symbol, sp.Float(1))
        if is_positive_derivative:
            prev = -math.inf
        else:
            prev = math.inf
        for i in range(1, 1001, 10):
            curr = sp.Float(temp_expr.subs(symbol, sp.Float(i/100)))
            if is_positive_derivative:
                if curr <= prev:
                    return False
            else:
                if curr >= prev:
                    return False
            prev = curr
    return True