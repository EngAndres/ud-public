from ..engines_subsystem import EngineFactory, Engine


class EngineFlyweight:

    def __init__(self):
        self.__engines = {}

    def create_engine(self, type_engine: str, price_engine) -> Engine:
        if price_engine not in self.__engines:
            if type_engine not in self.__engines[price_engine]:
                self.__engines[price_engine][type_engine] = EngineFactory.get_engine(
                    type_engine, price_engine
                )
        return self.__engines[price_engine][type_engine]
