"""This module contains a couple of function to apply the lexical analysis to a given source code."""

import re

# ============= LOAD TOKENS AND RULES IN MEMORY ============= #
# list of tokens
keywords = ['alarm', 'begin', 'stop', 'repeat', 'monday', 'thuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
special_chars = [':', '(', ')', ',', '//'] # // for comments

# regular expression to validate specific tokens
numbers = '[0-9]+' # [0-9][0-9]* = [0-9]+
identifiers = ['[a-z][[a-z][0-9][_]]*']


# ============= LEXICAL ANALYSIS FUNCTIONS ============= #
def remove_comments(code: str) -> str:
    """This function removes all comments from the given code.
    
    Args:
        code(str): The source code to remove comments from.
    
    Returns:
        A string with the source code without comments.
    """
    # each line is divided by jump line character
    code_lines = code.split('\n')
    processed_code = []

    for line in code_lines:
        if line.strip()[:2] != '//':
            processed_code.append(line)
    
    return '\n'.join(processed_code)

def remove_spaces(code: str) -> str:
    """This function removes all the whitespaces from the given code."""
    return re.sub(r'\s+', '', code)

def remove_punctuation(code: str) -> str:
    code = re.sub(':', '', code)
    code = re.sub('\n', '', code)
    return code


def lexical_analysis(code: str):
    code = remove_comments(code)
    code = remove_spaces(code)
    code = remove_punctuation(code)
    return code
    # get tokens and lexemes


# ============= MAIN ============= #
if __name__ == '__main__':
    code = """
    // This is a comment
    alarm: 5, 10
    begin
        repeat
            // This is another comment
            monday: 5, 10
            thuesday: 5, 10
            wednesday: 5, 10
            thursday: 5, 10
            friday: 5, 10
            saturday: 5, 10
            sunday: 5, 10
        stop
    """
    print(code)
    print(50*'-')
    new_code = lexical_analysis(code)
    print(new_code)