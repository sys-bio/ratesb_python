from collections import OrderedDict

class Results:
    """
    A class to represent the analysis results of a model.
    """

    def __init__(self):
        """
        Initializes the Results instance with an empty OrderedDict for results,
        and sets the number of errors and warnings to zero.
        """
        self._results = OrderedDict()
        self._num_errors = 0
        self._num_warnings = 0

    def add_message(self, reaction_name: str, code: int, message: str, is_warning: bool = True):
        """
        Adds a new message to the results list.

        Args:
            reaction_name (str): The name of the reaction.
            code (int): The code associated with the message.
            message (str): The message content.
            is_warning (bool): Indicates if the message is a warning. Defaults to True.

        Raises:
            None
        """
        if is_warning:
            self._num_warnings += 1
        else:
            self._num_errors += 1

        if reaction_name not in self._results:
            self._results[reaction_name] = []
        self._results[reaction_name].append({"code": code, "message": message, "is_warning": is_warning})

    def clear_results(self):
        """
        Clears all results from the results list, resetting the number of errors and warnings.

        Args:
            None

        Raises:
            None
        """
        self._results = OrderedDict()
        self._num_errors = 0
        self._num_warnings = 0
    
    def get_all_warnings(self):
        """
        Retrieves all warnings as a dictionary of reaction names to warning messages.

        Returns:
            OrderedDict: A dictionary containing warnings grouped by reaction names.
        """
        warnings = OrderedDict()
        for reaction_name, messages in self._results.items():
            warnings[reaction_name] = [msg for msg in messages if msg['is_warning']]
            if len(warnings[reaction_name]) == 0:
                del warnings[reaction_name]
        return warnings
    
    def get_all_errors(self):
        """
        Retrieves all errors as a dictionary of reaction names to error messages.

        Returns:
            OrderedDict: A dictionary containing errors grouped by reaction names.
        """
        errors = OrderedDict()
        for reaction_name, messages in self._results.items():
            errors[reaction_name] = [msg for msg in messages if not msg['is_warning']]
            if len(errors[reaction_name]) == 0:
                del errors[reaction_name]
        return errors
    
    def get_messages_by_reaction(self, reaction_name: str):
        """
        Retrieves all messages for a specific reaction.

        Args:
            reaction_name (str): The name of the reaction.

        Returns:
            list: A list of messages for the specified reaction.
        """
        return self._results.get(reaction_name, []).copy()
    
    def remove_messages_by_reaction(self, reaction_name: str):
        """
        Removes all messages for a specific reaction.

        Args:
            reaction_name (str): The name of the reaction.

        Raises:
            None
        """
        if reaction_name in self._results:
            for message in self._results[reaction_name]:
                if message['is_warning']:
                    self._num_warnings -= 1
                else:
                    self._num_errors -= 1
            del self._results[reaction_name]
        
    def count_messages(self):
        """
        Counts the total number of messages (errors and warnings).

        Returns:
            int: The total number of messages.
        """
        return self._num_errors + self._num_warnings
    
    def count_errors(self):
        """
        Counts the total number of errors.

        Returns:
            int: The total number of errors.
        """
        return self._num_errors

    def count_warnings(self):
        """
        Counts the total number of warnings.

        Returns:
            int: The total number of warnings.
        """
        return self._num_warnings

    def __repr__(self):
        """
        Returns a string representation of the results.

        Returns:
            str: A formatted string representing the results.
        """
        if self.count_messages() == 0:
            return 'No errors or warnings found.'
        str_repr = ''
        for reaction_name, messages in self._results.items():
            str_repr += f'{reaction_name}:\n'
            for message in messages:
                is_warning = message['is_warning']
                code = message['code']
                message_body = message['message']
                if is_warning:
                    str_repr += f'  Warning {str(code)}: {message_body}\n'
                else:
                    str_repr += f'  Error 000{str(code)}: {message_body}\n'
        return str_repr