from calculator import Calc

class ScientificCalculator(Calc):
    
    def __init__(self):
        super().__init__()

    def square(self, num: float) -> float:
        """This method returns the square of a number.

        Args:
            num(float): Number to be squared.

        Returns:
            The square of the number.
        """
        return num ** 2
