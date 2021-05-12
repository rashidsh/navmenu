import pytest

from navmenu.actions import MessageAction, SubmenuAction, GoBackAction, ExecuteAction, FunctionAction
from navmenu.responses import Message, Response


@pytest.fixture
def function_action():
    def func(payload):
        return Message(f"user {payload['user_id']}")

    return func


def test_message_action():
    action = MessageAction('message')
    res = action.process(None)

    assert isinstance(res, Message)
    assert res.text == 'message'


def test_submenu_action():
    action = SubmenuAction('new menu')
    res = action.process(None)

    assert isinstance(res, Response)
    assert res.menu == 'new menu'


def test_go_back_action():
    action = GoBackAction()
    res = action.process(None)

    assert isinstance(res, Response)
    assert res.go_back_count == 1


def test_execute_action(capsys):
    action = ExecuteAction('print("ok")')
    action.process(None)

    assert capsys.readouterr().out == 'ok\n'


def test_execute_action_with_result():
    action = ExecuteAction('2 + 2', True)
    res = action.process(None)

    assert isinstance(res, Message)
    assert res.text == '4'


def test_function_action(function_action):
    action = FunctionAction(function_action)
    res = action.process({'user_id': 123})

    assert isinstance(res, Message)
    assert res.text == 'user 123'
