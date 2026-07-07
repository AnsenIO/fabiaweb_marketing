from abc import ABC, abstractmethod


class Publisher(ABC):
    name: str = "base"

    @abstractmethod
    def publish(self, content: str, metadata: dict) -> dict:
        ...
