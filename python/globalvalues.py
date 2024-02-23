import telebot
import files

class GlobalVariables:
    ADMIN = -1

TOKEN = files.GetToken()
BOT = telebot.TeleBot(TOKEN)
MESSAGES = files.getMessages()
USERS = dict()
VARIABLES = GlobalVariables()
CONFIGURATION = files.getConfiguration()

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

    return __SafeGet(USERS[chat_id], keys)

def __SafeGet(cache, keys):

    key = keys.pop(0)
    if key not in cache: return None

    cache = cache[key]
    if len(keys) < 1: return cache
    else: return __SafeGet(cache, keys)

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