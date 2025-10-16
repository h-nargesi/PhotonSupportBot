import telebot
import files
from telebot import apihelper

class GlobalVariables:
    ADMIN = -1

TOKEN = files.GetToken()
CONFIGURATION = files.getConfiguration()
MESSAGES = files.getMessages()
USERS = dict()
VARIABLES = GlobalVariables()

BOT = telebot.TeleBot(TOKEN)
if 'proxy' in CONFIGURATION.keys() and CONFIGURATION['proxy'] is not None:
    apihelper.proxy = {
        'http': CONFIGURATION['proxy'],
        'https': CONFIGURATION['proxy']
    }

# USER
# {
#     name: string,
#     payment: {
#         chat_id: int,
#         user: string,
#         info: string,
#     },
#     user-info: {
#         query: string,
#         tries: int,
#     }
# }

def SafeGet(chat_id, keys):
    if chat_id not in USERS or len(keys) == 0:
        return None

    return safeGet(USERS[chat_id], keys)

def safeGet(cache, keys):

    key = keys.pop(0)
    if key not in cache: return None

    cache = cache[key]
    if len(keys) < 1: return cache
    else: return safeGet(cache, keys)

def AddUser(chat_id, username):
    if chat_id not in USERS:
        USERS[chat_id] = dict()
    
    if username is not None:
        USERS[chat_id]['name'] = username

def InitQueryInfo(chat_id):
    AddUser(chat_id, None)

    if 'user-info' not in USERS[chat_id]:
        USERS[chat_id]['user-info'] = dict()
    
    USERS[chat_id]['user-info']['tries'] = 0

def GetLogInfo(chat_id):
    username = 'ADMIN' if chat_id == VARIABLES.ADMIN else SafeGet(chat_id, ['name'])
    return { 'userid': chat_id, 'username': username }