from typing import Optional

from .keyboard import Keyboard


class Message:
    """An object that represents a message.

    Args:
        text: The message text.
        keyboard: The message keyboard.
        payload: The message payload.
    """

    __slots__ = 'keyboard', 'text', 'payload'

    def __init__(
            self, text: Optional[str] = None, keyboard: Optional[Keyboard] = None, payload: Optional[dict] = None
    ) -> None:
        if payload is None:
            payload = {}

        self.keyboard = keyboard
        self.text = text
        self.payload = payload

    def __repr__(self) -> str:
        return f'Message({repr(self.text)}, {self.keyboard}, {self.payload})'

    def get_text(self) -> Optional[str]:
        """Format and return message text.

        Returns:
            Formatted message text.
        """
        return self.text.format(**self.payload) if self.text is not None else None

    def update_payload(self, payload: dict) -> None:
        """Update the message payload.

        Args:
            payload: New message payload.
        """
        self.payload = payload

    def serialize(self) -> dict:
        """Serialize the class instance to a dictionary.

        Returns:
            A serialized class instance.
        """
        res = {}

        if self.text is not None:
            res['text'] = self.text

        if self.payload:
            res['payload'] = self.payload

        return res


class Response:
    """An object that represents a message and can be used to change the current menu.

    Args:
        message: The message.
        menu: The name of the menu to go to.
        go_back_count: How many steps to go back.
    """

    __slots__ = 'message', 'menu', 'go_back_count'

    def __init__(
            self, message: Optional[Message] = None, menu: Optional[str] = None, go_back_count: Optional[int] = None
    ) -> None:
        self.message = message
        self.menu = menu
        self.go_back_count = go_back_count

    def __repr__(self) -> str:
        return f'Response({self.message}, {repr(self.menu)}, {self.go_back_count})'

    def update_payload(self, payload: dict) -> None:
        """Update the message payload.

        Args:
            payload: New message payload.
        """
        if self.message is not None:
            self.message.update_payload(payload)

    def serialize(self) -> dict:
        """Serialize the class instance to a dictionary.

        Returns:
            A serialized class instance.
        """
        res = {}

        if self.message is not None:
            res['message'] = {
                'type': self.message.__class__.__name__,
                **self.message.serialize(),
            }

        if self.menu is not None:
            res['menu'] = self.menu

        if self.go_back_count is not None:
            res['go_back_count'] = self.go_back_count

        return res
