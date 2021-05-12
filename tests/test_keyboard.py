from navmenu.keyboard import Keyboard, KeyboardButton


def test_keyboard():
    keyboard = Keyboard()
    keyboard.add_button(KeyboardButton(1, 'button 1'))
    keyboard.add_button(KeyboardButton(2, 'button 2'))
    keyboard.add_line()
    keyboard.add_button(KeyboardButton(3, 'button 3'))

    assert len(keyboard.lines) == 2
    assert len(keyboard.lines[0]) == 2
    assert len(keyboard.lines[1]) == 1
    assert isinstance(keyboard.lines[1][0], KeyboardButton)


def test_create_keyboard_from_lines():
    keyboard = Keyboard(((
        KeyboardButton(1, 'button 1'),
        KeyboardButton(2, 'button 2'),
        KeyboardButton(3, 'button 3'),
    ),))

    assert len(keyboard.lines) == 1
    assert len(keyboard.lines[0]) == 3
    assert isinstance(keyboard.lines[0][0], KeyboardButton)
