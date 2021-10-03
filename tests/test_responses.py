from navmenu.contents import Content
from navmenu.responses import Message


def test_message_with_payload():
    message = Message(Content(text='message {user_id}'), payload={'user_id': 123})

    assert message.get_content().get('text') == 'message 123'
