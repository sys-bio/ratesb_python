import os
import math
import random
import sympy as sp

def get_model_str(model_reference, is_sbml):
    model_str = ""
    if isinstance(model_reference, str):
        if os.path.isfile(model_reference):
            with open(model_reference, 'r') as fd:
                lines = fd.readlines()
                model_str = ''.join(lines)
                if len(model_str) == 0:
                    if "readlines" in dir(model_reference):
                        lines = model_reference.readlines()
                    if len(lines) > 0 and isinstance(lines[0], bytes):
                        lines = [l.decode("utf-8") for l in lines]
                        model_str = ''.join(lines)
                        model_reference.close()
                    elif len(lines) == 0:
                        model_str = ''
                    else:
                        # Must be a string representation of a model
                        model_str = model_reference
        else:
            raise ValueError("Invalid model path!")
        # Process model_str into a model
        if is_sbml and "<sbml" not in model_str:
            # Antimony
            raise ValueError("Invalid SBML model.")
        return model_str
    else:
        raise ValueError("Invalid model_str format, should be string.")

def get_json_str(json_reference):
    json_str = ""
    if isinstance(json_reference, str):
        if os.path.isfile(json_reference):
            with open(json_reference, 'r') as fd:
                lines = fd.readlines()
            json_str = ''.join(lines)
        else:
            ValueError("Invalid rate law json file.")
    else:
        ValueError("Invalid json path.")
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
    """check if the derivative to symbols of a expression are always strictly positive

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
        for i in range(100, 1001, 10):
            curr = sp.Float(temp_expr.subs(symbol, sp.Float(i/100)))
            if is_positive_derivative:
                if curr <= prev:
                    return False
            else:
                if curr >= prev:
                    return False
            prev = curr
    return True