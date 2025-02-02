"""This module is just an example of how to use the compiler."""

from compiler import Compiler

# =========== Example usage ========== #
def example1(compiler_: Compiler):
    """This function is an example of how to use the compiler."""
    input_text = """
    START
    Cb4 1/2 F5 1/4 Ab5 1/4 Bb5 1/4 Bb5 1/8 Ab5 1 Fb5 1/8
    END
    """
    compiler_.compile(input_text)

def example2(compiler_: Compiler):
    """This function is an example of how to use the compiler."""
    input_text = """
    START
    C4 1 D4 1 E4 1 F4 1 G4 1 A4 1 B4 1 C5 1
    END
    """
    compiler_.compile(input_text)

if __name__ == '__main__':
    compiler = Compiler()
    example1(compiler)
