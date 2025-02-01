import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

def lex(code):
    tokens = []
    token_specification = [
        ('NOTE', r'[A-G][1-8]'),  # Notes
        ('DURATION', r'\d+'),    # Duration
        ('START', r'START'),     # Start
        ('END', r'END'),         # End
        ('SKIP', r'[ \t]+'),     # Skip over spaces and tabs
        ('MISMATCH', r'.'),      # Any other character
    ]
    tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected')
        else:
            tokens.append(Token(kind, value))
    return tokens