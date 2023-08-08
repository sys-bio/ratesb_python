from collections import OrderedDict

class Results:
    def __init__(self):
        self.results = OrderedDict()

    def add_message(self, reaction_name: str, code: int, message: str, is_warning=True):
        """
        Adds a new result to the results list.

        Args:
            reaction_name (str): name of the reaction
            code (int): Code of the message.
            message (str): The message to be added.
            is_warning (bool): if the message is warning message.
        """
        if reaction_name not in self.results:
            self.results[reaction_name] = []
        self.results[reaction_name].append({"code": code, "message": message, "is_warning": is_warning})

    def clear_results(self):
        """
        Clears all results from the results list.
        """
        self.results = OrderedDict()
    
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
        return self.results.get(reaction_name, [])
    
    def remove_messages_by_reaction(self, reaction_name: str):
        """
        Removes all the messages for a specific reaction.
        """
        if reaction_name in self.results:
            del self.results[reaction_name]
    
    def count_messages(self):
        """
        Returns the total number of errors and warnings.
        """
        total_errors = sum(1 for messages in self.results.values() for msg in messages if not msg['is_warning'])
        total_warnings = sum(1 for messages in self.results.values() for msg in messages if msg['is_warning'])
        return total_errors, total_warnings

    def __str__(self):
        """
        Overrides the __str__ method to print the results.

        Returns:
            str: A string representation of the results.
        """
        str_repr = ''
        # str_repr += f"Total errors and warnings: {str(self.count_messages)}"
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
    
    def to_html(self):
        """
        Converts the results to HTML format.
        
        Returns:
            str: A string representation of the results in HTML format.
        """
        html_repr = '<table style="width:100%; border:1px solid black;">'
        
        # Header
        html_repr += '<tr><th>Reaction</th><th>Type</th><th>Code</th><th>Message</th></tr>'

        # Data Rows
        for reaction_name, messages in self.results.items():
            for message in messages:
                is_warning = message['is_warning']
                code = message['code']
                message_body = message['message']
                message_type = 'Warning' if is_warning else 'Error'
                html_repr += f'<tr><td>{reaction_name}</td><td>{message_type}</td><td>{code}</td><td>{message_body}</td></tr>'
        
        html_repr += '</table>'
        return html_repr

