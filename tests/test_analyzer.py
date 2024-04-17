import unittest
import sys
import os
# setting path
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
common_dir = os.path.join(parent_dir, 'ratesb_python', 'common')
sys.path.append(common_dir)

from analyzer import Analyzer


DIR = os.path.dirname(os.path.abspath(__file__))
TEST_MODELS = "test_models"

INVALID_PATH = os.path.join(DIR, TEST_MODELS, "invalid.ant")
REVERSIBLE_MM_PATH = os.path.join(DIR, TEST_MODELS, "reversible_MM.json")

PATH_1 = os.path.join(DIR, TEST_MODELS, "1.ant")
TRUE_PATH_1 = os.path.join(DIR, TEST_MODELS, "true_0001.ant")
FALSE_PATH_1 = os.path.join(DIR, TEST_MODELS, "false_0001.ant")
TRUE_PATH_2 = os.path.join(DIR, TEST_MODELS, "true_0002.ant")
FALSE_PATH_2 = os.path.join(DIR, TEST_MODELS, "false_0002.ant")

TRUE_PATH_1001 = os.path.join(DIR, TEST_MODELS, "true_1001.ant")
FALSE_PATH_1001 = os.path.join(DIR, TEST_MODELS, "false_1001.ant")
TRUE_PATH_1002 = os.path.join(DIR, TEST_MODELS, "true_1002.ant")
FALSE_PATH_1002 = os.path.join(DIR, TEST_MODELS, "false_1002.ant")
TRUE_PATH_1003 = os.path.join(DIR, TEST_MODELS, "true_1003.ant")
FALSE_PATH_1003 = os.path.join(DIR, TEST_MODELS, "false_1003.ant")
TRUE_PATH_1004 = os.path.join(DIR, TEST_MODELS, "true_1004.ant")
FALSE_PATH_1004 = os.path.join(DIR, TEST_MODELS, "false_1004.ant")
TRUE_PATH_1005 = os.path.join(DIR, TEST_MODELS, "true_1005.ant")
FALSE_PATH_1005 = os.path.join(DIR, TEST_MODELS, "false_1005.ant")
TRUE_PATH_1006 = os.path.join(DIR, TEST_MODELS, "true_1006.ant")
FALSE_PATH_1006 = os.path.join(DIR, TEST_MODELS, "false_1006.ant")

TRUE_PATH_1010 = os.path.join(DIR, TEST_MODELS, "true_1010.ant")
FALSE_PATH_1010 = os.path.join(DIR, TEST_MODELS, "false_1010.ant")

TRUE_PATH_1020 = os.path.join(DIR, TEST_MODELS, "true_1020.ant")
FALSE_PATH_1020 = os.path.join(DIR, TEST_MODELS, "false_1020.ant")
TRUE_PATH_1021 = os.path.join(DIR, TEST_MODELS, "true_1021.ant")
FALSE_PATH_1021 = os.path.join(DIR, TEST_MODELS, "false_1021.ant")
TRUE_PATH_1022 = os.path.join(DIR, TEST_MODELS, "true_1022.ant")
FALSE_PATH_1022 = os.path.join(DIR, TEST_MODELS, "false_1022.ant")

TRUE_PATH_1030 = os.path.join(DIR, TEST_MODELS, "true_1030.ant")
FALSE_PATH_1030 = os.path.join(DIR, TEST_MODELS, "false_1030.ant")
TRUE_PATH_1031 = os.path.join(DIR, TEST_MODELS, "true_1031.ant")
FALSE_PATH_1031 = os.path.join(DIR, TEST_MODELS, "false_1031.ant")
TRUE_PATH_1032 = os.path.join(DIR, TEST_MODELS, "true_1032.ant")
FALSE_PATH_1032 = os.path.join(DIR, TEST_MODELS, "false_1032.ant")
TRUE_PATH_1033 = os.path.join(DIR, TEST_MODELS, "true_1033.ant")
FALSE_PATH_1033 = os.path.join(DIR, TEST_MODELS, "false_1033.ant")
TRUE_PATH_1034 = os.path.join(DIR, TEST_MODELS, "true_1034.ant")
FALSE_PATH_1034 = os.path.join(DIR, TEST_MODELS, "false_1034.ant")
TRUE_PATH_1035 = os.path.join(DIR, TEST_MODELS, "true_1035.ant")
FALSE_PATH_1035 = os.path.join(DIR, TEST_MODELS, "false_1035.ant")
TRUE_PATH_1036 = os.path.join(DIR, TEST_MODELS, "true_1036.ant")
FALSE_PATH_1036 = os.path.join(DIR, TEST_MODELS, "false_1036.ant")
TRUE_PATH_1037 = os.path.join(DIR, TEST_MODELS, "true_1037.ant")
FALSE_PATH_1037 = os.path.join(DIR, TEST_MODELS, "false_1037.ant")

TRUE_PATH_1040 = os.path.join(DIR, TEST_MODELS, "true_1040.xml")
FALSE_PATH_1040 = os.path.join(DIR, TEST_MODELS, "false_1040.xml")
TRUE_PATH_1041 = os.path.join(DIR, TEST_MODELS, "true_1041.xml")
FALSE_PATH_1041 = os.path.join(DIR, TEST_MODELS, "false_1041.xml")
TRUE_PATH_1042 = os.path.join(DIR, TEST_MODELS, "true_1042.xml")
FALSE_PATH_1042 = os.path.join(DIR, TEST_MODELS, "false_1042.xml")
TRUE_PATH_1043 = os.path.join(DIR, TEST_MODELS, "true_1043.xml")
FALSE_PATH_1043 = os.path.join(DIR, TEST_MODELS, "false_1043.xml")
TRUE_PATH_1044 = os.path.join(DIR, TEST_MODELS, "true_1044.xml")
FALSE_PATH_1044 = os.path.join(DIR, TEST_MODELS, "false_1044.xml")

class TestAnalyzer(unittest.TestCase):

    def setUp(self):
        # self.rate_analyzer = Analyzer("tests/test_models/1.ant", "tests/test_models/rate_laws.json")
        # self.mm_analyzer = Analyzer("tests/test_models/reversible_MM.ant", "tests/test_models/reversible_MM.json")
        self.analyzer = Analyzer("tests/test_models/1.ant")

    # def test_get_rate_laws(self):
    #     # Add test logic here. For example:
    #     # self.assertEqual(self.rate_analyzer.get_rate_laws(), expected_result)
    #     pass
    
    def test_init(self):
        # test if model_str is not str
        try:
            Analyzer(1)
        except ValueError as e:
            self.assertEqual(str(e), "Invalid model_str format, should be string.")
        else:
            self.fail("Expected ValueError")
        # test if rate_law_classifications_path is not str
        try:
            Analyzer(TRUE_PATH_1, 1)
        except ValueError as e:
            self.assertEqual(str(e), "Invalid rate_law_classifications_path format, should be string.")
        else:
            self.fail("Expected ValueError")
        # test xml file without '<sbml'
        try:
            Analyzer("<?xml")
        except ValueError as e:
            self.assertEqual(str(e), "Invalid SBML model.")
        else:
            self.fail("Expected ValueError")
        # test invalid antimony model
        try:
            Analyzer("a->b")
        except ValueError as e:
            self.assertEqual(str(e), "Invalid model_str format, should be SBML or Antimony string, or path to model file.")
        else:
            self.fail("Expected ValueError")
        # test valid antimony model
        try:
            Analyzer("S1 -> S2; k1*S1")
        except ValueError:
            self.fail("Unexpected ValueError")
        # test invalid antimony model with file input
        try:
            Analyzer(INVALID_PATH)
        except ValueError as e:
            self.assertEqual(str(e), "Invalid Antimony model.")
        else:
            self.fail("Expected ValueError")
        # test invalid file format
        try:
            Analyzer("invalid_path.json")
        except ValueError as e:
            self.assertEqual(str(e), "Invalid model_str format, should be SBML or Antimony string, or path to model file.")
        else:
            self.fail("Expected ValueError")
        # test custom classifier
        try:
            Analyzer(TRUE_PATH_1, REVERSIBLE_MM_PATH)
        except ValueError:
            self.fail("Unexpected ValueError")
    
    def test_check_0001(self):
        true_case_analyzer = Analyzer(TRUE_PATH_2)
        false_case_analyzer = Analyzer(FALSE_PATH_2)
        true_case_analyzer.checks([1])
        false_case_analyzer.checks([1])
        # self.assertEqual(self.rate_analyzer.classification_cp, [])
        self.assertEqual(str(true_case_analyzer.results), 'No errors or warnings found.')
        self.assertEqual(str(false_case_analyzer.results), 'No errors or warnings found.')
    
    def test_check_0002(self):
        true_case_analyzer = Analyzer(TRUE_PATH_2)
        false_case_analyzer = Analyzer(FALSE_PATH_2)
        true_case_analyzer.checks([2])
        false_case_analyzer.checks([2])
        self.assertEqual(str(true_case_analyzer.results), 'No errors or warnings found.')
        self.assertEqual(str(false_case_analyzer.results), '_J0:\n  Error 0002: Expecting reactants in rate law: a\n')
    
    def test_check_1001(self):
        true_case_analyzer = Analyzer(TRUE_PATH_1001)
        false_case_analyzer = Analyzer(FALSE_PATH_1001)
        true_case_analyzer.checks([1001])
        false_case_analyzer.checks([1001])
        self.assertEqual(str(true_case_analyzer.results), 'No errors or warnings found.')
        self.assertEqual(str(false_case_analyzer.results), '_J0:\n  Warning 1001: Rate law contains only number.\n')

    def test_check_1002(self):
        true_case_analyzer = Analyzer(TRUE_PATH_1002)
        false_case_analyzer = Analyzer(FALSE_PATH_1002)
        true_case_analyzer.checks([1002])
        false_case_analyzer.checks([1002])
        self.assertEqual(str(true_case_analyzer.results), 'No errors or warnings found.')
        self.assertEqual(str(false_case_analyzer.results), '_J0:\n  Warning 1002: Unrecognized rate law from the standard list.\n')
        false_case_2_analyzer = Analyzer(FALSE_PATH_1002, REVERSIBLE_MM_PATH)
        false_case_2_analyzer.checks([1002])
        self.assertEqual(str(false_case_2_analyzer.results), "_J0:\n  Warning 1002: Unrecognized rate law from the standard list and the custom list.\n")
    
    def test_check_1003(self):
        true_case_analyzer = Analyzer(TRUE_PATH_1003)
        false_case_analyzer = Analyzer(FALSE_PATH_1003)
        true_case_analyzer.checks([1003])
        false_case_analyzer.checks([1003])
        self.assertEqual(str(true_case_analyzer.results), 'No errors or warnings found.')
        self.assertEqual(str(false_case_analyzer.results), '_J0:\n  Warning 1003: Flux is not increasing as reactant increases.\n_J1:\n  Warning 1003: Flux is not increasing as reactant increases.\n_J2:\n  Warning 1003: Flux is not increasing as reactant increases.\n')
    
    def test_check_1004(self):
        true_case_analyzer = Analyzer(TRUE_PATH_1004)
        false_case_analyzer = Analyzer(FALSE_PATH_1004)
        true_case_analyzer.checks([1004])
        false_case_analyzer.checks([1004])
        self.assertEqual(str(true_case_analyzer.results), 'No errors or warnings found.')
        self.assertEqual(str(false_case_analyzer.results), '_J0:\n  Warning 1004: Flux is not decreasing as product increases.\n')
    
    def test_check_1005(self):
        true_case_analyzer = Analyzer(TRUE_PATH_1005)
        false_case_analyzer = Analyzer(FALSE_PATH_1005)
        true_case_analyzer.checks([1005])
        false_case_analyzer.checks([1005])
        self.assertEqual(str(true_case_analyzer.results), 'No errors or warnings found.')
        self.assertEqual(str(false_case_analyzer.results), '_J0:\n  Warning 1005: Expecting boundary species reactant in rate law: a\n')
    
    def test_check_1006(self):
        true_case_analyzer = Analyzer(TRUE_PATH_1006)
        false_case_analyzer = Analyzer(FALSE_PATH_1006)
        true_case_analyzer.checks([1006])
        false_case_analyzer.checks([1006])
        self.assertEqual(str(true_case_analyzer.results), 'No errors or warnings found.')
        self.assertEqual(str(false_case_analyzer.results), '_J0:\n  Warning 1006: Expecting these parameters to be constants: k1\n')
    
    def test_check_1010(self):
        true_case_analyzer = Analyzer(TRUE_PATH_1010)
        false_case_analyzer = Analyzer(FALSE_PATH_1010)
        true_case_analyzer.checks([1010])
        false_case_analyzer.checks([1010])
        self.assertEqual(str(true_case_analyzer.results), 'No errors or warnings found.')
        self.assertEqual(str(false_case_analyzer.results), '_J0:\n  Warning 1010: Irreversible reaction kinetic law contains products: b\n')
    
    def test_check_1020(self):
        true_case_analyzer = Analyzer(TRUE_PATH_1020)
        false_case_analyzer = Analyzer(FALSE_PATH_1020)
        true_case_analyzer.checks([1020])
        false_case_analyzer.checks([1020])
        self.assertEqual(str(true_case_analyzer.results), 'No errors or warnings found.')
        self.assertEqual(str(false_case_analyzer.results), "_J0:\n  Warning 1020: We recommend that these parameters start with 'k': v1\n_J1:\n  Warning 1020: We recommend that these parameters start with 'k': K1\n_J2:\n  Warning 1020: We recommend that these parameters start with 'k': K1\n_J3:\n  Warning 1020: We recommend that these parameters start with 'k': v1\n")
    
    def test_check_1021(self):
        true_case_analyzer = Analyzer(TRUE_PATH_1021)
        false_case_analyzer = Analyzer(FALSE_PATH_1021)
        true_case_analyzer.checks([1021])
        false_case_analyzer.checks([1021])
        self.assertEqual(str(true_case_analyzer.results), 'No errors or warnings found.')
        self.assertEqual(str(false_case_analyzer.results), "_J0:\n  Warning 1021: We recommend that these parameters start with 'K': km\n_J1:\n  Warning 1021: We recommend that these parameters start with 'K': km\n_J2:\n  Warning 1021: We recommend that these parameters start with 'K': k3\n")
    
    def test_check_1022(self):
        true_case_analyzer = Analyzer(TRUE_PATH_1022)
        false_case_analyzer = Analyzer(FALSE_PATH_1022)
        true_case_analyzer.checks([1022])
        false_case_analyzer.checks([1022])
        self.assertEqual(str(true_case_analyzer.results), 'No errors or warnings found.')
        self.assertEqual(str(false_case_analyzer.results), "_J0:\n  Warning 1022: We recommend that these parameters start with 'V': vm\n")
    
    def test_check_1030(self):
        true_case_analyzer = Analyzer(TRUE_PATH_1030)
        false_case_analyzer = Analyzer(FALSE_PATH_1030)
        true_case_analyzer.checks([1030])
        false_case_analyzer.checks([1030])
        self.assertEqual(str(true_case_analyzer.results), 'No errors or warnings found.')
        self.assertEqual(str(false_case_analyzer.results), "_J0:\n  Warning 1030: Elements of the same type are not ordered alphabetically\n_J1:\n  Warning 1030: Elements of the same type are not ordered alphabetically\n")
    
    def test_check_1031(self):
        true_case_analyzer = Analyzer(TRUE_PATH_1031)
        false_case_analyzer = Analyzer(FALSE_PATH_1031)
        true_case_analyzer.checks([1031])
        false_case_analyzer.checks([1031])
        self.assertEqual(str(true_case_analyzer.results), 'No errors or warnings found.')
        self.assertEqual(str(false_case_analyzer.results), "_J0:\n  Warning 1031: Formatting convention not followed (compartment before parameters before species)\n_J1:\n  Warning 1031: Formatting convention not followed (compartment before parameters before species)\n")

    # TODO: implement convention checks for fractional rate laws
    def test_check_1032(self):
        true_case_analyzer = Analyzer(TRUE_PATH_1032)
        false_case_analyzer = Analyzer(FALSE_PATH_1032)
        true_case_analyzer.checks([1032])
        false_case_analyzer.checks([1032])
        self.assertEqual(str(true_case_analyzer.results), 'No errors or warnings found.')
        self.assertEqual(str(false_case_analyzer.results), "_J0:\n  Warning 1032: Denominator not in alphabetical order\n")

    def test_check_1033(self):
        true_case_analyzer = Analyzer(TRUE_PATH_1033)
        false_case_analyzer = Analyzer(FALSE_PATH_1033)
        true_case_analyzer.checks([1033])
        false_case_analyzer.checks([1033])
        self.assertEqual(str(true_case_analyzer.results), 'No errors or warnings found.')
        self.assertEqual(str(false_case_analyzer.results), "_J0:\n  Warning 1033: Numerator and denominator not in alphabetical order\n")

    def test_check_1034(self):
        true_case_analyzer = Analyzer(TRUE_PATH_1034)
        false_case_analyzer = Analyzer(FALSE_PATH_1034)
        true_case_analyzer.checks([1034])
        false_case_analyzer.checks([1034])
        self.assertEqual(str(true_case_analyzer.results), 'No errors or warnings found.')
        self.assertEqual(str(false_case_analyzer.results), "_J0:\n  Warning 1034: Numerator convention not followed and denominator not in alphabetical order\n")

    # def test_check_1035(self):
    #     true_case_analyzer = Analyzer(TRUE_PATH_1035)
    #     false_case_analyzer = Analyzer(FALSE_PATH_1035)
    #     true_case_analyzer.checks([1035])
    #     false_case_analyzer.checks([1035])
    #     self.assertEqual(str(true_case_analyzer.results), 'No errors or warnings found.')
    #     self.assertEqual(str(false_case_analyzer.results), "_J0:\n  Warning 1035: Denominator convention not followed\n")

    # def test_check_1036(self):
    #     true_case_analyzer = Analyzer(TRUE_PATH_1036)
    #     false_case_analyzer = Analyzer(FALSE_PATH_1036)
    #     true_case_analyzer.checks([1036])
    #     false_case_analyzer.checks([1036])
    #     # self.assertEqual(str(true_case_analyzer.results), 'No errors or warnings found.')
    #     self.assertEqual(str(false_case_analyzer.results), "_J0:\n  Warning 1036: Numerator not in alphabetical order and denominator convention not followed\n")

    # def test_check_1037(self):
    #     true_case_analyzer = Analyzer(TRUE_PATH_1037)
    #     false_case_analyzer = Analyzer(FALSE_PATH_1037)
    #     true_case_analyzer.checks([1037])
    #     false_case_analyzer.checks([1037])
    #     self.assertEqual(str(true_case_analyzer.results), 'No errors or warnings found.')
    #     self.assertEqual(str(false_case_analyzer.results), "_J0:\n  Warning 1037: Numerator and denominator convention not followed\n")

    def test_check_1040(self):
        true_case_analyzer = Analyzer(TRUE_PATH_1040)
        false_case_analyzer = Analyzer(FALSE_PATH_1040)
        true_case_analyzer.checks([1040])
        false_case_analyzer.checks([1040])
        self.assertEqual(str(true_case_analyzer.results), 'No errors or warnings found.')
        self.assertEqual(str(false_case_analyzer.results), "_J0:\n  Warning 1040: Uni-directional mass action annotation not following recommended SBO terms, we recommend annotations to be subclasses of: SBO_0000430, SBO_0000041\n")

    def test_check_1041(self):
        true_case_analyzer = Analyzer(TRUE_PATH_1041)
        false_case_analyzer = Analyzer(FALSE_PATH_1041)
        true_case_analyzer.checks([1041])
        false_case_analyzer.checks([1041])
        self.assertEqual(str(true_case_analyzer.results), 'No errors or warnings found.')
        self.assertEqual(str(false_case_analyzer.results), "_J0:\n  Warning 1041: Uni-Directional Mass Action with an Activator annotation not following recommended SBO terms, we recommend annotations to be subclasses of: SBO_0000041\n")

    def test_check_1042(self):
        true_case_analyzer = Analyzer(TRUE_PATH_1042)
        false_case_analyzer = Analyzer(FALSE_PATH_1042)
        true_case_analyzer.checks([1042])
        false_case_analyzer.checks([1042])
        self.assertEqual(str(true_case_analyzer.results), 'No errors or warnings found.')
        self.assertEqual(str(false_case_analyzer.results), "_J0:\n  Warning 1042: Bi-directional mass action (with an Activator) annotation not following recommended SBO terms, we recommend annotations to be subclasses of: SBO_0000042\n")

    def test_check_1043(self):
        true_case_analyzer = Analyzer(TRUE_PATH_1043)
        false_case_analyzer = Analyzer(FALSE_PATH_1043)
        true_case_analyzer.checks([1043])
        false_case_analyzer.checks([1043])
        self.assertEqual(str(true_case_analyzer.results), 'No errors or warnings found.')
        self.assertEqual(str(false_case_analyzer.results), "_J0:\n  Warning 1043: Michaelis-Menten kinetics without an explicit enzyme annotation not following recommended SBO terms, we recommend annotations to be subclasses of: SBO_0000028\n")

    def test_check_1044(self):
        true_case_analyzer = Analyzer(TRUE_PATH_1044)
        false_case_analyzer = Analyzer(FALSE_PATH_1044)
        true_case_analyzer.checks([1044])
        false_case_analyzer.checks([1044])
        self.assertEqual(str(true_case_analyzer.results), 'No errors or warnings found.')
        self.assertEqual(str(false_case_analyzer.results), "_J0:\n  Warning 1044: Michaelis-Menten kinetics with an explicit enzyme annotation not following recommended SBO terms, we recommend annotations to be subclasses of: SBO_0000028, SBO_0000430\n")
    
    def test_check_except(self):
        except_analyzer = Analyzer(PATH_1)
        analyzer = Analyzer(PATH_1)
        except_analyzer.check_except([1,2])
        analyzer.checks([1001, 1002, 1003, 1004, 1005, 1006, 1010, 1020, 1021, 1022, 1030, 1031, 1032, 1033, 1034, 1035, 1036, 1037, 1040, 1041, 1042, 1043, 1044])
        self.assertEqual(str(except_analyzer.results), str(analyzer.results))
    
    def test_check_all(self):
        all_analyzer = Analyzer(PATH_1)
        analyzer = Analyzer(PATH_1)
        all_analyzer.check_all()
        analyzer.check_except([])
        self.assertEqual(str(all_analyzer.results), str(analyzer.results))
        

if __name__ == "__main__":
    unittest.main()
