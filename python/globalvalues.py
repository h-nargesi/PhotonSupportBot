import telebot
import files
from telebot import apihelper

class GlobalVariables:
    ADMIN = -2

class UserCache:
    # USER
    # [username: string] = {
    #     name: string,
    #     chat-id: int,
    #     payment: {
    #         user: string,
    #         info: string,
    #     },
    #     user-info: {
    #         alert-admin: datetime,
    #         alert-user: datetime,
    #     }
    # }
    USERS = dict()

    # CHAT
    # [chat-id: int] = {
    #     chat-id: int,
    #     latest-user-name: string,
    #     chat-info: {
    #         query: string,
    #         tries: int,
    #     }
    #     users: [username: string] = User
    # }
    CHATS = dict()

    def getUser(self, username, *keys):
        if username is None: return None
        elif username not in self.USERS:
            self.set(username, None)

        if len(keys) == 0: return self.USERS[username]
        else: return UserCache.__get_safe(self.USERS[username], list(keys))

    def getChat(self, chat_id, *keys):
        if chat_id is None: return None
        elif chat_id not in self.CHATS:
            self.set(None, chat_id)

        if len(keys) == 0: return self.CHATS[chat_id]
        else: return UserCache.__get_safe(self.CHATS[chat_id], list(keys))

    def set(self, username, chat_id, save=True):
        if username is not None:
            if username not in self.USERS:
                self.USERS[username] = { 'name': username, 'chat-id': chat_id }
            elif chat_id is not None:
                self.USERS[username]['chat-id'] = chat_id

        if chat_id is not None:
            if chat_id not in self.CHATS:
                self.CHATS[chat_id] = {
                    'chat-id': chat_id,
                    'users': dict()
                }
            if username is not None:
                self.CHATS[chat_id]['latest-user-name'] = username
                self.CHATS[chat_id]['users'][username] = self.USERS[username]

        if save: files.SaveData('users', { 'users': self.USERS, 'chats': self.CHATS })

    def initPayment(self, username, chat_id):
        self.set(username, chat_id)
        if 'payment' not in self.USERS[username]:
            self.USERS[username]['payment'] = dict()

        self.USERS[username]['payment']['user'] = username

        files.SaveData('users', { 'users': self.USERS, 'chats': self.CHATS })

    def initQueryInfo(self, chat_id):
        self.set(None, chat_id)
        if 'chat-info' not in self.CHATS[chat_id]:
            self.CHATS[chat_id]['chat-info'] = dict()

        self.CHATS[chat_id]['chat-info']['tries'] = 0

        files.SaveData('users', { 'users': self.USERS, 'chats': self.CHATS })

    def alertSent(self, username, chat_id, time, type):
        self.set(username, chat_id)
        if 'user-info' not in self.USERS[username]:
            self.USERS[username]['user-info'] = dict()

        self.USERS[username]['user-info'][type] = time

        files.SaveData('users', { 'users': self.USERS, 'chats': self.CHATS })

    def __get_safe(cache, keys):
        key = keys.pop(0)
        if key not in cache: return None

        cache = cache[key]
        if cache is None or len(keys) < 1: return cache
        else: return UserCache.__get_safe(cache, keys)

TOKEN = files.GetToken()
BOT = telebot.TeleBot(TOKEN)
MESSAGES = files.GetMessages()
VARIABLES = GlobalVariables()
CONFIGURATION = files.GetConfiguration()
USERS = UserCache()

if 'proxy' in CONFIGURATION.keys() and CONFIGURATION['proxy'] is not None:
    apihelper.proxy = {
        'http': CONFIGURATION['proxy'],
        'https': CONFIGURATION['proxy']
    }

def GetLogInfo(chat_id):
    username = 'ADMIN' if chat_id == VARIABLES.ADMIN else USERS.getChat(chat_id, 'latest-user-name')
    return { 'userid': chat_id, 'username': username }
