from collections import OrderedDict

class Results:
    """
    A class used to represent the analysis results of a model.
    
    Rep invariant: 
        num_errors >= 0, num_warnings >= 0
        num_errors = number of errors, num_warnings = number of warnings
        
    Attributes:
        results (OrderedDict): A dictionary of the results.
        num_errors (int): The number of errors.
        num_warnings (int): The number of warnings.
    """
    
    def __init__(self):
        self.results = OrderedDict()
        self.num_errors = 0
        self.num_warnings = 0

    def add_message(self, reaction_name: str, code: int, message: str, is_warning=True):
        """
        Adds a new result to the results list.

        Args:
            reaction_name (str): name of the reaction
            code (int): Code of the message.
            message (str): The message to be added.
            is_warning (bool): if the message is warning message.
        """
        if is_warning:
            self.num_warnings += 1
        else:
            self.num_errors += 1
        if reaction_name not in self.results:
            self.results[reaction_name] = []
        self.results[reaction_name].append({"code": code, "message": message, "is_warning": is_warning})

    def clear_results(self):
        """
        Clears all results from the results list.
        """
        self.results = OrderedDict()
        self.num_errors = 0
        self.num_warnings = 0
    
    def get_warnings(self):
        """
        Returns all the warnings.
        """
        warnings = OrderedDict()
        for reaction_name, messages in self.results.items():
            warnings[reaction_name] = [msg for msg in messages if msg['is_warning']]
            if len(warnings[reaction_name]) == 0:
                del warnings[reaction_name]
        return warnings
    
    def get_errors(self):
        """
        Returns all the errors.
        """
        errors = OrderedDict()
        for reaction_name, messages in self.results.items():
            errors[reaction_name] = [msg for msg in messages if not msg['is_warning']]
            if len(errors[reaction_name]) == 0:
                del errors[reaction_name]
        return errors
    
    def get_messages_by_reaction(self, reaction_name: str):
        """
        Returns all the messages for a specific reaction.
        """
        return self.results.get(reaction_name, []).copy()
    
    def remove_messages_by_reaction(self, reaction_name: str):
        """
        Removes all the messages for a specific reaction.
        """
        if reaction_name in self.results:
            for message in self.results[reaction_name]:
                if message['is_warning']:
                    self.num_warnings -= 1
                else:
                    self.num_errors -= 1
            del self.results[reaction_name]
        
    
    def count_messages(self):
        """
        Returns the total number of errors and warnings.
        """
        return self.num_errors + self.num_warnings
    
    def count_errors(self):
        """
        Returns the total number of errors.
        """
        return self.num_errors

    def count_warnings(self):
        """
        Returns the total number of warnings.
        """
        return self.num_warnings

    def __repr__(self):
        """
        Overrides the __repr__ method.

        Returns:
            str: A string representation of the results.
        """
        str_repr = ''
        for reaction_name, messages in self.results.items():
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