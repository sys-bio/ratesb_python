Using Custom Rate Law Classifications
=====================================

`ratesb_python` allows the use of custom rate law classifications. To utilize this, you must create a JSON file defining your rate laws. Each rate law object in the JSON file should include:

1. **name**: A string that specifies the name of the rate law.
2. **expression**: A valid mathematical equation using specific symbols (compartment, parameter, reactant1, reactant2, reactant3, product1, product2, product3, and enzyme). "species" is NOT allowed, instead you should specify whether a species is reactant, product or enzyme. Any other symbols should not be used in the expression. Mathematical operators such as +, -, *, /, **, and parentheses should be used to construct the equation.
3. **optional_symbols**: An array of symbols not necessarily required in the model's rate law.
4. **power_limited_species**: An array of species where the power (exponent) matters in the analysis. If a species is listed here, it should be raised to a specific power in the rate law (specified in the expression).

Here's an example of how to define your rate laws in the JSON file:

.. code-block:: json

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
