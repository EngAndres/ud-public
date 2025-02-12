"""This module represents the behavior of a syntactic analyzer.

Author: Carlos Andres Sierra <casierrav@udistrital.edu.co>
"""

# GRAMMAR DEFINITION:
# <S>             -> "START" <TIME> <NOTE_SEQUENCE> "END"
# <TIME>          -> "TIME" <DURATION>
# <NOTE_SEQUENCE> -> <NOTE> <NOTE_DURATION> <NOTE_SEQUENCE> | <NOTE> <NOTE_DURATION>
# <NOTE>          -> ("A" | "B" | "C" | "D" | "E" | "F" | "G") <OCTAVE>
# <OCTAVE>        -> "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8"
# <DIGIT>         -> "1" | "2" | "3" | "4" | ... | "18" | "19" | "20"
# <DURATION>      -> <DIGIT> "/" <DIGIT>
# <NOTE_DURATION> -> "1" | "1/" <FAST_DURATION>
# <FAST_DURATION> -> "2" | "4" | "8" | "16"


class SintacticAnalyzer:
    """This class represents the behavior of a syntactic analyzer."""

    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.pos = -1
        self.advance()

    def advance(self):
        """This method advances the current token
        to the next token."""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def parse(self):
        """This method starts the parsing process.
        This just follows the structure of the grammar.
        """
        self.start()
        self.time_signature()
        self.note_sequence()
        self.end()

    def start(self):
        """This method checks if the first token is 'START'."""
        if (
            self.current_token.type_ == "KEYWORDS"
            and self.current_token.value == "START"
        ):
            self.advance()
        else:
            self.error("START")

    def end(self):
        """This method checks if the last token is 'END'."""
        if (
            self.current_token
            and self.current_token.type_ == "KEYWORDS"
            and self.current_token.value == "END"
        ):
            self.advance()
            if self.current_token is not None:
                self.error("No extra tokens expected after END")
        else:
            self.error("END")

    def time_signature(self):
        """This method processes the TIME signature:
        expecting 'TIME' keyword followed by a DURATION token.
        """
        if (
            self.current_token
            and self.current_token.type_ == "KEYWORDS"
            and self.current_token.value == "TIME"
        ):
            self.advance()
            if self.current_token and self.current_token.type_ == "DURATION":
                # Process time signature; you might store it for later.
                time_sig = self.current_token.value
                print(f"Time Signature Detected: {time_sig}")
                self.advance()
            else:
                self.error("DURATION after TIME")
        else:
            self.error("TIME")

    def note_sequence(self):
        """This method checks if the sequence of notes is correct."""
        self.note()
        while self.current_token and self.current_token.type_ == "NOTE":
            self.note()

    def note(self):
        """This method checks if the note is correct.
        Here you would typically also verify the following duration token.
        """
        if self.current_token and self.current_token.type_ == "NOTE":
            note_value = self.current_token.value
            self.advance()
            # Check for duration following the note
            if self.current_token and self.current_token.type_ == "DURATION":
                duration_value = self.current_token.value
                print(f"Note: {note_value} Duration: {duration_value}")
                self.advance()
            else:
                self.error("DURATION after NOTE")
        else:
            self.error("NOTE")

    def error(self, expected):
        """This method raises an exception if the current token is not the expected one.

        Args:
            expected (str): The expected token.
        """
        raise SyntaxError(
            f"Syntax error: expected {expected}, found {self.current_token}"
        )
