from dataclasses import dataclass
import json
import sys
import os
current_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(current_dir)
sys.path.append(parent_dir)

from custom_classifier import _CustomClassifier
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", 
        category=SyntaxWarning,
        module="SBMLKinetics.kinetics_output"
    )
    from SBMLKinetics.common.simple_sbml import SimpleSBML
    from SBMLKinetics.common.reaction import Reaction
from typing import List
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", 
        category=SyntaxWarning,
        module="SBMLKinetics.kinetics_output"
    )
    from SBMLKinetics import kinetics_output
from common import util
from results import Results

import antimony
import libsbml
import os
import sympy as sp

sp

from typing import List

ZERO = "ZERO"
UNDR1 = "UNDR1"
UNDR2 = "UNDR2"
UNDR3 = "UNDR3"
UNDR_A1 = "UNDR-A1"
UNDR_A2 = "UNDR-A2"
UNDR_A3 = "UNDR-A3"
BIDR11 = "BIDR11"
BIDR12 = "BIDR12"
BIDR21 = "BIDR21"
BIDR22 = "BIDR22"
BIDR_A11 = "BIDR-A11"
BIDR_A12 = "BIDR-A12"
BIDR_A21 = "BIDR-A21"
BIDR_A22 = "BIDR-A22"
MM = "MM"
MM_CAT = "MMcat"
AMM = "AMM"
IMM = "IMM"
RMM = "RMM"
RMM_CAT = "RMMcat"
HILL = "Hill"

NON_MM_KEYS = [
    ZERO, UNDR1, UNDR2, UNDR3, UNDR_A1, UNDR_A2, UNDR_A3,
    BIDR11, BIDR12, BIDR21, BIDR22, BIDR_A11, BIDR_A12, BIDR_A21, BIDR_A22
]

MM_KEYS = [MM, MM_CAT, AMM, IMM, RMM, RMM_CAT]

UNDR_KEYS = [UNDR1, UNDR2, UNDR3]

UNDR_A_KEYS = [UNDR_A1, UNDR_A2, UNDR_A3]

BIDR_ALL_KEYS = [BIDR11, BIDR12, BIDR21, BIDR22,
                 BIDR_A11, BIDR_A12, BIDR_A21, BIDR_A22]

MM_CAT_KEYS = [MM_CAT, AMM, IMM, RMM_CAT]

UNDR_SBOS = [41, 43, 44, 45, 47, 49, 50, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 140, 141, 142, 143, 144, 145, 146, 163, 166, 333, 560, 561, 562, 563, 564, 430, 270, 458,
             275, 273, 379, 440, 443, 451, 454, 456, 260, 271, 378, 387, 262, 265, 276, 441, 267, 274, 444, 452, 453, 455, 457, 386, 388, 442, 277, 445, 446, 447, 448, 266, 449, 450]

UNDR_A_SBOS = [41, 43, 44, 45, 47, 49, 50, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61,
               140, 141, 142, 143, 144, 145, 146, 163, 166, 333, 560, 561, 562, 563, 564]

BI_SBOS = [42, 69, 78, 88, 109, 646, 70, 71, 74, 79, 80, 81, 84, 89, 99, 110, 120, 130, 72, 73, 75, 76, 77, 82, 83, 85, 86, 87, 90, 91, 92, 95, 100, 101, 102, 105, 111, 112,
           113, 116, 121, 122, 123, 126, 131, 132, 133, 136, 93, 94, 96, 97, 98, 103, 104, 106, 107, 108, 114, 115, 117, 118, 119, 124, 125, 127, 128, 129, 134, 135, 137, 138, 139]

MM_SBOS = [28, 29, 30, 31, 199]

MM_CAT_SBOS = [28, 29, 30, 31, 199, 430, 270, 458, 275, 273, 379, 440, 443, 451, 454, 456, 260, 271, 378, 387,
               262, 265, 276, 441, 267, 274, 444, 452, 453, 455, 457, 386, 388, 442, 277, 445, 446, 447, 448, 266, 449, 450]

HILL_SBOS = [192, 195, 198]

ALL_CHECKS = []
ERROR_CHECKS = []
WARNING_CHECKS = []
for i in range(1, 3):
    ALL_CHECKS.append(i)
    ERROR_CHECKS.append(i)
for i in range(1001, 1007):
    ALL_CHECKS.append(i)
    WARNING_CHECKS.append(i)
for i in range(1010, 1011):
    ALL_CHECKS.append(i)
    WARNING_CHECKS.append(i)
for i in range(1020, 1023):
    ALL_CHECKS.append(i)
    WARNING_CHECKS.append(i)
for i in range(1030, 1038):
    ALL_CHECKS.append(i)
    WARNING_CHECKS.append(i)
for i in range(1040, 1045):
    ALL_CHECKS.append(i)
    WARNING_CHECKS.append(i)
    
messages_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "messages.json")
with open(messages_path) as file:
    MESSAGES = json.load(file)

@dataclass
class ReactionData:
    reaction_id: str
    kinetics: str
    kinetics_sim: str
    reactant_list: List[str]
    product_list: List[str]
    species_in_kinetic_law: List[str]
    parameters_in_kinetic_law: List[str]
    ids_list: List[str]
    sorted_species: List[str]
    boundary_species: List[str]
    parameters_in_kinetic_law_only: List[str]
    compartment_in_kinetic_law: List[str]
    is_reversible: bool
    sbo_term: int
    codes: List[int]
    non_constant_params: List[str]


class AnalyzerData:
    def __init__(self, model_str: str, rate_law_classifications_path: str=None):
        """
        Initializes the AnalyzerData object.

        Args:
            model_str (str): Path to the model file, or the string representation of model.
            rate_law_classifications_path (str): Path to the rate law classification file.
            customized rate law classification.

        Examples:
            import Analyzer from ratesb_python.common.analyzer
            analyzer = Analyzer("path/to/biomodel.xml", "path/to/rate_laws.json")
            analyzer.check_all()
            results = analyzer.results
            print(str(results))
            str(results)
        """
        # check if parameters are strings
        if not isinstance(model_str, str):
            raise ValueError("Invalid model_str format, should be string.")
        if rate_law_classifications_path and not isinstance(rate_law_classifications_path, str):
            raise ValueError("Invalid rate_law_classifications_path format, should be string.")
        # check if the model_str is sbml
        if '<?xml' in model_str:
            if '<sbml' not in model_str:
                raise ValueError("Invalid SBML model.")
            else:
                xml = model_str
        else:
            # model_str is not sbml
            load_int = antimony.loadAntimonyString(model_str)
            if load_int > 0:
                xml = antimony.getSBMLString()
            elif model_str.endswith('.ant') or model_str.endswith('.txt') or model_str.endswith('.xml'):
                # model_str is path to model
                xml = ''
                if model_str.endswith('.ant') or model_str.endswith('.txt'):
                    ant = util.get_model_str(model_str, False)
                    load_int = antimony.loadAntimonyString(ant)
                    if load_int > 0:
                        xml = antimony.getSBMLString()
                    else:
                        raise ValueError("Invalid Antimony model.")
                else:
                    xml = util.get_model_str(model_str, True)
            else:
                raise ValueError("Invalid model_str format, should be SBML or Antimony string, or path to model file.")
        reader = libsbml.SBMLReader()
        document = reader.readSBMLFromString(xml)
        util.checkSBMLDocument(document)
        self.model = document.getModel()
        self.simple = SimpleSBML(self.model)
        self.custom_classifier = None
        self.default_classifications = {}
        self.custom_classifications = {}
        self.results = Results()
        self.errors = []
        default_classifier_path = os.path.join(current_dir, "default_classifier.json")
        self.default_classifier = _CustomClassifier(default_classifier_path)

        if rate_law_classifications_path:
            self.custom_classifier = _CustomClassifier(
                rate_law_classifications_path)
            if len(self.custom_classifier.warning_message) > 0:
                print(self.custom_classifier.warning_message)
        
        self.reactions = []
        for reaction in self.simple.reactions:
            reaction.kinetic_law.formula = reaction.kinetic_law.formula.replace(
                '^', '**')
            ids_list = list(dict.fromkeys(reaction.kinetic_law.symbols))

            libsbml_kinetics = reaction.kinetic_law.libsbml_kinetics
            sbo_term = -1
            if libsbml_kinetics:
                sbo_term = libsbml_kinetics.getSBOTerm()

            reaction_id = reaction.getId()
            sorted_species = self._get_sorted_species(reaction.reaction)
            species_list, parameter_list, local_parameter_list, compartment_list, kinetics, kinetics_sim = self._preprocess_reactions(
                reaction)
            reactant_list, product_list = self._extract_kinetics_details(
                reaction)
            species_in_kinetic_law, parameters_in_kinetic_law_only, compartment_in_kinetic_law, others_in_kinetic_law = self._identify_parameters_in_kinetics(
                ids_list, species_list, parameter_list, local_parameter_list, compartment_list)
            boundary_species = self._get_boundary_species(
                reactant_list, product_list)
            non_constant_params = self._get_non_constant_params(parameters_in_kinetic_law_only)
            
            is_reversible = reaction.reaction.getReversible()
            
            codes = []
            
            data = ReactionData(
                reaction_id=reaction_id,
                kinetics=kinetics,
                kinetics_sim=kinetics_sim,
                reactant_list=reactant_list,
                product_list=product_list,
                species_in_kinetic_law=species_in_kinetic_law,
                parameters_in_kinetic_law=parameters_in_kinetic_law_only + others_in_kinetic_law,
                ids_list=ids_list,
                sorted_species=sorted_species,
                boundary_species=boundary_species,
                parameters_in_kinetic_law_only=parameters_in_kinetic_law_only,
                compartment_in_kinetic_law=compartment_in_kinetic_law,
                is_reversible=is_reversible,
                sbo_term=sbo_term,
                codes=codes,
                non_constant_params=non_constant_params
            )
            
            self.reactions.append(data)

    def _get_sorted_species(self, reaction):
        sorted_species_reference = [reaction.getReactant(n) for n in range(
            reaction.getNumReactants())] + [reaction.getProduct(n) for n in range(reaction.getNumProducts())]
        sorted_species = []
        for species_reference in sorted_species_reference:
            sorted_species.append(species_reference.getSpecies())
        return sorted_species

    def _preprocess_reactions(self, reaction):
        # Extract and process necessary data from the reaction
        species_num = self.model.getNumSpecies()
        parameter_num = self.model.getNumParameters()
        compartment_num = self.model.getNumCompartments()

        species_list = [self.model.getSpecies(
            i).getId() for i in range(species_num)]
        parameter_list = [self.model.getParameter(
            i).getId() for i in range(parameter_num)]
        local_parameter_list= (
            [reaction.kinetic_law.libsbml_kinetics.getLocalParameter(i).getId() for i in range(reaction.kinetic_law.libsbml_kinetics.getNumLocalParameters())])
        compartment_list = [self.model.getCompartment(
            i).getId() for i in range(compartment_num)]

        kinetics = reaction.kinetic_law.expanded_formula

        try:
            kinetics_sim = str(sp.simplify(kinetics))
        except:
            kinetics_sim = kinetics

        return species_list, parameter_list, local_parameter_list, compartment_list, kinetics, kinetics_sim

    def _extract_kinetics_details(self, reaction):
        reactant_list = [r.getSpecies() for r in reaction.reactants]
        product_list = [p.getSpecies() for p in reaction.products]
        return reactant_list, product_list

    def _identify_parameters_in_kinetics(self, ids_list, species_list, parameter_list, local_parameter_list, compartment_list):
        species_in_kinetic_law = []
        parameters_in_kinetic_law_only = []
        compartment_in_kinetic_law = []
        others_in_kinetic_law = []

        for id in ids_list:
            if id in species_list:
                species_in_kinetic_law.append(id)
            elif id in parameter_list:
                parameters_in_kinetic_law_only.append(id)
            elif id in local_parameter_list:
                parameters_in_kinetic_law_only.append(id)
            elif id in compartment_list:
                compartment_in_kinetic_law.append(id)
                others_in_kinetic_law.append(id)
            else:
                others_in_kinetic_law.append(id)

        return species_in_kinetic_law, parameters_in_kinetic_law_only, compartment_in_kinetic_law, others_in_kinetic_law

    def _get_boundary_species(self, reactant_list, product_list):
        boundary_species = [reactant for reactant in reactant_list if self.model.getSpecies(
            reactant).getBoundaryCondition()]
        boundary_species += [product for product in product_list if self.model.getSpecies(
            product).getBoundaryCondition()]
        return boundary_species

    def _get_non_constant_params(self, parameters_in_kinetic_law_only):
        non_constant_params = []
        for param in parameters_in_kinetic_law_only:
            try:
                libsbml_param = self.model.getParameter(param)
                if libsbml_param and not libsbml_param.getConstant():
                    non_constant_params.append(param)
            except:
                pass
        return non_constant_params