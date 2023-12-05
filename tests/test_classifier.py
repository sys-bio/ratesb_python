import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import call
from unittest.mock import ANY
import os
import math
import random

import sympy as sp
import numpy as np
import pandas as pd
import libsbml
import antimony as sb
import json

import sys
 
# setting path
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
common_dir = os.path.join(parent_dir, 'ratesb_python', 'common')
sys.path.append(common_dir)

# from ratesb_python.common.custom_classifier import _CustomClassifier
from analyzer import Analyzer

DIR = os.path.dirname(os.path.realpath(__file__))
UPPER_DIR = os.path.dirname(DIR)
DEFAULT_CLASSIFIER_PATH = os.path.join(UPPER_DIR, "ratesb_python", "common", "default_classifier.json")

TEST_CLASSIFIER_MODELS = "test_classifier_models"
ZERO_PATH = os.path.join(DIR, TEST_CLASSIFIER_MODELS, "zero.ant")

# DEFAULT_CLASSIFIER = _CustomClassifier(DEFAULT_CLASSIFIER_PATH)

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

class TestClassifier(unittest.TestCase):
    def test_false(self):
        analyzer = Analyzer(os.path.join(DIR, TEST_CLASSIFIER_MODELS, "false.ant"))
        analyzer.check([])
        for key, val in analyzer.default_classifications.items():
            for k, v in val.items():
                self.assertFalse(v)

    def test_zero(self):
        analyzer = Analyzer(ZERO_PATH)
        analyzer.check([])
        for key, val in analyzer.default_classifications.items():
            self.assertTrue(val[ZERO])
            # assert all other values are false
            for k, v in val.items():
                if k != ZERO:
                    self.assertFalse(v)
    
    def test_undr(self):
        analyzer = Analyzer(os.path.join(DIR, TEST_CLASSIFIER_MODELS, "undr.ant"))
        analyzer.check([])
        for key, val in analyzer.default_classifications.items():
            self.assertTrue(val[UNDR1] or val[UNDR2] or val[UNDR3])
            for k, v in val.items():
                if k != UNDR1 and k != UNDR2 and k != UNDR3:
                    self.assertFalse(v)
    
    def test_undr_a(self):
        analyzer = Analyzer(os.path.join(DIR, TEST_CLASSIFIER_MODELS, "undr_a.ant"))
        analyzer.check([])
        for key, val in analyzer.default_classifications.items():
            self.assertTrue(val[UNDR_A1] or val[UNDR_A2] or val[UNDR_A3])
            for k, v in val.items():
                if k != UNDR_A1 and k != UNDR_A2 and k != UNDR_A3:
                    self.assertFalse(v)
    
    def test_bidr(self):
        analyzer = Analyzer(os.path.join(DIR, TEST_CLASSIFIER_MODELS, "bidr.ant"))
        analyzer.check([])
        for key, val in analyzer.default_classifications.items():
            self.assertTrue(val[BIDR11] or val[BIDR12] or val[BIDR21] or val[BIDR22])
            for k, v in val.items():
                if k != BIDR11 and k != BIDR12 and k != BIDR21 and k != BIDR22:
                    self.assertFalse(v)
    
    def test_bidr_a(self):
        analyzer = Analyzer(os.path.join(DIR, TEST_CLASSIFIER_MODELS, "bidr_a.ant"))
        analyzer.check([])
        for key, val in analyzer.default_classifications.items():
            self.assertTrue(val[BIDR_A11] or val[BIDR_A12] or val[BIDR_A21] or val[BIDR_A22])
            for k, v in val.items():
                if k != BIDR_A11 and k != BIDR_A12 and k != BIDR_A21 and k != BIDR_A22:
                    self.assertFalse(v)
    
    def test_mm(self):
        analyzer = Analyzer(os.path.join(DIR, TEST_CLASSIFIER_MODELS, "mm.ant"))
        analyzer.check([])
        for key, val in analyzer.default_classifications.items():
            self.assertTrue(val[MM])
            for k, v in val.items():
                if k != MM:
                    self.assertFalse(v)
    
    def test_mmcat(self):
        analyzer = Analyzer(os.path.join(DIR, TEST_CLASSIFIER_MODELS, "mmcat.ant"))
        analyzer.check([])
        for key, val in analyzer.default_classifications.items():
            self.assertTrue(val[MM_CAT])
            for k, v in val.items():
                if k != MM_CAT:
                    self.assertFalse(v)
    
    def test_amm(self):
        analyzer = Analyzer(os.path.join(DIR, TEST_CLASSIFIER_MODELS, "amm.ant"))
        analyzer.check([])
        for key, val in analyzer.default_classifications.items():
            self.assertTrue(val[AMM])
            for k, v in val.items():
                if k != AMM:
                    self.assertFalse(v)
    
    def test_imm(self):
        analyzer = Analyzer(os.path.join(DIR, TEST_CLASSIFIER_MODELS, "imm.ant"))
        analyzer.check([])
        for key, val in analyzer.default_classifications.items():
            self.assertTrue(val[IMM])
            for k, v in val.items():
                if k != IMM:
                    self.assertFalse(v)
    
    def test_rmm(self):
        analyzer = Analyzer(os.path.join(DIR, TEST_CLASSIFIER_MODELS, "rmm.ant"))
        analyzer.check([])
        for key, val in analyzer.default_classifications.items():
            self.assertTrue(val[RMM])
            for k, v in val.items():
                if k != RMM:
                    self.assertFalse(v)
    
    def test_rmmcat(self):
        analyzer = Analyzer(os.path.join(DIR, TEST_CLASSIFIER_MODELS, "rmmcat.ant"))
        analyzer.check([])
        for key, val in analyzer.default_classifications.items():
            self.assertTrue(val[RMM_CAT])
            for k, v in val.items():
                if k != RMM_CAT:
                    self.assertFalse(v)
    
    def test_hill(self):
        analyzer = Analyzer(os.path.join(DIR, TEST_CLASSIFIER_MODELS, "hill.ant"))
        analyzer.check([])
        for key, val in analyzer.default_classifications.items():
            self.assertTrue(val[HILL])
            for k, v in val.items():
                if k != HILL:
                    self.assertFalse(v)

if __name__ == "__main__":
    unittest.main()