import json
import telebot

from navmenu import MenuManager
from navmenu.contents import Content
from navmenu.deserializer import deserialize
from navmenu.io import TelegramIO
from navmenu.responses import Message, Response
from navmenu.state import MemoryStateHandler

TOKEN = 'abc123'


def go_back_func(msg):
    return Response(Message(Content('Going back...')), go_back_count=1)


def reply(message, text, keyboard):
    bot.send_message(message.chat.id, text, reply_markup=keyboard)


def handle_messages(messages):
    for message in messages:
        res = io.process(message.from_user.id, message.text, {})
        for res_message in res:
            reply(message, res_message.text, res_message.keyboard)


def callback_query(call):
    res = io.process(call.from_user.id, None, json.loads(call.data))
    bot.answer_callback_query(call.id)
    for res_message in res:
        reply(call.message, res_message.text, res_message.keyboard)


def main():
    global bot, io

    with open('example_menu.json') as f:
        menus = deserialize(json.load(f), __import__(__name__))

    menu_manager = MenuManager(menus, MemoryStateHandler('main_menu'))
    io = TelegramIO(menu_manager)

    bot = telebot.TeleBot(TOKEN)
    bot.set_update_listener(handle_messages)
    bot.add_callback_query_handler({'function': callback_query, 'filters': {}})

    print('Bot started')

    bot.polling()


if __name__ == '__main__':
    main()
