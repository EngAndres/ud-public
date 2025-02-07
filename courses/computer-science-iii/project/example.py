"""This module is just an example of how to use the compiler."""

from compiler import Compiler

# =========== Example usage ========== #
def example1(compiler_: Compiler):
    """This function is an example of how to use the compiler."""
    input_text = """
    START 
    Cb5 1/2 F5 1/4 Ab5 1/4 Bb5 1/4 Bb5 1/8 Ab5 1 Fb5 1/8 As5 1/4 Cb5 1/16 As5 1/16
    END
    """
    compiler_.compile(input_text)

def example2(compiler_: Compiler):
    """This function is an example of how to use the compiler."""
    input_text = """
    START 
    C4 1/4 D4 1/4 E4 1/4 F4 1/4 G4 1/4 A4 1/4 B4 1/4 C5 1/4 
    END
    """
    compiler_.compile(input_text)


if __name__ == '__main__':
    compiler = Compiler()
    example2(compiler)
