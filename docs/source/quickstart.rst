Quick Start Guide
=================

This guide provides a quick introduction to using `ratesb_python`.

Simple Example
--------------

.. literalinclude:: ../../examples/simple_example.py
   :language: python
   :caption: Simple example using check_model
   :name: simple-example

Complex Example
---------------

.. literalinclude:: ../../examples/complex_example.py
   :language: python
   :caption: Complex example using Analyzer
   :name: complex-example

This example shows how to use the custom rate law checker to check a model for rate law correctness. The custom rate law checker allows for the creation of custom rate law checks. For detailed information on creating custom rate law checks, see the Custom Rate Law Checks section.

Here is the custom rate law file in JSON format:

.. literalinclude:: ../../examples/classification_tutorial.json

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