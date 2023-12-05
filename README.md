# ratesb_python: Rate Law Analysis for SBML and Antimony Models

`ratesb_python` is a Python package designed for analyzing rate laws in SBML (Systems Biology Markup Language) and Antimony models, which are commonly used in systems biology for representing biological networks. This package offers a user-friendly API to help ensure that your models are robust and accurate by providing detailed warnings and errors related to rate laws.

## Installation

To install `ratesb_python`, execute the following command in your terminal:

```bash
pip install ratesb_python
```

## Usage

Below is an example demonstrating how to use the ratesb_python package:

```python
from ratesb_python.common.analyzer import Analyzer

# Assuming `model` is your SBML or Antimony model
analyzer = Analyzer("path/to/model.xml", "path/to/custom_classifications.json")

# Analyze the model for rate law correctness
results = analyzer.check()

# Display all errors and warnings
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

# Get total errors and warnings
errors, warnings = results.count_messages()
print("Total Errors: ", errors)
print("Total Warnings: ", warnings)
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
Before the analysis, we classify each rate law into different categories. If a rate law does not belong to any of the default classes or the custom classification file provided, a warning will be raised.

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

## Versions

0.1.0: initial release, used SBMLKinetics for rate law classifications

0.2.0: removed numpy dependency, updated rate law classifications scheme, no longer using SBMLKinetics for rate law classifications. Restructured code for web integration.

## Contributing

Contributions to `ratesb_python` are welcomed! Whether it's bug reports, feature requests, or new code contributions, we value your feedback and contributions. Please submit a pull request or open an issue on our [GitHub repo](https://github.com/sys-bio/ratesb_python).

## License

`ratesb_python` is licensed under the MIT license. Please see the LICENSE file for more information.

## Future Works

- Implement stoichiometry checks for mass actions.
- Perform checks after default classification to optimize performance.

## Known bugs

- checks with no argument does not work properly

## Contact

For additional queries, please contact Longxuan Fan at longxuan@usc.edu.

We hope ratesb_python assists you effectively in your model rate law analysis!
