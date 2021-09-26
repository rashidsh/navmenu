import pytest

from navmenu.actions import MessageAction
from navmenu.item_contents import TextItemContent
from navmenu.items import Item, LineBreakItem, ConditionalItem
from navmenu.responses import Message


@pytest.fixture
def item():
    return Item('item', TextItemContent('text'))


@pytest.fixture
def item_with_action():
    return Item('item', TextItemContent('text'), MessageAction('message'))


@pytest.fixture
def conditional_item():
    return ConditionalItem('item', TextItemContent('text'), MessageAction('message'), 'lambda x: x == 123')


def test_is_menu_item_available(item):
    assert item.is_available()


def test_item_on_select(item):
    assert item.on_select() == ()


def test_item_on_select_with_action(item_with_action):
    res = item_with_action.on_select()
    message = next(res, None)

    assert isinstance(message, Message)
    assert message.get_text() == 'message'


def test_item_get_content(item):
    content = item.get_content()

    assert isinstance(content, dict)
    assert content['type'] == 'button'
    assert content['text'] == 'text'
    assert content['payload'] == 'item'


def test_line_break_item_get_content():
    item = LineBreakItem()
    content = item.get_content()

    assert isinstance(content, dict)
    assert content['type'] == 'line_break'


def test_conditional_item(conditional_item):
    assert conditional_item.is_available(123)
    assert not conditional_item.is_available()
