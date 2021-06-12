from typing import Any, Optional, Sequence


class ButtonColors:
    """Button colors."""

    DEFAULT = 0
    PRIMARY = 1
    POSITIVE = 2
    NEGATIVE = 3


class KeyboardButton:
    """An object that represents a keyboard button."""

    __slots__ = 'payload', 'text', 'color'

    def __init__(self, payload: Any, text: str, color: Optional[int] = ButtonColors.DEFAULT) -> None:
        self.payload = payload
        self.text = text
        self.color = color

    def __repr__(self) -> str:
        return f'KeyboardButton({repr(self.payload)}, {repr(self.text)}, {self.color})'


class Keyboard:
    """An object that represents a keyboard."""

    __slots__ = 'lines',

    def __init__(self, lines: Optional[Sequence] = None) -> None:
        if lines is None:
            lines = []

        self.lines = lines

    def __repr__(self) -> str:
        return f'Keyboard({self.lines})'

    def add_button(self, button: KeyboardButton) -> None:
        """Add button to the last keyboard's line."""

        if len(self.lines) == 0:
            self.add_line()

        self.lines[-1].append(button)

    def add_line(self) -> None:
        """Add empty line to the keyboard."""

        self.lines.append([])
