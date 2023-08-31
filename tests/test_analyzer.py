import unittest
from ratesb_python.common.analyzer import Analyzer
from SBMLKinetics.common.simple_sbml import SimpleSBML
from libsbml import SBMLReader

class TestAnalyzer(unittest.TestCase):

    # def setUp(self):
    #     # self.rate_analyzer = Analyzer("tests/test_models/1.ant", "tests/test_models/rate_laws.json")
    #     # self.mm_analyzer = Analyzer("tests/test_models/reversible_MM.ant", "tests/test_models/reversible_MM.json")
    #     self.analyzer = Analyzer("tests/test_models/1.ant")

    # def test_get_rate_laws(self):
    #     # Add test logic here. For example:
    #     # self.assertEqual(self.rate_analyzer.get_rate_laws(), expected_result)
    #     pass
    
    # def test_check_0001(self):
    #     pass
    #     true_case_analyzer = Analyzer("tests/test_models/true_0001.ant")
    #     false_case_analyzer = Analyzer("tests/test_models/false_0001.ant")
    #     true_case_analyzer.check(1)
    #     false_case_analyzer.check(1)
    #     # self.assertEqual(self.rate_analyzer.classification_cp, [])
    #     self.assertEqual(str(true_case_analyzer.results), '')
    #     self.assertEqual(str(false_case_analyzer.results), '')
    
    def test_check_0002(self):
        true_case_analyzer = Analyzer("tests/test_models/true_0002.ant")
        false_case_analyzer = Analyzer("tests/test_models/false_0002.ant")
        true_case_analyzer.check(2)
        false_case_analyzer.check(2)
        self.assertEqual(str(true_case_analyzer.results), '')
        self.assertEqual(str(false_case_analyzer.results), '_J0:\n  Error 0002: Expecting reactants in rate law: a\n')
    
    def test_check_1001(self):
        true_case_analyzer = Analyzer("tests/test_models/true_1001.ant")
        false_case_analyzer = Analyzer("tests/test_models/false_1001.ant")
        true_case_analyzer.check(1001)
        false_case_analyzer.check(1001)
        self.assertEqual(str(true_case_analyzer.results), '')
        self.assertEqual(str(false_case_analyzer.results), '_J0:\n  Warning 1001: Rate law contains only number.\n')

    def test_check_1002(self):
        true_case_analyzer = Analyzer("tests/test_models/true_1002.ant")
        false_case_analyzer = Analyzer("tests/test_models/false_1002.ant")
        true_case_analyzer.check(1002)
        false_case_analyzer.check(1002)
        self.assertEqual(str(true_case_analyzer.results), '')
        self.assertEqual(str(false_case_analyzer.results), '_J0:\n  Warning 1002: Unrecognized rate law from the standard list.\n')
    
    def test_check_1003(self):
        true_case_analyzer = Analyzer("tests/test_models/true_1003.ant")
        false_case_analyzer = Analyzer("tests/test_models/false_1003.ant")
        true_case_analyzer.check(1003)
        false_case_analyzer.check(1003)
        self.assertEqual(str(true_case_analyzer.results), '')
        self.assertEqual(str(false_case_analyzer.results), '_J0:\n  Warning 1003: Flux is not increasing as reactant increases.\n_J1:\n  Warning 1003: Flux is not increasing as reactant increases.\n_J2:\n  Warning 1003: Flux is not increasing as reactant increases.\n')
    
    def test_check_1004(self):
        true_case_analyzer = Analyzer("tests/test_models/true_1004.ant")
        false_case_analyzer = Analyzer("tests/test_models/false_1004.ant")
        true_case_analyzer.check(1004)
        false_case_analyzer.check(1004)
        self.assertEqual(str(true_case_analyzer.results), '')
        self.assertEqual(str(false_case_analyzer.results), '')
    
    def test_check_1005(self):
        true_case_analyzer = Analyzer("tests/test_models/true_1005.ant")
        false_case_analyzer = Analyzer("tests/test_models/false_1005.ant")
        true_case_analyzer.check(1005)
        false_case_analyzer.check(1005)
        self.assertEqual(str(true_case_analyzer.results), '')
        self.assertEqual(str(false_case_analyzer.results), '_J0:\n  Warning 1005: Expecting boundary species reactant in rate law: a\n')
    
    def test_check_1006(self):
        true_case_analyzer = Analyzer("tests/test_models/true_1006.ant")
        false_case_analyzer = Analyzer("tests/test_models/false_1006.ant")
        true_case_analyzer.check(1006)
        false_case_analyzer.check(1006)
        self.assertEqual(str(true_case_analyzer.results), '')
        self.assertEqual(str(false_case_analyzer.results), '_J0:\n  Warning 1006: Expecting boundary species reactant in rate law: k1\n')
    
    def test_check_1010(self):
        true_case_analyzer = Analyzer("tests/test_models/true_1010.ant")
        false_case_analyzer = Analyzer("tests/test_models/false_1010.ant")
        true_case_analyzer.check(1010)
        false_case_analyzer.check(1010)
        self.assertEqual(str(true_case_analyzer.results), '')
        self.assertEqual(str(false_case_analyzer.results), '_J0:\n  Warning 1010: Irreversible reaction kinetic law contains products: b\n')
    
    def test_check_1020(self):
        true_case_analyzer = Analyzer("tests/test_models/true_1020.ant")
        false_case_analyzer = Analyzer("tests/test_models/false_1020.ant")
        true_case_analyzer.check(1020)
        false_case_analyzer.check(1020)
        self.assertEqual(str(true_case_analyzer.results), '')
        self.assertEqual(str(false_case_analyzer.results), "_J0:\n  Warning 1020: We recommend that these parameters start with 'k': v1\n_J1:\n  Warning 1020: We recommend that these parameters start with 'k': K1\n_J2:\n  Warning 1020: We recommend that these parameters start with 'k': K1\n_J3:\n  Warning 1020: We recommend that these parameters start with 'k': v1\n")
    
    def test_check_1021(self):
        true_case_analyzer = Analyzer("tests/test_models/true_1021.ant")
        false_case_analyzer = Analyzer("tests/test_models/false_1021.ant")
        true_case_analyzer.check(1021)
        false_case_analyzer.check(1021)
        self.assertEqual(str(true_case_analyzer.results), '')
        self.assertEqual(str(false_case_analyzer.results), "_J0:\n  Warning 1021: We recommend that these parameters start with 'K': km\n_J1:\n  Warning 1021: We recommend that these parameters start with 'K': km\n_J2:\n  Warning 1021: We recommend that these parameters start with 'K': k3\n")
    
    def test_check_1022(self):
        true_case_analyzer = Analyzer("tests/test_models/true_1022.ant")
        false_case_analyzer = Analyzer("tests/test_models/false_1022.ant")
        true_case_analyzer.check(1022)
        false_case_analyzer.check(1022)
        self.assertEqual(str(true_case_analyzer.results), '')
        self.assertEqual(str(false_case_analyzer.results), "_J0:\n  Warning 1022: We recommend that these parameters start with 'V': vm\n")
    
    def test_check_1030(self):
        true_case_analyzer = Analyzer("tests/test_models/true_1030.ant")
        false_case_analyzer = Analyzer("tests/test_models/false_1030.ant")
        true_case_analyzer.check(1030)
        false_case_analyzer.check(1030)
        self.assertEqual(str(true_case_analyzer.results), '')
        self.assertEqual(str(false_case_analyzer.results), "_J0:\n  Warning 1030: Elements of the same type are not ordered properly\n_J1:\n  Warning 1030: Elements of the same type are not ordered properly\n")
    
    def test_check_1031(self):
        true_case_analyzer = Analyzer("tests/test_models/true_1031.ant")
        false_case_analyzer = Analyzer("tests/test_models/false_1031.ant")
        true_case_analyzer.check(1031)
        false_case_analyzer.check(1031)
        self.assertEqual(str(true_case_analyzer.results), '')
        self.assertEqual(str(false_case_analyzer.results), "_J0:\n  Warning 1031: Formatting convention not followed (compartment before parameters before species)\n_J1:\n  Warning 1031: Formatting convention not followed (compartment before parameters before species)\n")

    def test_check_1032(self):
        true_case_analyzer = Analyzer("tests/test_models/true_1032.ant")
        false_case_analyzer = Analyzer("tests/test_models/false_1032.ant")
        true_case_analyzer.check(1032)
        false_case_analyzer.check(1032)
        self.assertEqual(str(true_case_analyzer.results), '')
        self.assertEqual(str(false_case_analyzer.results), "_J0:\n  Warning 1032: Denominator not in alphabetical order\n")

    def test_check_1033(self):
        true_case_analyzer = Analyzer("tests/test_models/true_1033.ant")
        false_case_analyzer = Analyzer("tests/test_models/false_1033.ant")
        true_case_analyzer.check(1033)
        false_case_analyzer.check(1033)
        self.assertEqual(str(true_case_analyzer.results), '')
        self.assertEqual(str(false_case_analyzer.results), "_J0:\n  Warning 1033: Numerator and denominator not in alphabetical order\n")

    def test_check_1034(self):
        true_case_analyzer = Analyzer("tests/test_models/true_1034.ant")
        false_case_analyzer = Analyzer("tests/test_models/false_1034.ant")
        true_case_analyzer.check(1034)
        false_case_analyzer.check(1034)
        self.assertEqual(str(true_case_analyzer.results), '')
        self.assertEqual(str(false_case_analyzer.results), "_J0:\n  Warning 1034: Numerator convention not followed and denominator not in alphabetical order\n")

    def test_check_1035(self):
        true_case_analyzer = Analyzer("tests/test_models/true_1035.ant")
        false_case_analyzer = Analyzer("tests/test_models/false_1035.ant")
        true_case_analyzer.check(1035)
        false_case_analyzer.check(1035)
        self.assertEqual(str(true_case_analyzer.results), '')
        self.assertEqual(str(false_case_analyzer.results), "_J0:\n  Warning 1035: Denominator convention not followed\n")

    def test_check_1036(self):
        true_case_analyzer = Analyzer("tests/test_models/true_1036.ant")
        false_case_analyzer = Analyzer("tests/test_models/false_1036.ant")
        true_case_analyzer.check(1036)
        false_case_analyzer.check(1036)
        # self.assertEqual(str(true_case_analyzer.results), '')
        self.assertEqual(str(false_case_analyzer.results), "_J0:\n  Warning 1036: Numerator not in alphabetical order and denominator convention not followed\n")

    def test_check_1037(self):
        true_case_analyzer = Analyzer("tests/test_models/true_1037.ant")
        false_case_analyzer = Analyzer("tests/test_models/false_1037.ant")
        true_case_analyzer.check(1037)
        false_case_analyzer.check(1037)
        self.assertEqual(str(true_case_analyzer.results), '')
        self.assertEqual(str(false_case_analyzer.results), "_J0:\n  Warning 1037: Numerator and denominator convention not followed\n")

    def test_check_1040(self):
        true_case_analyzer = Analyzer("tests/test_models/true_1040.xml")
        false_case_analyzer = Analyzer("tests/test_models/false_1040.xml")
        true_case_analyzer.check(1040)
        false_case_analyzer.check(1040)
        self.assertEqual(str(true_case_analyzer.results), '')
        self.assertEqual(str(false_case_analyzer.results), "_J0:\n  Warning 1040: Uni-directional mass action annotation not following recommended SBO terms, we recommend annotations to be subclasses of: SBO_0000430, SBO_0000041\n")

    def test_check_1041(self):
        true_case_analyzer = Analyzer("tests/test_models/true_1041.xml")
        false_case_analyzer = Analyzer("tests/test_models/false_1041.xml")
        true_case_analyzer.check(1041)
        false_case_analyzer.check(1041)
        self.assertEqual(str(true_case_analyzer.results), '')
        self.assertEqual(str(false_case_analyzer.results), "_J0:\n  Warning 1041: Uni-term with the moderator annotation not following recommended SBO terms, we recommend annotations to be subclasses of: SBO_0000041\n")

    def test_check_1042(self):
        true_case_analyzer = Analyzer("tests/test_models/true_1042.xml")
        false_case_analyzer = Analyzer("tests/test_models/false_1042.xml")
        true_case_analyzer.check(1042)
        false_case_analyzer.check(1042)
        self.assertEqual(str(true_case_analyzer.results), '')
        self.assertEqual(str(false_case_analyzer.results), "_J0:\n  Warning 1042: Bi-directional mass action or Bi-terms with the moderator annotation not following recommended SBO terms, we recommend annotations to be subclasses of: SBO_0000042\n")

    def test_check_1043(self):
        true_case_analyzer = Analyzer("tests/test_models/true_1043.xml")
        false_case_analyzer = Analyzer("tests/test_models/false_1043.xml")
        true_case_analyzer.check(1043)
        false_case_analyzer.check(1043)
        self.assertEqual(str(true_case_analyzer.results), '')
        self.assertEqual(str(false_case_analyzer.results), "_J0:\n  Warning 1043: Michaelis-Menten kinetics without an explicit enzyme annotation not following recommended SBO terms, we recommend annotations to be subclasses of: SBO_0000028\n")

    def test_check_1044(self):
        true_case_analyzer = Analyzer("tests/test_models/true_1044.xml")
        false_case_analyzer = Analyzer("tests/test_models/false_1044.xml")
        true_case_analyzer.check(1044)
        false_case_analyzer.check(1044)
        self.assertEqual(str(true_case_analyzer.results), '')
        self.assertEqual(str(false_case_analyzer.results), "_J0:\n  Warning 1044: Michaelis-Menten kinetics with an explicit enzyme annotation not following recommended SBO terms, we recommend annotations to be subclasses of: SBO_0000028, SBO_0000430\n")
    
    def test_check_except(self):
        except_analyzer = Analyzer("tests/test_models/1.ant")
        analyzer = Analyzer("tests/test_models/1.ant")
        except_analyzer.check_except([1,2])
        analyzer.checks([1001, 1002, 1003, 1004, 1005, 1006, 1010, 1020, 1021, 1022, 1030, 1031, 1032, 1033, 1034, 1035, 1036, 1037, 1040, 1041, 1042, 1043, 1044])
        self.assertEqual(str(except_analyzer.results), str(analyzer.results))

if __name__ == "__main__":
    unittest.main()
