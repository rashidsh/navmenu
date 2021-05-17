from abc import ABC, abstractmethod
from typing import Iterator, Optional

from .actions import Action
from .item_contents import ItemContent


class BaseItem(ABC):
    __slots__ = 'name', 'action'

    def __init__(self, name: str = None, action: Action = None) -> None:
        self.name = name
        self.action = action

    def __repr__(self) -> str:
        return f'BaseItem({repr(self.name)}, {self.action})'

    @abstractmethod
    def get_content(self) -> dict:
        pass

    def is_available(self, payload: Optional[dict] = None) -> bool:
        return True

    def on_select(self, payload: Optional[dict] = None) -> Iterator:
        if self.action is None:
            return ()

        actions = (self.action, ) if isinstance(self.action, Action) else self.action
        return (action.process(payload) for action in actions)

    def serialize(self) -> dict:
        res = {}

        if self.name is not None:
            res['name'] = self.name

        if self.action is not None:
            res['action'] = {
                'type': self.action.__class__.__name__,
                **self.action.serialize(),
            }

        return res


class Item(BaseItem):
    __slots__ = 'content',

    def __init__(self, name: str, content: ItemContent, action: Action = None) -> None:
        super().__init__(name, action)

        self.content = content

    def __repr__(self) -> str:
        return f'Item({repr(self.name)}, {self.content}, {self.action})'

    def get_content(self) -> dict:
        return self.content.get_content(self.name)

    def serialize(self) -> dict:
        res = super().serialize()

        res['content'] = {
            'type': self.content.__class__.__name__,
            **self.content.serialize(),
        }

        return res


class LineBreakItem(BaseItem):
    __slots__ = ()

    def __repr__(self) -> str:
        return 'LineBreakItem()'

    def get_content(self) -> dict:
        return {
            'type': 'line_break',
        }


class ConditionalItem(Item):
    __slots__ = 'condition',

    def __init__(self, name: str, content: ItemContent, action: Action, condition: str) -> None:
        super().__init__(name, content, action)

        self.condition = condition

    def __repr__(self) -> str:
        return f'ConditionalItem({repr(self.name)}, {self.content}, {self.action}, {repr(self.condition)})'

    def is_available(self, payload: Optional[dict] = None) -> bool:
        return eval(self.condition)(payload)

    def serialize(self) -> dict:
        res = super().serialize()

        res['condition'] = self.condition

        return res
