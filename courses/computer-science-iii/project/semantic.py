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
        """
        Analyzes the tokens and returns a tuple containing:
            - A list of notes as (note, duration) pairs.
            - The time signature as a string.

        Expected input format:
            START
            TIME 4/4
            C4 1/4 D4 1/4 ...
            END
        """
        time_signature = None
        # Iterate through tokens
        token_count = len(self.tokens)
        i = 0
        while i < token_count:
            token = self.tokens[i]
            if token.type_ == "KEYWORDS":
                # If token is TIME keyword then next token (if DURATION) is the time signature.
                if token.value == "TIME":
                    if i + 1 < token_count and self.tokens[i + 1].type_ == "DURATION":
                        time_signature = self.tokens[i + 1].value
                        i += 2
                        continue
                    else:
                        raise Exception("Expected DURATION token after TIME keyword.")
                # Skip other keywords like START and END.
                i += 1
            elif token.type_ == "NOTE":
                # Append note with duration placeholder None.
                self.notes.append((token.value, None))
                i += 1
            elif token.type_ == "DURATION":
                # Associate DURATION to the most recent note if not already set.
                if self.notes and self.notes[-1][1] is None:
                    self.notes[-1] = (self.notes[-1][0], token.value)
                i += 1
            else:
                i += 1

        return self.notes, time_signature
    
# START TIME 4/4 A3 B3 Cs4 END  -> ([A3, B3, Cs4], 4/4)