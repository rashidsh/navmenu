import pytest

from navmenu.actions import MessageAction
from navmenu.contents import Content
from navmenu.item_contents import TextItemContent
from navmenu.items import Item
from navmenu.menu_manager import MenuManager
from navmenu.menus import Menu
from navmenu.state import MemoryStateHandler
from navmenu.responses import Message


@pytest.fixture
def menu():
    return Menu(Content('menu content'), (
        Item('item', TextItemContent('button title'), MessageAction('message text')),
    ))


@pytest.fixture
def menu_manager(menu):
    return MenuManager({
        'menu': menu,
    }, MemoryStateHandler('menu'))


def test_get_message(menu_manager):
    message = menu_manager.get_message()

    assert isinstance(message, Message)
    assert message.text == 'menu content'


def test_select(menu_manager):
    messages = menu_manager.select('item')

    assert len(messages) == 1
    assert isinstance(messages[0], Message)
    assert messages[0].text == 'message text'


def test_select_invalid_action(menu_manager):
    with pytest.raises(ValueError):
        menu_manager.select('invalid item')
