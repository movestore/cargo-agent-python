from abc import ABC, abstractmethod


class BaseAnalyzer(ABC):
    @abstractmethod
    def analyze(self, path: str) -> list:
        pass
