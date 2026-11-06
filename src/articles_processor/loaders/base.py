from abc import ABC, abstractmethod
from typing import Any


class BaseLoader(ABC):
    @abstractmethod
    def load(self, source: str) -> Any:
        pass
