# ratesb_python: Rate Law Analysis for SBML and Antimony Models

`ratesb_python` is a Python package designed to analyze the rate laws in an SBML or Antimony model. It provides a user-friendly API to analyze your model and fetch warnings and errors. With `ratesb_python`, you can ensure that your models are robust and accurate.

## Features

- Analyze rate laws in SBML and Antimony models.
- Fetch a list of warnings and errors.
- Clear all results.
- Get all warnings or all errors separately.
- Get or remove all messages for a specific reaction.
- Get the total number of errors and warnings.

## Installation

To install `ratesb_python`, run the following command in your terminal:

``pip install ratesb_python``


## Usage

Here is a quick example of how to use the `ratesb_python` package:

```python
from ratesb_python.common.analyzer import Analyzer, Results

# assuming `model` is your model
analyzer = Analyzer("path/to/model.xml", "path/to/custom_classifications.json")

# Analyze the model
results = analyzer.analyze()

# Print all errors and warnings
print(results)

# Print only warnings
warnings = results.get_warnings()
for reaction, messages in warnings.items():
    print(reaction, messages)

# Get all messages related to a specific reaction
messages = results.get_messages_by_reaction("Reaction1")
print(messages)

# Remove all messages related to a specific reaction
results.remove_messages_by_reaction("Reaction1")

# Get the total number of errors and warnings
errors, warnings = results.count_messages()
print("Total Errors: ", errors)
print("Total Warnings: ", warnings)
```

## Using Custom Rate Law Classifications

`ratesb_python` allows you to use your own custom rate law classifications to analyze your models. You can do this by creating a JSON file that defines your rate laws.

# Rules for Creating Custom Rate Law Classification Files
The custom rate law classifications in ratesb are defined in a JSON file. This JSON file should be an array of rate law objects, each representing a distinct type of rate law. Each object must have the following keys:

1. name: A string that specifies the name of the rate law.

2. expression: A string that defines the formula of the rate law. The expression should be a valid mathematical equation using the provided symbols. The allowed symbols are: compartment, parameter, reactant1, reactant2, reactant3, product1, product2, product3, and enzyme. Note that species is NOT allowed. Any other symbols should not be used in the expression. Mathematical operators such as +, -, *, /, **, and parentheses should be used to construct the equation.

3. optional_symbols: An array of symbols that do not necessarily need to appear in the rate law of the model. Any symbol listed here is considered optional and its absence will not trigger a warning or error.

4. power_limited_species: An array of symbols that ratesb will pay special attention to during the analysis. These symbols are the species in the model where the power (the exponent to which they are raised) matters. If a species is listed here, it should be raised to a specific power in the rate law (specified in the expression).

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
]
```

## Contributing

Contributions to `ratesb_python` are welcomed! Whether it's bug reports, feature requests, or new code contributions, we value your feedback and contributions. Please submit a pull request or open an issue on our GitHub page.

## License

`ratesb_python` is licensed under the MIT license. Please see the LICENSE file for more information.

## Future Works

Improve performance of classifying Michaelis-Menten rate laws by switching the algorithm to custom rate law classification

## Contact

For any additional questions or comments, please contact:

Longxuan Fan: longxuan@usc.edu

We hope you find ratesb helpful for your model rate law analysis!
