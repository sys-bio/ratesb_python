# ratesb_python: Rate Law Analysis for SBML and Antimony Models

`ratesb_python` is a Python package designed for analyzing rate laws in SBML (Systems Biology Markup Language) and Antimony models, which are commonly used in systems biology for representing biological networks. This package offers a user-friendly API to help ensure that your models are robust and accurate by providing detailed warnings and errors related to rate laws.

## ReadTheDocs

For detailed documentation, please visit [ReadTheDocs](https://longxf-ratesb-python.readthedocs-hosted.com/en/latest/).

## Installation

To install `ratesb_python`, execute the following command in your terminal:

```bash
pip install ratesb_python
```

## Usage

Below are examples demonstrating how to use the ratesb_python package with file input:

Simple example:
```python
from ratesb_python import check_model
print(check_model("S->P;k1*S"))
```

Expected output:
```bash
_J0:
  Warning 1004: Flux is not decreasing as product increases.
```

Explanation:
- `_J0` represents an internal identifier for the reaction flux. It is automatically assigned to the reaction for tracking purposes.
- The warning (1004) indicates that as the product (P) increases, the flux does not decrease as expected, suggesting a potential issue with the reversible reaction kinetics.

Complex example:
```python
from ratesb_python import Analyzer

analyzer = Analyzer("Reaction1: S1->P1; k1 * S1")

# Analyze the model for rate law correctness
analyzer.check_all()

# Display all errors and warnings
print(analyzer.results)

# Check selected errors and warnings
analyzer.checks([1, 2, 1001, 1002])
results = analyzer.results
print(results)

# Display only warnings
warnings = results.get_warnings()
for reaction, messages in warnings.items():
    print(reaction, messages)

# Retrieve messages for a specific reaction
messages = results.get_messages_by_reaction("Reaction1")
print(messages)

# Remove messages for a specific reaction
results.remove_messages_by_reaction("Reaction1")

# Get number of errors and warnings
print("Num Errors: ", results.count_errors())
print("Num Warnings: ", results.count_warnings())
```

## Errors and Warnings
### Errors
- 0001: No rate law entered 
- 0002: Expecting reactant in rate law but not found
### Warnings
#### Common Warnings
- 1001: Rate law contains only number
- 1002: Unrecognized rate law from the standard list (and the custom list if given)
- 1003: Flux is not increasing as reactant increases
- 1004: Flux is not decreasing as product increases
- 1005: Expecting boundary species reactant in rate law but not found
- 1006: Expecting parameters to be constants

#### Reversibility
- 1010: Irreversible reaction kinetic law contains products

#### Naming Conventions
- 1020: We recommend that these parameters start with 'k'
- 1021: We recommend that these parameters start with 'K'
- 1022: We recommend that these parameters start with 'V'

#### Formatting Conventions:
- 1030: Elements of the same type are not ordered properly
- 1031: Formatting convention not followed (compartment before parameters before species)
- 1032: Denominator not in alphabetical order
- 1033: Numerator and denominator not in alphabetical order
- 1034: Numerator convention not followed and denominator not in alphabetical order
- 1035: Denominator convention not followed
- 1036: Numerator not in alphabetical order and denominator convention not followed
- 1037: Numerator and denominator convention not followed
- Note that in 1035-1037, adding a parameter with species in the denominator's product terms differs from standard Michaelis-Menten kinetics, so we do not perform these checks.

#### SBOTerm Annotations:
- 1040: Uni-directional mass action annotation not following recommended SBO terms
- 1041: Uni-term with the moderator annotation not following recommended SBO terms
- 1042: Bi-directional mass action or Bi-terms with the moderator annotation not following recommended SBO terms
- 1043: Michaelis-Menten kinetics without an explicit enzyme annotation not following recommended SBO terms
- 1044: Michaelis-Menten kinetics with an explicit enzyme annotation not following recommended SBO terms

For more details about warnings and errors, please refer to "View Error Codes" button in [RateSB](https://sys-bio.github.io/ratesb/).

## Default Rate Law Classifications
Before the analysis, we classify each rate law into different categories (Xu, 2023). If a rate law does not belong to any of the default classes or the custom classification file provided, a warning will be raised.

The following categories are used for classifying rate laws:
- Zeroth order (ZERO): No reactant or product in the rate law.
- Uni-Directional Mass Action (UNDR): Direct, one-way reactions where all reactants influencing the rate law and resulting in a single product.
- Uni-Directional Mass Action with an Activator (UNDR-A): Similar to UNDR but includes an essential activator.
- Irreversible Enzymatic non-Mass Action Rate Law: Features at least one enzyme and not all reactants in the rate law.
- Bi-Directional Mass Action (BIDR): Covers reversible reactions with all reactants and products in the rate law.
- Bi-Directional Mass Action with Activator(s) (BIDR-A): Reversible reactions with activators, including enzymes different from reactants and products.
- Reversible Enzymatic non-Mass Action Rate Law: For reversible reactions where not all reactants or products are in the rate law, including at least one enzyme.
- Michaelis-Menten (MM): Describes enzymatic reactions based on substrate concentration, following specific Michaelis-Menten formulas without explicitly mentioning the enzyme.
- Michaelis-Menten with explicit enzyme (MMcat): Michaelis-Menten model explicitly incorporating the enzyme in the reaction rate equation.
- Allosteric and Inhibitors: Michaelis-Menten format affected by allosteric effects or inhibitors, altering reaction rates through enzyme or substrate modulation.
- Reversible Michaelis-Menten: Accounts for reaction reversibility in Michaelis-Menten format.
- Hill Equation: Describes enzyme kinetics in cooperative binding scenarios, relating reaction rate to substrate concentration through a sigmoidal curve.

The details of the default rate law classifications can be found in the [source code](https://github.com/sys-bio/ratesb_python/tree/main/ratesb_python/common).

[SBMLKinetics]: https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-023-05380-3#citeas

## Using Custom Rate Law Classifications

`ratesb_python` allows the use of custom rate law classifications. To utilize this, you must create a JSON file defining your rate laws. Each rate law object in the JSON file should include:

1. name: A string that specifies the name of the rate law.

2. expression: A valid mathematical equation using specific symbols (compartment, parameter, reactant1, reactant2, reactant3, product1, product2, product3, and enzyme). "species" is NOT allowed, instead you should specify whether a species is reactant, product or enzyme. Any other symbols should not be used in the expression. Mathematical operators such as +, -, *, /, **, and parentheses should be used to construct the equation.

3. optional_symbols: An array of symbols not necessarily required in the model's rate law.

4. power_limited_species: An array of species where the power (exponent) matters in the analysis. If a species is listed here, it should be raised to a specific power in the rate law (specified in the expression).

Here's an example of how to define your rate laws in the JSON file:

```json
[
    {
        "name": "Unidirectional Mass Action with two reactants",
        "expression": "compartment * parameter * reactant1 * reactant2**2",
        "optional_symbols": ["compartment", "parameter"],
        "power_limited_species": ["reactant1,reactant2"]
    },
    {
        "name": "Michaelis Menten",
        "expression": "compartment * parameter * reactant1 / (reactant1 + parameter)",
        "optional_symbols": ["compartment"],
        "power_limited_species": ["reactant1"]
    },
    {
        "name": "Your own rate law",
        "expression": "use: compartment, parameter, reactant1, reactant2, reactant3, product1, product2, product3, enzyme. Do NOT use: species",
        "optional_symbols": ["symbols that do not have to include in a rate law"],
        "power_limited_species": ["RateSB will pay attention to the power of these species (power matters in this case) symbols that have to be set to a certain power in a rate law (please specify power in the expression)"]
    }
    // Add more custom rate laws as needed
]
```

## Testing

For testing, run 
```bash
python -m unittest
```

## Release Notes

### 0.2.7
* Supported Local Parameters in SBML

### 0.2.6
* Created ReadTheDocs
* Bug Fixes
* Improved test coverage to 99%
* Supressed python 3.12 string warning

### 0.2.5
* Separated model reading from analysis
* Tested on 1054 biomodels and fixed bugs
* Added check_model method to allow user to use the package with one line
* Solved when running sympy with sympy builtin symbols that raise error such as "S", a reaction like "S->P;k1*S" would work now

For older versions and a full changelog, please check the repository's [CHANGELOG.md](https://github.com/sys-bio/ratesb_python/blob/main/CHANGELOG.md).

## Contributing

Contributions to `ratesb_python` are welcomed! Whether it's bug reports, feature requests, or new code contributions, we value your feedback and contributions. Please submit a pull request or open an issue on our [GitHub repo](https://github.com/sys-bio/ratesb_python).

## Developing



## License

`ratesb_python` is licensed under the MIT license. Please see the LICENSE file for more information.

## Future Works

* Implement stoichiometry checks for mass actions.
* Perform checks after default classification to optimize performance.
* Give user option to not use the default rate law classification to improve performance

## Known Issues

N/A

## Contact

For additional queries, please contact Longxuan Fan at longxuan@usc.edu.

We hope ratesb_python assists you effectively in your model rate law analysis!

## References

Xu, J. SBMLKinetics: a tool for annotation-independent classification of reaction kinetics for SBML models. BMC Bioinformatics 24, 248 (2023). https://doi.org/10.1186/s12859-023-05380-3