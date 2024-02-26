from abc import ABC, abstractmethod

class IDataCollector(ABC):
    @abstractmethod
    def get_meal(self, input: str, input_type: str) -> None:
        pass