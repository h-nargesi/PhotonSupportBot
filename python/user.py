import database

from globalvalues import BOT, MESSAGES, USERS

MESSAGES_USR = None

def Init():
    global MESSAGES_USR
    MESSAGES_USR = MESSAGES["user"]

@BOT.message_handler(commands=["user"])
def GetUserInfo(message):
    request_text = message.text.split(" ")[1:]
    messages = MESSAGES["user"]

    if (len(request_text) == 2):
        info = database.GetUserInfo(request_text[0], request_text[1])
        if info is None or len(info) < 1: info = messages["empty-result"]
        else: USERS[message.chat.id] = { 'name': request_text[0] }
        
        BOT.send_message(message.chat.id, info, parse_mode='markdown')

    elif (len(request_text) == 1):
        if message.chat.id not in USERS:
            BOT.send_message(message.chat.id, messages["user-not-set"], parse_mode='markdown')
        else:
            info = database.GetUserInfo(USERS[message.chat.id]['name'], request_text[0])
            BOT.send_message(message.chat.id, info)
    
    else: BOT.send_message(message.chat.id, messages["empty-request"], parse_mode='markdown')
