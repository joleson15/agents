from abc import ABC, abstractmethod

class ModelProvider(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def send_message(self) -> None:
        """abstract method for invoke"""