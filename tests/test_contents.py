from navmenu.contents import Content


def test_content():
    content = Content('message')
    kwargs = {**content}

    assert 'text' in kwargs
    assert kwargs['text'] == 'message'
