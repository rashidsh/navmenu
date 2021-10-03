import json
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from vk_api.utils import get_random_id

from navmenu import MenuManager
from navmenu.contents import Content
from navmenu.deserializer import deserialize
from navmenu.io import VKIO
from navmenu.responses import Message, Response
from navmenu.state import MemoryStateHandler


TOKEN = 'abc123'
GROUP_ID = 123


def go_back_func(msg):
    return Response(Message(Content('Going back...')), go_back_count=1)


def send(peer_id, text, keyboard):
    vk.method('messages.send', {
        'peer_id': peer_id, 'message': text, 'keyboard': keyboard, 'random_id': get_random_id(),
    })


def main():
    global vk

    with open('example_menu.json') as f:
        menus = deserialize(json.load(f), __import__(__name__))

    menu_manager = MenuManager(menus, MemoryStateHandler('main_menu'))
    io = VKIO(menu_manager)

    vk = VkApi(token=TOKEN)
    lp = VkBotLongPoll(vk, GROUP_ID)

    print('Bot started')

    while True:
        for event in lp.check():
            if event.type == VkBotEventType.MESSAGE_NEW:
                msg = event.raw['object']['message']

                payload = json.loads(msg['payload']) if 'payload' in msg else {}

                res = io.process(msg['from_id'], msg['text'], payload)
                for message in res:
                    send(msg['peer_id'], message.text, message.keyboard)


if __name__ == '__main__':
    main()
