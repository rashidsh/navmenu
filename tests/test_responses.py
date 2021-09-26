from navmenu.responses import Message


def test_message_with_payload():
    message = Message('message {user_id}', payload={'user_id': 123})

    assert message.get_text() == 'message 123'
