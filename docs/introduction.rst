Introduction
============

navmenu is a library to create multilevel menus for chatbots.

Installation
------------

navmenu can be installed with pip::

    pip3 install navmenu

Quickstart
----------

First, import everything you will need::

    from navmenu import MenuManager
    from navmenu.actions import MessageAction, SubmenuAction, GoBackAction
    from navmenu.contents import Content
    from navmenu.io import ConsoleIO
    from navmenu.item_contents import TextItemContent
    from navmenu.items import Item
    from navmenu.menus import Menu
    from navmenu.state import MemoryStateHandler

Then, create a menu with one item::

    menu = Menu(Content('Welcome!'), [
        Item('print', TextItemContent('print text'), MessageAction('Text message'))
    ])

``'print'`` is the internal menu item name. It can be any string but **must be unique within menu**.

Also, you can add items to menus later::

    new_item = Item('hello', TextItemContent('say hello'), MessageAction('Hello!'))
    menu.add_item(new_item)

Every menu should be wrapped in a :class:`~navmenu.menu_manager.MenuManager`::

    menu_manager = MenuManager({
        'main_menu': menu
    }, MemoryStateHandler('main_menu'))

``MemoryStateHandler('main_menu')`` means that the user state will be saved in memory. It will not persist between app restarts. ``'main_menu'`` is the name of the first menu to show.

Finally, show the menu to a user::

    io = ConsoleIO(menu_manager)
    io.start_loop()

Adding a submenu
----------------

To add a submenu, define it like the first menu::

    submenu = Menu(Content('Submenu'), [
        Item('back', TextItemContent('go back'), GoBackAction())
    ])

Then, add this submenu to the menu manager::

    menu_manager = MenuManager({
        'main_menu': menu,
        'submenu': submenu
    }, MemoryStateHandler('main_menu'))

Finally, add an item to the main menu that will open the submenu::

    menu = Menu(Content('Welcome!'), [
        Item('print', TextItemContent('print text'), MessageAction('Text message')),
        Item('open', TextItemContent('open submenu'), SubmenuAction('submenu'))
    ])

