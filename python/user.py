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

    logging.info('user command: (%s)', ')('.join(request_text), extra=logging_info)

    if len(request_text) == 2:
        info = database.GetUserInfo(request_text[0], request_text[1])
        if info is None or len(info) < 1: info = MESSAGES_USR["empty-result"]
        else: USERS[message.chat.id] = { 'name': request_text[0] }
        
        BOT.send_message(message.chat.id, info, parse_mode='markdown')

    elif len(request_text) == 1:
        if message.chat.id == VARIABLES.ADMIN:
            info = database.GetUserInfoByAdmin(request_text[0])
            if info is None or len(info) < 1: info = MESSAGES_USR["empty-result"]
            BOT.send_message(message.chat.id, info, parse_mode='markdown')
            GetUserInfo()

        else:
            CheckUserName(message, request_text[0])
    
    else:
        output = MESSAGES_USR['get-user-name']
        if message.chat.id in USERS and 'name' in USERS[message.chat.id]:
            output += MESSAGES_USR['default-user'].format(USERS[message.chat.id]['name'])
        BOT.send_message(message.chat.id, output, parse_mode='markdown')
        
        BOT.register_next_step_handler(message, GetUsername)

        info = database.GetUserInfo(USERS[message.chat.id]['name'], request_text[0])
        BOT.send_message(message.chat.id, info, parse_mode='markdown')

def GetUsername(message):
    CheckUserName(message, message.text)

def CheckUserName(message, username):
    user_info_query = USERS[message.chat.id]['user-info']
    user_info_query['username'] = username

    if username is None:
        BOT.send_message(message.chat.id, MESSAGES_USR["invalid-account-name"], parse_mode='markdown')
    else:
        BOT.send_message(message.chat.id, MESSAGES_USR["get-auth"], parse_mode='markdown')
        BOT.register_next_step_handler(message, GetAuthentication)

def GetAuthentication(message):
    user_info_query = USERS[message.chat.id]['user-info']
    GetUserInfo(user_info_query['username'], message.text)
    return

def GetUserInfo(chat_id, username, secret):
    info = database.GetUserInfo(username, secret)
    result = MakeResult(info)

    BOT.send_message(chat_id, result, parse_mode='markdown')
    return

def MakeResult(chat_id, info):
    result = []

    if info is None or len(info) == 0:
        return MESSAGES_USR["empty-result"]
    elif len(info) == 1:
        if chat_id not in USERS: USERS[chat_id] = { 'name': info['username'] }
        else: USERS[chat_id]['name'] = info['username']

    for (username, left_days, left_hours, giga_left) in info:
        account_info = ""

        if left_days is not None and left_days > 0:
            account_info += " and *{} days*".format(left_days)
        if left_hours is not None and (left_hours > 0 or left_days <= 0):
            account_info += " and *{} hours*".format(left_hours)
        if giga_left is not None:
            account_info += " and *{} GB*".format(giga_left)

        if len(account_info) > 0: account_info = "{} remains".format(account_info[5:])
        else: account_info = "*no limit!*"
        
        result.append("{}: {}".format(username, account_info))

    return "\n".join(result)
