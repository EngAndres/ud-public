from scientific_calculator import ScientificCalculator

class EngineeringCalculator(ScientificCalculator):
    pass


test_eng = EngineeringCalculator()
print(test_eng.sum(3,4))
print(test_eng.square(5))