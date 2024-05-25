API Documentation
=================

Analyzer
--------

.. autoclass:: ratesb_python.analyzer.Analyzer
   :members:
   :undoc-members:
   :show-inheritance:

   .. method:: check_model(model_str: str, rate_law_classifications_path: str=None, abort_on_complicated_rate_laws: bool=True, excluded_codes: List[int]=[])

      Checks the SBML model for rate law errors and warnings.

      **Parameters:**

         - **model_str** (*str*): Path to the model file, or the string representation of model.
         - **rate_law_classifications_path** (*str*): Path to the rate law classification file.
         - **abort_on_complicated_rate_laws** (*bool*): If True, the check will abort if the rate law is too complicated to process.
         - **excluded_codes** (*List[int]*): List of codes of the checks to exclude. If None, all checks are performed.

      **Returns:**

         The results of the checks as a result object, can be printed or converted to string.

   .. method:: list_all_checks()

      Returns a string representation of all the checks.

      **Returns:**

         A string listing all error and warning checks.

   .. method:: list_check(code: int)

      Returns a string representation of the check corresponding to the provided code.

      **Parameters:**

         - **code** (*int*): The code of the check.

      **Returns:**

         A string describing the check corresponding to the provided code.

   .. method:: __init__(model_str: str, rate_law_classifications_path: str=None, abort_on_complicated_rate_laws: bool=True)

      Initializes the Analyzer class.

      **Parameters:**

         - **model_str** (*str*): Path to the model file, or the string representation of model.
         - **rate_law_classifications_path** (*str*): Path to the rate law classification file.
         - **abort_on_complicated_rate_laws** (*bool*): If True, the check will abort if the rate law is too complicated to process.

      **Examples:**

      ::

         from ratesb_python.analyzer import Analyzer
         analyzer = Analyzer("path/to/biomodel.xml", "path/to/rate_laws.json")
         analyzer.check_all()
         results = analyzer.results
         print(str(results))
         str(results)

   .. method:: check_except(excluded_codes: Optional[List[int]]=[])

      Performs all checks except the ones corresponding to the provided list of error or warning codes.

      **Parameters:**

         - **excluded_codes** (*Optional[List[int]]*): List of codes of the checks to exclude. If None, all checks are performed.

      **Updates:**

         The results of the check(s) to self.results.

   .. method:: check_all()

      Performs all checks.

      **Updates:**

         The results of the check_all to self.results.

   .. method:: checks(codes: List[int])

      Performs multiple checks based on the provided list of error or warning codes. If no codes are provided, all checks are performed.

      **Parameters:**

         - **codes** (*List[int]*): List of codes of the checks to perform.

      **Updates:**

         The results of the checks to self.results.

Results
-------

.. autoclass:: ratesb_python.results.Results
   :members:
   :undoc-members:
   :show-inheritance:

   .. method:: __init__()

      Initializes the Results class.

   .. method:: add_message(reaction_name: str, code: int, message: str, is_warning=True)

      Adds a new result to the results list.

      **Parameters:**

         - **reaction_name** (*str*): Name of the reaction.
         - **code** (*int*): Code of the message.
         - **message** (*str*): The message to be added.
         - **is_warning** (*bool*): If the message is a warning message.

   .. method:: clear_results()

      Clears all results from the results list.

   .. method:: get_all_warnings()

      Returns all the warnings as a list of strings.

      **Returns:**

         A list of warnings.

   .. method:: get_all_errors()

      Returns all the errors.

      **Returns:**

         A list of errors.

   .. method:: get_messages_by_reaction(reaction_name: str)

      Returns all the messages for a specific reaction.

      **Parameters:**

         - **reaction_name** (*str*): Name of the reaction.

      **Returns:**

         A list of messages for the specified reaction.

   .. method:: remove_messages_by_reaction(reaction_name: str)

      Removes all the messages for a specific reaction.

      **Parameters:**

         - **reaction_name** (*str*): Name of the reaction.

   .. method:: count_messages()

      Returns the total number of errors and warnings.

      **Returns:**

         The total count of errors and warnings.

   .. method:: count_errors()

      Returns the total number of errors.

      **Returns:**

         The total count of errors.

   .. method:: count_warnings()

      Returns the total number of warnings.

      **Returns:**

         The total count of warnings.

   .. method:: __repr__()

      Overrides the __repr__ method.

      **Returns:**

         str: A string representation of the results.
