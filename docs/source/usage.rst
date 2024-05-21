Usage
=====

This section provides detailed usage examples for `ratesb_python`.

Simple Example
--------------

Here’s a simple example of using `ratesb_python`:

.. code-block:: python

   from ratesb_python import check_model
   print(check_model("S->P;k1*S"))

Complex Example
---------------

For more complex use cases, follow the example below:

.. code-block:: python

   from ratesb_python import Analyzer

   # Assuming `model` is your SBML or Antimony model
   analyzer = Analyzer("path/to/model.xml", "path/to/custom_classifications.json")
   # or:
   analyzer2 = Analyzer("S1->P1; k1 * S1") # custom classification file is optional

   # Analyze the model for rate law correctness
   analyzer.check_all()
   results = analyzer.results

   # Display all errors and warnings
   print(results)

   # Check selected errors and warnings
   analyzer.checks([1, 2, 1001, 1002])

   # No need to set results = analyzer.results again as results updates automatically
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
