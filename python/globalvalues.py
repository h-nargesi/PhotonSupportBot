import telebot
import files

class GlobalVariables:
    ADMIN = -2

TOKEN = files.GetToken()
BOT = telebot.TeleBot(TOKEN)
MESSAGES = files.GetMessages()
USERS = dict()
USERS_BY_NAME = dict()
VARIABLES = GlobalVariables()
CONFIGURATION = files.GetConfiguration()

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
#         alert-admin: datetime,
#         alert-user: datetime,
#     }
# }

def SafeGet(chat_id, *keys):
    if chat_id not in USERS or len(keys) == 0:
        return None

    return safeGet(USERS[chat_id], list(keys))

def safeGet(cache, keys):

    key = keys.pop(0)
    if key not in cache: return None

    cache = cache[key]
    if cache is None or len(keys) < 1: return cache
    else: return safeGet(cache, keys)

def GetUserByName(username):
    chat_id = USERS_BY_NAME[username] if username in USERS_BY_NAME else -1

    if chat_id not in USERS or USERS[chat_id]['name'] != username:
        chat_id = -1
        for id in USERS:
            if USERS[id]['name'] == username:
                USERS_BY_NAME[username] = id
                files.SaveData('users-by-name', USERS_BY_NAME)
                chat_id = id
                break

    return int(chat_id)

def AddUser(chat_id, username, save=True):
    if chat_id < 0: return 

    if chat_id not in USERS:
        USERS[chat_id] = { 'name': username }
    
    elif username is not None:
        USERS[chat_id]['name'] = username

    if save: files.SaveData('users', USERS)

def InitPayment(chat_id, username):
    AddUser(chat_id, None, False)

    if 'payment' not in USERS[chat_id]:
        USERS[chat_id]['payment'] = dict()

    USERS[chat_id]['payment']['username'] = username
    files.SaveData('users', USERS)
    
def InitQueryInfo(chat_id):
    AddUser(chat_id, None, False)

    if 'user-info' not in USERS[chat_id]:
        USERS[chat_id]['user-info'] = dict()
    
    USERS[chat_id]['user-info']['tries'] = 0
    files.SaveData('users', USERS)

def AlertSent(chat_id, time, type):
    AddUser(chat_id, None, False)

    if 'user-info' not in USERS[chat_id]:
        USERS[chat_id]['user-info'] = dict()
    
    USERS[chat_id]['user-info']['alert-' + type] = time
    files.SaveData('users', USERS)

def GetLogInfo(chat_id):
    username = 'ADMIN' if chat_id == VARIABLES.ADMIN else SafeGet(chat_id, 'name')
    return { 'userid': chat_id, 'username': username }
