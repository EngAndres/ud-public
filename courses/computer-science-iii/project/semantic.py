"""This module represents the behavior of a semantic analyzer.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
"""

# pylint: disable=too-few-public-methods
class SemanticAnalyzer:
    """This class represents the behavior of a semantic analyzer."""

    def __init__(self, tokens_input: list):
        self.tokens = tokens_input
        self.notes = []

    def analyze(self):
        """This method analyzes the tokens and returns the notes."""
        for token in self.tokens:
            if token.type == 'NOTE':
                self.notes.append((token.value, None))
            elif token.type == 'DURATION':
                if self.notes:
                    self.notes[-1] = (self.notes[-1][0], token.value)
        return self.notes
    