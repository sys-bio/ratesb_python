Quick Start Guide
=================

This guide provides a quick introduction to using `ratesb_python`.

Simple Example
--------------

This shows how to check a simple model for rate law correctness. `ratesb_python` uses either SBML or a human-readable representation of SBML models called Antimony. The Antimony code for this example contains a single reaction with associated kinetics. After creating the Antimony string, use the

.. code-block:: python

   from ratesb_python import check_model
   print(check_model("S->P;k1*S; k1 = 0.1; S = 10"))

Output:

.. code-block:: text

   _J0:
     Warning 1004: Flux is not decreasing as product increases.
     Warning 1020: We recommend that these parameters start with 'k': a

Complex Example
---------------

This example shows how to use the `Analyzer` class to check a model for rate law correctness. The `Analyzer` class provides more control over the analysis process and allows for more detailed analysis of the model.

.. code-block:: python

   from ratesb_python import Analyzer

   analyzer = Analyzer("S1->P1; k1 * S1")

   # Analyze the model for rate law correctness
   analyzer.check_all()

   # Display all errors and warnings
   print(analyzer.results)

   # Check selected errors and warnings
   analyzer.checks([1, 2, 1001, 1002])

   print(analyzer.results)

   # Display only warnings
   warnings = analyzer.results.get_all_warnings()
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

This example shows how to use the custom rate law checker to check a model for rate law correctness. The custom rate law checker allows for the creation of custom rate law checks. For detailed information on creating custom rate law checks, see the Custom Rate Law Checks section.

Here is the custom rate law file in JSON format:

.. code-block:: json

    [
        {
            "name": "Your rate law check (Here is Uni-Directional Mass Action, which is included)",
            "expression": "compartment * parameter * reactant1",
            "optional_symbols": ["compartment", "parameter"],
            "power_limited_species": []
        }
    ]

Here is the Python code to use the custom rate law checker:

.. code-block:: python

    from ratesb_python import check_model

    # Load custom rate law checks
    custom_rate_law_file = "custom_rate_law.json"
    print(check_model("S1->P1; k1 * S1", custom_rate_law_file))

Or, you can use the `Analyzer` class to check a model for rate law correctness:

.. code-block:: python

    from ratesb_python import Analyzer

    # Load custom rate law checks
    custom_rate_law_file = "custom_rate_law.json"
    analyzer = Analyzer("S1->P1; k1 * S1", custom_rate_law_file)

    # Analyze the model for rate law correctness
    analyzer.check_all()
    print(analyzer.results)

`ratesb_python` provides more methods to analyze the model. For more information, see the API documentation.