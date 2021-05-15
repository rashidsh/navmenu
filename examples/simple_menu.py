from navmenu import MenuManager
from navmenu.actions import MessageAction, SubmenuAction, GoBackAction, ExecuteAction, FunctionAction
from navmenu.contents import Content
from navmenu.item_contents import TextItemContent
from navmenu.items import Item, LineBreakItem
from navmenu.menus import Menu
from navmenu.state import MemoryStateHandler
from navmenu.responses import Message, Response


def go_back_func(msg):
    return Response(Message('Going back...'), go_back_count=1)


main_menu = Menu(Content('Main menu'), (
    Item('print', TextItemContent('print text'), MessageAction('Text message')),
    LineBreakItem(),
    Item('open', TextItemContent('open submenu'), SubmenuAction('submenu')),
    LineBreakItem(),
    Item('quit', TextItemContent('quit the program'), ExecuteAction('import sys; sys.exit()')),
), default_action=MessageAction('Please type "print" or "open" to navigate'))

submenu = Menu(Content('Submenu'), (
    Item('calc', TextItemContent('calculate 2 + 2'), ExecuteAction('f"2 + 2 = {2 + 2}"', return_text=True)),
    Item('func', TextItemContent('run function'), FunctionAction(go_back_func)),
    LineBreakItem(),
    Item('back', TextItemContent('go back'), GoBackAction()),
))

menu_manager = MenuManager({
    'main_menu': main_menu,
    'submenu': submenu,
}, MemoryStateHandler('main_menu'))


def main():
    while True:
        message = menu_manager.get_message()

        if message:
            actions = ''
            for line in message.keyboard.lines:
                actions += ' | '.join(f"{i.payload}: {i.text}" for i in line) + '\n'

            separator = '-' * 20

            print(f"{separator}\n{message.text}\n{separator}\n{actions}{separator}")

        text = input('Command: ')

        try:
            messages = menu_manager.select(text)

        except ValueError:
            print('Invalid command')

        else:
            for message in messages:
                print(message.text)


if __name__ == '__main__':
    main()
