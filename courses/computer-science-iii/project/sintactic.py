class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.pos = -1
        self.advance()

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def parse(self):
        self.start()
        self.note_sequence()
        self.end()

    def start(self):
        if self.current_token.type == 'START':
            self.advance()
        else:
            self.error('START')

    def end(self):
        if self.current_token.type == 'END':
            self.advance()
        else:
            self.error('END')

    def note_sequence(self):
        self.note()
        while self.current_token and self.current_token.type == 'NOTE':
            self.note()

    def note(self):
        if self.current_token.type == 'NOTE':
            self.advance()
            if self.current_token.type == 'DURATION':
                self.advance()
            else:
                self.error('DURATION')
        else:
            self.error('NOTE')

    def error(self, expected):
        raise Exception(f"Syntax error: expected {expected}, found {self.current_token}")