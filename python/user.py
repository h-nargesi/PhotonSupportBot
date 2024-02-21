import database
import logging

from globalvalues import BOT, MESSAGES, USERS, VARIABLES

MESSAGES_USR = None

def Init():
    global MESSAGES_USR
    MESSAGES_USR = MESSAGES["user"]

@BOT.message_handler(commands=["user"])
def GetUserInfo(message):
    logging_info = { 'userid': message.chat.id }
    request_text = message.text.split(" ")[1:]
    messages = MESSAGES["user"]

    logging.info('user command: (%s)', ')('.join(request_text), extra=logging_info)

    if len(request_text) == 2:
        info = database.GetUserInfo(request_text[0], request_text[1])
        if info is None or len(info) < 1: info = messages["empty-result"]
        else: USERS[message.chat.id] = { 'name': request_text[0] }
        
        BOT.send_message(message.chat.id, info, parse_mode='markdown')

    elif len(request_text) == 1:
        if message.chat.id == VARIABLES.ADMIN:
            info = database.GetUserInfoByAdmin(request_text[0])
            if info is None or len(info) < 1: info = messages["empty-result"]
            BOT.send_message(message.chat.id, info, parse_mode='markdown')

        elif message.chat.id not in USERS:
            BOT.send_message(message.chat.id, messages["user-not-set"], parse_mode='markdown')

        else:
            info = database.GetUserInfo(USERS[message.chat.id]['name'], request_text[0])
            BOT.send_message(message.chat.id, info, parse_mode='markdown')
    
    else: BOT.send_message(message.chat.id, messages["empty-request"], parse_mode='markdown')
