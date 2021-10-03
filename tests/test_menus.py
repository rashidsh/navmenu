import pytest
import types

from navmenu.actions import MessageAction
from navmenu.contents import Content
from navmenu.item_contents import TextItemContent
from navmenu.items import Item
from navmenu.menus import Menu
from navmenu.responses import Message


@pytest.fixture
def menu_item():
    return Item('item', TextItemContent('button title'), MessageAction('message text'))


@pytest.fixture
def menu_item_2():
    return Item('hello', TextItemContent('say hello'), MessageAction('Hello!'))


@pytest.fixture
def menu(menu_item):
    return Menu(Content('menu content'), (
        menu_item,
    ))


@pytest.fixture
def formatted_menu_item():
    return Item('item', TextItemContent('button {user_id}'))


@pytest.fixture
def formatted_menu(formatted_menu_item):
    return Menu(Content('menu {user_id}'), (
        formatted_menu_item,
    ))


@pytest.fixture
def menu_with_default_action(menu_item):
    return Menu(Content('menu content'), (
        menu_item,
    ), default_action=MessageAction('default message'))


@pytest.fixture
def empty_menu():
    return Menu(Content('empty menu'))


def test_menu_content(menu):
    assert menu.content.text == 'menu content'


def test_menu_items(menu_item, menu):
    assert len(menu.items) == 1
    assert menu.items[0] == menu_item


def test_menu_select(menu):
    actions = menu.select('item')
    assert isinstance(actions, types.GeneratorType)

    message = next(actions, None)

    assert isinstance(message, Message)
    assert message.get_content().get('text') == 'message text'


def test_menu_select_invalid_item(menu):
    assert menu.select('invalid item') is None


def test_menu_select_default_item(menu_with_default_action):
    actions = menu_with_default_action.select('invalid item')
    assert isinstance(actions, tuple)

    message = actions[0]

    assert isinstance(message, Message)
    assert message.get_content().get('text') == 'default message'


def test_get_message(menu):
    message = menu.get_message()

    assert message.get_content().get('text') == 'menu content'
    assert len(message.keyboard.lines) == 1
    assert len(message.keyboard.lines[0]) == 1
    assert message.keyboard.lines[0][0].payload == 'item'
    assert message.keyboard.lines[0][0].text == 'button title'


def test_get_message_with_payload(formatted_menu):
    message = formatted_menu.get_message({'user_id': 123})

    assert message.get_content().get('text') == 'menu 123'
    assert message.keyboard.lines[0][0].text == 'button 123'


def test_menu_add_item(empty_menu, menu_item_2):
    empty_menu.add_item(menu_item_2)

    assert len(empty_menu.items) == 1
    assert empty_menu.items[0] is menu_item_2


def test_menu_add_item_with_immutable_item_list(menu, menu_item_2):
    with pytest.raises(RuntimeError):
        menu.add_item(menu_item_2)
