from navmenu.keyboard import ButtonColors
from navmenu.item_contents import TextItemContent


def test_text_item_content():
    item_content = TextItemContent('text', ButtonColors.PRIMARY)
    res = item_content.get_content('payload')

    assert res['text'] == 'text'
    assert res['color'] == ButtonColors.PRIMARY
    assert res['payload'] == 'payload'
