import time
from dotenv import dotenv_values
import requests
import random


# bot_key = '7812745946:AAFZdNV7oGZd4C2b9aozVRh9dJcY66c2dvM'
#
# url = f"https://api.telegram.org/bot{bot_key}/"  # don't forget to change the token!
#
class SingletonBot(type):
    __instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instance:
            instance = super().__call__(*args, **kwargs)
            cls.__instance[cls] = instance
        return cls.__instance[cls]


class Bot(metaclass=SingletonBot):
    def __init__(self, some_number):
        self.some_number = some_number
        config = dotenv_values(".env")
        self.bot_key = config.get('TOKEN')
        self.url = f"https://api.telegram.org/bot{self.bot_key}/"  # don't forget to change the token!

    def last_update(self, request):
        response = requests.get(request + 'getUpdates')
        print(response)
        response = response.json()
        print(response)
        results = response['result']
        total_updates = len(results) - 1
        return results[total_updates]

    def get_chat_id(self, update):
        chat_id = update['message']['chat']['id']
        return chat_id

    def get_message_text(self, update):
        message_text = update['message']['text']
        return message_text

    def send_message(self, chat, text):
        params = {'chat_id': chat, 'text': text}
        response = requests.post(self.url + 'sendMessage', data=params)
        return response

    def main(self):
        update_id = self.last_update(self.url)['update_id']
        while True:
            time.sleep(3)
            update = self.last_update(self.url)
            if update_id == update['update_id']:
                if self.get_message_text(update).lower() == 'hi' or self.get_message_text(
                        update).lower() == 'hello' or self.get_message_text(update).lower() == 'hey':
                    self.send_message(self.get_chat_id(update), 'Greetings! Type "Dice" to roll the dice!')
                elif self.get_message_text(update).lower() == 'qa24':
                    self.send_message(self.get_chat_id(update), 'Python')
                elif self.get_message_text(update).lower() == 'python':
                    self.send_message(self.get_chat_id(update), 'version 3.10')
                elif self.get_message_text(update).lower() == 'dice':
                    _1 = random.randint(1, 6)
                    _2 = random.randint(1, 6)
                    self.send_message(self.get_chat_id(update),
                                      'You have ' + str(_1) + ' and ' + str(_2) + '!\nYour result is ' + str(
                                          _1 + _2) + '!')
                else:
                    self.send_message(self.get_chat_id(update), 'Sorry, I don\'t understand you :(')
                update_id += 1


# if __name__ == '__main__':
#     main()

bender = Bot(3)
print(bender.bot_key)
print(bender.some_number)
# bender.main()

chappy = Bot(5)
print(chappy.bot_key)
print(chappy.some_number)
# chappy.main()
