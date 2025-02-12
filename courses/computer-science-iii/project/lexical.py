"""This module represents the behavior of a lexical analyzer.

Author: Carlos Andres Sierra <casierrav@udistrital.edu.co>
"""

import re


# pylint: disable=too-few-public-methods
class Token:
    """This class represents the data structure of a token.
    It means: a type of token and its value (lexema)."""

    def __init__(self, type_: str, value):
        self.type_ = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type_}, {self.value})"


class LexicalAnalyzer:
    """This class represents the behavior of a lexical analyzer."""

    @staticmethod
    def lex(code):
        """This method receives a code and returns a list of tokens."""
        tokens = []
        token_specification = [
            (
                "NOTE",
                r"[A-G][b-s]{0,1}[1-8]",
            ),  # Notes: A-B-C-D-E-F-G followed by 1-8 (octave)
            ("DURATION", r"\d+/\d+|\d+"),  # Duration
            ("KEYWORDS", r"START|END|TIME"),  # Start-End
            ("SKIP", r"[ \t]+"),  # Skip over spaces and tabs
            ("MISMATCH", r"."),  # Any other character
        ]

        tok_regex = "|".join(
            f"(?P<{pair[0]}>{pair[1]})" for pair in token_specification
        )
        for mo in re.finditer(tok_regex, code):
            kind = mo.lastgroup
            value = mo.group()

            if kind == "MISMATCH":
                # throws an error if the character is not recognized
                raise RuntimeError(f"{value} unexpected")
            if kind == "SKIP":
                # ignores spaces and tabs
                continue
            # if all validations are fine, just add as a new token
            tokens.append(Token(kind, value))

        # Remove tokens that are spaces or sequences of spaces
        tokens = [token for token in tokens if token.type_ != "SKIP"]

        return tokens
