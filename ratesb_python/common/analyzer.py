import sys

from ratesb_python.common.custom_classifier import _CustomClassifier
from SBMLKinetics.common.simple_sbml import SimpleSBML
from SBMLKinetics.common.reaction import Reaction
from typing import List, Dict, Optional
from ratesb_python.common import util
from ratesb_python.common.results import Results

import antimony
import libsbml
import os
import re
import sympy as sp


class Analyzer:
    """
    The Analyzer class analyzes SBML models to check if the rate laws are following 
    some rules. It uses sympy for processing mathematical symbol expressions, libsbmlpython 
    for processing SBML models, and SBMLKinetics for analyzing SBML models and classifying 
    rate laws. The class can return errors and warnings based on the specified checks.
    """

    def __init__(self, model_str: str, rate_law_classifications_path: str=None):
        """
        Initializes the Analyzer class.

        Args:
            model_str (str): Path to the model file, or the string representation of model.
            rate_law_classifications_path (str): Path to the rate law classification file.
            customized rate law classification.

        Examples:
            import Analyzer from ratesb-python
            analyzer = Analyzer("path/to/biomodel.xml", "path/to/rate_laws.json")
            analyzer.check_all()
            results = analyzer.results
            print(str(results))
            str(results)
        """
        splitted_path = os.path.splitext(model_str)
        ext = splitted_path[1]
        xml = ''
        if ext == '.ant' or ext == '.txt':
            ant = util.get_model_str(model_str, False)
            load_int = antimony.loadAntimonyString(ant)
            if load_int > 0:
                xml = antimony.getSBMLString()
            else:
                raise ValueError("Invalid Antimony model.")
        elif ext == '.xml':
            xml = util.get_model_str(model_str, True)
        else:
            raise ValueError("Invalid file format, accepting .xml, .ant, and .txt")
        reader = libsbml.SBMLReader()
        document = reader.readSBMLFromString(xml)
        util.checkSBMLDocument(document)
        self.model = document.getModel()
        self.simple = SimpleSBML(self.model)
        self.custom_classifier = None
        self.classification_cp = []
        self.custom_classifications = []
        self.results = Results()
        
        if rate_law_classifications_path:
            self.custom_classifier = _CustomClassifier(rate_law_classifications_path)
            if len(self.custom_classifier.warning_message) > 0:
                print(self.custom_classifier.warning_message)

    def check(self, code: Optional[int]=[]):
        """
        Performs a check based on the provided error or warning code. If no code is provided, 
        all checks are performed.

        Args:
            code (Optional[int]): Code of the check to perform. If None, all checks are performed.

        Prints:
            The results of the check(s).
        """
        if code is None:
            self.check_except([])
        else:
            self.checks([code])
    
    def check_except(self, excluded_codes: Optional[List[int]]=[]):
        """
        Performs all checks except the ones corresponding to the provided list of error or warning codes.

        Args:
            excluded_codes (Optional[List[int]]): List of codes of the checks to exclude. If None, all checks are performed.

        Prints:
            The results of the check(s).
        """
        all_checks = []
        for i in range(1, 3):
            all_checks.append(i)
        for i in range(1001, 1007):
            all_checks.append(i)
        for i in range(1010, 1011):
            all_checks.append(i)
        for i in range(1020, 1023):
            all_checks.append(i)
        for i in range(1030, 1038):
            all_checks.append(i)
        for i in range(1040, 1045):
            all_checks.append(i)
        self.checks(list(set(all_checks) - set(excluded_codes)))
            
    def check_all(self):
        """
        Performs all checks.
        
        Prints:
            The results of the check(s).
        """
        self.check_except()

    def checks(self, codes: Optional[List[int]]=None):
        """
        Performs multiple checks based on the provided list of error or warning codes. If no codes are provided, 
        all checks are performed.

        Args:
            codes (Optional[List[int]]): List of codes of the checks to perform. If None, all checks are performed.

        Prints:
            The results of the check(s).
        """
        self.classification_cp = []
        self.custom_classifications = []
        self.results.clear_results()
        
        for reaction in self.simple.reactions:
            reaction.kinetic_law.formula = reaction.kinetic_law.formula.replace('^','**')
            
            reactant_list = [r.getSpecies() for r in reaction.reactants]
            product_list = [p.getSpecies() for p in reaction.products]
            
            reactant_stg = " + ".join(
                [r.getSpecies() for r in reaction.reactants])
            product_stg = " + ".join(
                [p.getSpecies() for p in reaction.products])
        
            kinetic_law = reaction.kinetic_law
            
            species_num = self.simple.model.getNumSpecies()
            parameter_num = self.simple.model.getNumParameters()
            compartment_num = self.simple.model.getNumCompartments()

            species_list = []
            parameter_list = []
            compartment_list = []
            for i in range(species_num):
                species = self.simple.model.getSpecies(i)
                species_id = species.getId()
                species_list.append(species_id)

            for i in range(parameter_num):
                parameter = self.simple.model.getParameter(i)
                parameter_id =  parameter.getId()
                parameter_list.append(parameter_id)
            
            for i in range(compartment_num):
                compartment = self.simple.model.getCompartment(i)
                compartment_id =  compartment.getId()
                compartment_list.append(compartment_id)
                
            kinetics = reaction.kinetic_law.expanded_formula
            
            try:
                kinetics_sim = str(sp.simplify(kinetics))
            except:
                kinetics_sim = kinetics

            ids_list = list(dict.fromkeys(reaction.kinetic_law.symbols))

            species_in_kinetic_law = []
            parameters_in_kinetic_law_only = []
            compartment_in_kinetic_law = []
            others_in_kinetic_law = []

            for id in ids_list:
                if id in species_list:
                    species_in_kinetic_law.append(id)
                elif id in parameter_list:
                    parameters_in_kinetic_law_only.append(id)
                elif id in compartment_list:
                    compartment_in_kinetic_law.append(id)
                    others_in_kinetic_law.append(id)
                else:
                    others_in_kinetic_law.append(id)

            parameters_in_kinetic_law = parameters_in_kinetic_law_only + others_in_kinetic_law

            #only for MM, MMcat and FR
            if len(reactant_list) != 0:
                ids_list += reactant_list # some rcts/prds also needs symbols definition
            if len(product_list) != 0:
                ids_list += product_list
            ids_list = list(dict.fromkeys(ids_list))
            
            boundary_species = [reactant for reactant in reactant_list if self.simple.model.getSpecies(reactant).getBoundaryCondition()]
            boundary_species += [product for product in product_list if self.simple.model.getSpecies(product).getBoundaryCondition()]
            
            kwargs = {"reaction": reaction, "kinetics": kinetics, "kinetics_sim": kinetics_sim, \
            "reactant_list": reactant_list, "product_list": product_list, \
            "species_in_kinetic_law": species_in_kinetic_law, "parameters_in_kinetic_law": parameters_in_kinetic_law, \
            "ids_list": ids_list, "boundary_species": boundary_species, "parameters_in_kinetic_law_only": parameters_in_kinetic_law_only, \
            "compartment_in_kinetic_law": compartment_in_kinetic_law, "reaction": reaction, "codes": codes}
            
            self._set_kinetics_type(**kwargs)
            if 1 in codes:
                self._check_empty_kinetics(**kwargs)
            if 2 in codes:
                self._check_floating_species(**kwargs)
            if 1001 in codes:
                self._check_pure_number(**kwargs)
            if 1002 in codes:
                self._check_unrecognized_rate_law(**kwargs)
            if 1003 in codes:
                self._check_flux_increasing_with_reactant(**kwargs)
            if 1004 in codes:
                self._check_flux_decreasing_with_product(**kwargs)
            if 1005 in codes:
                self._check_boundary_floating_species(**kwargs)
            if 1006 in codes:
                self._check_constant_parameters(**kwargs)
            if 1010 in codes:
                self._check_irreversibility(**kwargs)
            if 1020 in codes or 1021 in codes or 1022 in codes:
                self._check_naming_conventions(**kwargs)
            if any(isinstance(num, int) and 1030 <= num <= 1037 for num in codes):
                self._check_formatting_conventions(**kwargs)
            if any(isinstance(num, int) and 1040 <= num <= 1044 for num in codes):
                self._check_sbterm_annotations(**kwargs)
            
            # self._check_empty_kinetics(**kwargs)
            # self._check_boundary_floating_species(**kwargs)
            

    def _set_kinetics_type(self, **kwargs):
        reaction = kwargs["reaction"]
        self.classification_cp.append([#needs to be in order
            reaction.kinetic_law.isZerothOrder(**kwargs),
            # reaction.kinetic_law.isPowerTerms(**kwargs),
            reaction.kinetic_law.isUNDR(**kwargs),
            reaction.kinetic_law.isUNMO(**kwargs),
            reaction.kinetic_law.isBIDR(**kwargs),
            reaction.kinetic_law.isBIMO(**kwargs),
            reaction.kinetic_law.isMM(**kwargs),
            reaction.kinetic_law.isMMcat(**kwargs),
            reaction.kinetic_law.isHill(**kwargs),
            reaction.kinetic_law.isFraction(**kwargs),
            #reaction.kinetic_law.isPolynomial(**kwargs),
        ])
        if self.custom_classifier:
            self.custom_classifications.append(self.custom_classifier.custom_classify(**kwargs))

    def _check_empty_kinetics(self, **kwargs):
        """
        Checks if the given reaction has an empty kinetic law.
        Code: 1
        
        Args:
            reaction (object): The reaction object to check.

        Adds:
            An error message to results specifying that no rate law was entered for the reaction.
        """
        reaction = kwargs["reaction"]
        if len(reaction.kinetic_law.formula.replace(' ', '')) == 0:
            self.results.add_message(reaction.getId(), 1, f"No rate law entered.", False)
    
    def _check_floating_species(self, **kwargs):
        """
        Checks if all reactants in the rate law of the given reaction are defined as species, excluding boundary species.
        Code: 2
        
        Args:
            reaction (object): The reaction object to check.
            species_in_kinetic_law (list): A list of species present in the rate law.
            reactant_list (list): A list of reactants for the reaction.
            boundary_species (list): A list of boundary species in the model.

        Adds:
            An error message to results specifying the missing reactants that are expected in the rate law.
        """
        reaction = kwargs["reaction"]
        species_in_kinetic_law = kwargs["species_in_kinetic_law"]
        reactant_list = kwargs["reactant_list"]
        boundary_species = kwargs["boundary_species"]
        
        floating_species = []
        for reactant in reactant_list:
            if reactant not in species_in_kinetic_law:
                if reactant not in boundary_species:
                    floating_species.append(reactant)
        if len(floating_species) > 0:
            floating_species = ",".join(floating_species)
            self.results.add_message(reaction.getId(), 2, f"Expecting reactants in rate law: {floating_species}", False)
    
    def _check_pure_number(self, **kwargs):
        """
        Checks if the rate law contains only number
        Code: 1001
        
        Args:
            reaction: The reaction object to check
            kinetics_sim: string-simplified kinetics

        Adds:
            A warning message to results specifying that the rate law contains only numbers.
        """
        reaction = kwargs["reaction"]
        kinetics_sim = kwargs["kinetics_sim"]
        try:
            float(kinetics_sim)
            self.results.add_message(reaction.getId(), 1001, "Rate law contains only number.")
        except:
            return
    
    def _check_unrecognized_rate_law(self, **kwargs):
        """
        Checks if the rate law from the standard and custom list (if given) is recognized
        Code: 1002

        Args:
            reaction: The reaction object to check.
            standard_rate_laws: The list of standard rate laws.

        Adds:
            A warning message to results specifying that the rate law is unrecognized.
        """
        reaction = kwargs["reaction"]
        if len(self.custom_classifications) > 0:
            if not (any(self.classification_cp[-1]) or any(item["comparison_result"] for item in self.custom_classifications[-1])):
                self.results.add_message(reaction.getId(), 1002, "Unrecognized rate law from the standard list and the custom list.")
        else:
            if not any(self.classification_cp[-1]):
                self.results.add_message(reaction.getId(), 1002, "Unrecognized rate law from the standard list.")
    
    def _check_flux_increasing_with_reactant(self, **kwargs):
        """
        Checks if the flux is increasing as the reactant increases.
        Code: 1003

        Args:
            reaction: The reaction object to check.

        Adds:
            A warning message to results specifying if the flux is not increasing as reactant increases.
        """
        reaction = kwargs["reaction"]
        reactant_list = kwargs["reactant_list"]
        kinetics = kwargs["kinetics"]

        if not util.check_symbols_derivative(sp.sympify(kinetics), reactant_list):
            self.results.add_message(reaction.getId(), 1003, "Flux is not increasing as reactant increases.")

    def _check_flux_decreasing_with_product(self, **kwargs):
        """
        Checks if the flux is increasing as the product decreases.
        Code: 1004

        Args:
            reaction: The reaction object to check.

        Adds:
            A warning message to results specifying if the flux is not decreasing as product increases.
        """
        reaction = kwargs["reaction"]
        product_list = kwargs["product_list"]
        kinetics = kwargs["kinetics"]
        
        if reaction.reaction.getReversible():
            if not util.check_symbols_derivative(sp.sympify(kinetics), product_list, False):
                self.results.add_message(reaction.getId(), 1004, "Flux is not decreasing as product increases.")

    def _check_boundary_floating_species(self, **kwargs):
        """
        Checks if any reactant in the rate law of the given reaction is a boundary species.
        Code: 1005
        
        Args:
            reaction: The reaction object to check.
            species_in_kinetic_law: A list of species present in the rate law.
            reactant_list: A list of reactants for the reaction.
            boundary_species: A list of boundary species in the model.

        Adds:
            A warning message to results specifying the boundary species reactants found in the rate law.
        """
        reaction = kwargs["reaction"]
        species_in_kinetic_law = kwargs["species_in_kinetic_law"]
        reactant_list = kwargs["reactant_list"]
        boundary_species = kwargs["boundary_species"]
        
        boundary_floating_species = []
        for reactant in reactant_list:
            if reactant not in species_in_kinetic_law:
                if reactant in boundary_species:
                    boundary_floating_species.append(reactant)
        if len(boundary_floating_species) > 0:
            boundary_floating_species = ",".join(boundary_floating_species)
            self.results.add_message(reaction.getId(), 1005, f"Expecting boundary species reactant in rate law: {boundary_floating_species}")

    def _check_constant_parameters(self, **kwargs):
        """
        Checks if the parameters in the rate law are constants.
        Code: 1006

        Args:
            reaction: The reaction object to check.

        Adds:
            A warning message to results specifying if the parameters are not constants.
        """
        reaction = kwargs["reaction"]
        parameters_in_kinetic_law_only = kwargs["parameters_in_kinetic_law_only"]
        non_constant_params = []
        for param in parameters_in_kinetic_law_only:
            libsbml_param = self.simple.model.getParameter(param)
            if not libsbml_param.getConstant():
                non_constant_params.append(param)
        if len(non_constant_params) > 0:
            non_constant_params = ",".join(non_constant_params)
            self.results.add_message(reaction.getId(), 1006, f"Expecting boundary species reactant in rate law: {non_constant_params}")

    def _check_irreversibility(self, **kwargs):
        """
        Checks if an irreversible reaction's kinetic law contains products.
        Code: 1010

        Args:
            reaction: The reaction object to check.
            species_in_kinetic_law: A list of species present in the rate law.
            product_list: A list of products for the reaction.

        Returns:
            An error message specifying the products found in the rate law of an irreversible reaction.
        """
        reaction = kwargs["reaction"]
        species_in_kinetic_law = kwargs["species_in_kinetic_law"]
        product_list = kwargs["product_list"]
        
        inconsistent_products = []
        if not reaction.reaction.getReversible():
            for product in product_list:
                if product in species_in_kinetic_law:
                    inconsistent_products.append(product)
        if len(inconsistent_products) > 0:
            inconsistent_products = ",".join(inconsistent_products)
            self.results.add_message(reaction.getId(), 1010, f"Irreversible reaction kinetic law contains products: {inconsistent_products}")

    def _check_naming_conventions(self, **kwargs):
        """
        Checks if certain parameters in the rate law follow the recommended naming convention (starting with 'k', 'K', or 'V').
        Code: 1020, 1021, 1022

        Args:
            reaction (object): The reaction object to check.

        Adds:
            A warning message to results specifying that certain parameters in the rate law are not following the recommended naming convention.
        """
        reaction = kwargs["reaction"]
        parameters_in_kinetic_law = kwargs["parameters_in_kinetic_law"]
        kinetics_sim = kwargs["kinetics_sim"]
        ids_list = kwargs["ids_list"]
        codes = kwargs["codes"]
        
        naming_convention_warnings = {'k': [], 'K': [], 'V': []}
        classifications = self.classification_cp[-1]
        if classifications[0]:
            naming_convention_warnings['k'] = self._check_symbols_start_with('k', parameters_in_kinetic_law)
        elif classifications[1]:
            naming_convention_warnings['k'] = self._check_symbols_start_with('k', parameters_in_kinetic_law)
        elif classifications[2]:
            naming_convention_warnings['k'] = self._check_symbols_start_with('k', parameters_in_kinetic_law)
        elif classifications[3]:
            naming_convention_warnings['k'] = self._check_symbols_start_with('k', parameters_in_kinetic_law)
        elif classifications[4]:
            naming_convention_warnings['k'] = self._check_symbols_start_with('k', parameters_in_kinetic_law)
        elif classifications[5]:
            eq = self._numerator_denominator(kinetics_sim, ids_list)
            eq0 = [param for param in parameters_in_kinetic_law if param in eq[0]]
            eq1 = [param for param in parameters_in_kinetic_law if param in eq[1]]
            naming_convention_warnings['V'] = self._check_symbols_start_with('V', eq0)
            naming_convention_warnings['K'] = self._check_symbols_start_with('K', eq1)
        elif classifications[6]:
            eq = self._numerator_denominator(kinetics_sim, ids_list)
            eq0 = [param for param in parameters_in_kinetic_law if param in eq[0]]
            eq1 = [param for param in parameters_in_kinetic_law if param in eq[1]]
            naming_convention_warnings['K'] = self._check_symbols_start_with('K', eq0)
            naming_convention_warnings['K'] = self._check_symbols_start_with('K', eq1)
        elif classifications[7]:
            eq = self._numerator_denominator(kinetics_sim, ids_list)
            eq0 = [param for param in parameters_in_kinetic_law if param in eq[0]]
            eq1 = [param for param in parameters_in_kinetic_law if param in eq[1]]
            naming_convention_warnings['K'] = self._check_symbols_start_with('K', eq1)
        # add elif for "Fraction" and "Polynomial" if needed
        
        if 1020 in codes and len(naming_convention_warnings['k']) > 0:
            naming_convention_warnings_k = ",".join(naming_convention_warnings['k'])
            self.results.add_message(reaction.getId(), 1020, f"We recommend that these parameters start with 'k': {naming_convention_warnings_k}")
        if 1021 in codes and len(naming_convention_warnings['K']) > 0:
            naming_convention_warnings_K = ",".join(naming_convention_warnings['K'])
            self.results.add_message(reaction.getId(), 1021, f"We recommend that these parameters start with 'K': {naming_convention_warnings_K}")
        if 1022 in codes and len(naming_convention_warnings['V']) > 0:
            naming_convention_warnings_V = ",".join(naming_convention_warnings['V'])
            self.results.add_message(reaction.getId(), 1022, f"We recommend that these parameters start with 'V': {naming_convention_warnings_V}")

    def _check_symbols_start_with(self, start, symbols):
        ret = []
        for symbol in symbols:
            if not symbol.startswith(start):
                ret.append(symbol)
        return ret

    def _numerator_denominator(self, kinetics_sim, ids_list):
        """
        Get the numerator and denominator of a "fraction" function.
        
        Parameters
        ----    
        kinetics_sim: string-simplified kinetics
        ids_list: list-id list including all the ids in kinetics, reactants and products

        Returns
        -------
        Type - the numerator and the denominator of the fraction
        """

        strange_func = 0 
        pre_symbols = ''
        for i in range(len(ids_list)):
            pre_symbols += ids_list[i]
            pre_symbols += ' '
        pre_symbols = pre_symbols[:-1] #remove the space at the end
        pre_symbols_comma = pre_symbols.replace(" ",",")
        stmt = "%s = sp.symbols('%s')"%(pre_symbols_comma,pre_symbols)
        try: #sometimes there is "invalid syntax error"
            exec(stmt,globals())
        except:
            strange_func = 1
        
        try: #check if there is strange func (i.e. delay) in kinetic law; 
            #sometimes ids_list is not enough for all the ids in kinetics
            eq_stat = "kinetics_eq = " + kinetics_sim
            exec(eq_stat,globals())
        except:
            strange_func = 1

        eq = ['', '']
        
        if strange_func == 0:
            try: 
                numerator = str(kinetics_eq.as_numer_denom()[0])
                denominator = str(kinetics_eq.as_numer_denom()[1])
                eq[0] = numerator
                eq[1] = denominator
            except:
                pass

        return eq

    def _numerator_denominator_order_remained(self, kinetics, ids_list):
        # Split the fraction at the '/' character
        split_fraction = kinetics.split('/')

        # Check if there's a numerator and a denominator
        if len(split_fraction) != 2:
            return ['','']

        # Return the numerator and the denominator as a tuple
        return split_fraction[0].strip(), split_fraction[1].strip()
    
    def _find_positions_in_rate_law(self, element_list, rate_law):
        largest_position = -1
        smallest_position = sys.maxsize
        prev_position = -1
        increasing_flag = True

        for element in element_list:
            pattern = re.compile(rf"\b{re.escape(element)}\b")
            match = pattern.search(rate_law)
            if match:
                index = match.start()
                largest_position = max(index, largest_position)
                smallest_position = min(index, smallest_position)
                if index < prev_position:
                    increasing_flag = False
                prev_position = index
        return largest_position, smallest_position, increasing_flag

    def _check_product_of_terms_format(self, kinetics, compartment_in_kinetic_law, parameters_in_kinetic_law_only, sorted_species_reference):
        comp_stats = self._find_positions_in_rate_law(compartment_in_kinetic_law, kinetics)
        param_stats = self._find_positions_in_rate_law(parameters_in_kinetic_law_only, kinetics)
        sorted_species = []
        for species_reference in sorted_species_reference:
            sorted_species.append(species_reference.getSpecies())
        spec_stats = self._find_positions_in_rate_law(sorted_species, kinetics)
        is_formatted = (comp_stats[0] < param_stats[1] or param_stats[1] == sys.maxsize) and \
                       (param_stats[0] < spec_stats[1] or spec_stats[1] == sys.maxsize) and \
                       (comp_stats[0] < spec_stats[1] or spec_stats[1] == sys.maxsize)
        increasing_flag = comp_stats[2] and param_stats[2] and spec_stats[2]
        if is_formatted:
            return 0 if increasing_flag else 1
        return 2
    
    def _check_expression_format(self, kinetics, compartment_in_kinetic_law, parameters_in_kinetic_law_only, reaction: Reaction):
        compartment_in_kinetic_law.sort()
        parameters_in_kinetic_law_only.sort()
        product_of_terms = re.split(r"[+-]", kinetics)
        ret = 0
        for term in product_of_terms:
            format_status = self._check_product_of_terms_format(term, compartment_in_kinetic_law, parameters_in_kinetic_law_only, reaction.reactants + reaction.products)
            if format_status > ret:
                ret = format_status
        return ret
    
    def _check_formatting_conventions(self, **kwargs):
        reaction = kwargs["reaction"]
        compartment_in_kinetic_law = kwargs["compartment_in_kinetic_law"]
        kinetics = kwargs["kinetics"]
        ids_list = kwargs["ids_list"]
        parameters_in_kinetic_law_only = kwargs["parameters_in_kinetic_law_only"]
        codes = kwargs["codes"]
        
        flag = 0
        assert len(self.classification_cp) > 0
        if self.classification_cp[-1][5] or self.classification_cp[-1][6] or self.classification_cp[-1][7] or self.classification_cp[-1][8]:
            eq = self._numerator_denominator_order_remained(kinetics, ids_list)  # _numerator_denominator not provided
            flag = self._check_expression_format(eq[0], compartment_in_kinetic_law, parameters_in_kinetic_law_only, reaction)
            flag += 3 * self._check_expression_format(eq[1], compartment_in_kinetic_law, parameters_in_kinetic_law_only, reaction)
        else:
            flag = self._check_expression_format(kinetics, compartment_in_kinetic_law, parameters_in_kinetic_law_only, reaction)
        if flag == 1 and 1030 in codes:
            self.results.add_message(reaction.getId(), 1030, f"Elements of the same type are not ordered properly")
        if flag == 2 and 1031 in codes:
            self.results.add_message(reaction.getId(), 1031, f"Formatting convention not followed (compartment before parameters before species)")
        if flag == 3 and 1032 in codes:
            self.results.add_message(reaction.getId(), 1032, f"Denominator not in alphabetical order")
        if flag == 4 and 1033 in codes:
            self.results.add_message(reaction.getId(), 1033, f"Numerator and denominator not in alphabetical order")
        if flag == 5 and 1034 in codes:
            self.results.add_message(reaction.getId(), 1034, f"Numerator convention not followed and denominator not in alphabetical order")
        if flag == 6 and 1035 in codes:
            self.results.add_message(reaction.getId(), 1035, f"Denominator convention not followed")
        if flag == 7 and 1036 in codes:
            self.results.add_message(reaction.getId(), 1036, f"Numerator not in alphabetical order and denominator convention not followed")
        if flag == 8 and 1037 in codes:
            self.results.add_message(reaction.getId(), 1037, f"Numerator and denominator convention not followed")

    def _check_sbterm_annotations(self, **kwargs):
        """
        Checks if the SBOTerm annotations for the rate law follow recommended SBO terms.
        Code: 1040, 1041, 1042, 1043, 1044

        Args:
            reaction (object): The reaction object to check.

        Adds:
            A warning message to results specifying that the annotations for the rate law do not follow recommended SBO terms.
        """
        reaction: Reaction = kwargs["reaction"]
        codes = kwargs["codes"]
        libsbml_kinetics = reaction.kinetic_law.libsbml_kinetics
        assert len(self.classification_cp) > 0
        classifications = self.classification_cp[-1]
        flag = 0
        if libsbml_kinetics:
            sbo_term = libsbml_kinetics.getSBOTerm()
            if sbo_term < 0:
                flag = 0
            elif classifications[1]:
                undrSBOs = [41, 43, 44, 45, 47, 49, 50, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 140, 141, 142, 143, 144, 145, 146, 163, 166, 333, 560, 561, 562, 563, 564, 430, 270, 458, 275, 273, 379, 440, 443, 451, 454, 456, 260, 271, 378, 387, 262, 265, 276, 441, 267, 274, 444, 452, 453, 455, 457, 386, 388, 442, 277, 445, 446, 447, 448, 266, 449, 450]
                if sbo_term not in undrSBOs:
                    flag = 1
            elif classifications[2]:
                unmoSBOs = [41, 43, 44, 45, 47, 49, 50, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 140, 141, 142, 143, 144, 145, 146, 163, 166, 333, 560, 561, 562, 563, 564]
                if sbo_term not in unmoSBOs:
                    flag = 2
            elif classifications[3] or classifications[4]:
                biSBOs = [42, 69, 78, 88, 109, 646, 70, 71, 74, 79, 80, 81, 84, 89, 99, 110, 120, 130, 72, 73, 75, 76, 77, 82, 83, 85, 86, 87, 90, 91, 92, 95, 100, 101, 102, 105, 111, 112, 113, 116, 121, 122, 123, 126, 131, 132, 133, 136, 93, 94, 96, 97, 98, 103, 104, 106, 107, 108, 114, 115, 117, 118, 119, 124, 125, 127, 128, 129, 134, 135, 137, 138, 139]
                if sbo_term not in biSBOs:
                    flag = 3
            elif classifications[5]:
                mmSBOs = [28, 29, 30, 31, 199]
                if sbo_term not in mmSBOs:
                    flag = 4
            elif classifications[6]:
                mmcatSBOs = [28, 29, 30, 31, 199, 430, 270, 458, 275, 273, 379, 440, 443, 451, 454, 456, 260, 271, 378, 387, 262, 265, 276, 441, 267, 274, 444, 452, 453, 455, 457, 386, 388, 442, 277, 445, 446, 447, 448, 266, 449, 450]
                if sbo_term not in mmcatSBOs:
                    flag = 5
            elif classifications[7]:
                hillSBOs = [192, 195, 198]
                if sbo_term not in hillSBOs:
                    flag = 6
        if flag == 1 and 1040 in codes:
            self.results.add_message(reaction.getId(), 1040, f"Uni-directional mass action annotation not following recommended SBO terms, we recommend annotations to be subclasses of: SBO_0000430, SBO_0000041")
        elif flag == 2 and 1041 in codes:
            self.results.add_message(reaction.getId(), 1041, f"Uni-term with the moderator annotation not following recommended SBO terms, we recommend annotations to be subclasses of: SBO_0000041")
        elif flag == 3 and 1042 in codes:
            self.results.add_message(reaction.getId(), 1042, f"Bi-directional mass action or Bi-terms with the moderator annotation not following recommended SBO terms, we recommend annotations to be subclasses of: SBO_0000042")
        elif flag == 4 and 1043 in codes:
            self.results.add_message(reaction.getId(), 1043, f"Michaelis-Menten kinetics without an explicit enzyme annotation not following recommended SBO terms, we recommend annotations to be subclasses of: SBO_0000028")
        elif flag == 5 and 1044 in codes:
            self.results.add_message(reaction.getId(), 1044, f"Michaelis-Menten kinetics with an explicit enzyme annotation not following recommended SBO terms, we recommend annotations to be subclasses of: SBO_0000028, SBO_0000430")

                