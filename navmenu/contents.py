from abc import ABC, abstractmethod


class BaseContent(ABC):
    def __getitem__(self, key):
        return getattr(self, key)

    @abstractmethod
    def serialize(self) -> dict:
        pass


class Content(BaseContent):
    def __init__(self, text: str = None) -> None:
        self.text = text

    def __repr__(self) -> str:
        return f'Content({repr(self.text)})'

    @staticmethod
    def keys() -> tuple[str]:
        return 'text',

    def serialize(self) -> dict:
        res = {}

        if self.text is not None:
            res['text'] = self.text

        return res
