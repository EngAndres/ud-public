"""This module represents the behavior of a syntactic analyzer.

Author: Carlos Andres Sierra <casierrav@udistrital.edu.co>
"""

# GRAMMAR DEFINITION:
# <S> -> "START" <NOTE_SEQUENCE> "END"
# <NOTE_SEQUENCE> -> <NOTE> <NOTE_DURATION> <NOTE_SEQUENCE> | <NOTE> <NOTE_DURATION>
# <NOTE> -> ("A" | "B" | "C" | "D" | "E" | "F" | "G") <OCTAVE>
# <OCTAVE> -> "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8"
# <NOTE_DURATION> -> <DURATION> | "1 /" <FAST_DURATION>
# <DURATION> -> "1" | "2" | "4"
# <FAST_DURATION> -> "2" | "4" | "8"


class Parser:
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
        This just follows the structure of the grammar."""
        self.start()
        self.note_sequence()
        self.end()

    def start(self):
        """This method checks if the first token is 'START'."""
        if self.current_token.type == 'START':
            self.advance()
        else:
            self.error('START')

    def end(self):
        """This method checks if the last token is 'END'."""
        if self.current_token.type == 'END':
            self.advance()
            if self.current_token is not None:
                self.error('END')

    def note_sequence(self):
        """This method checks if the sequence of notes is correct."""
        self.note()
        while self.current_token and self.current_token.type == 'NOTE':
            self.note()

    def note(self):
        """This method checks if the note is correct."""
        if self.current_token.type == 'NOTE':
            self.advance()
            if self.current_token.type == 'DURATION':
                self.advance()
            else:
                self.error('DURATION')
        else:
            self.error('NOTE')

    def error(self, expected):
        """This method raises an exception if the current token is not the expected one.
        
        Args:
            expected (str): The expected token.
        """
        raise Exception(f"Syntax error: expected {expected}, found {self.current_token}")
    