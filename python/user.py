import database
import log
import re
import traceback
import globalvalues as gv

from globalvalues import BOT, MESSAGES, VARIABLES

MESSAGES_USR = None

def Init():
    global MESSAGES_USR
    MESSAGES_USR = MESSAGES["user"]

@BOT.message_handler(commands=["user"])
def GetUserInfo(message):
    try:
        request_text = message.text.split(" ")[1:]

        username = secret = None
        
        if message.chat.id != VARIABLES.ADMIN:
            gv.InitQueryInfo(message.chat.id)

        if len(request_text) > 0:
            username = request_text[0]
            username = checkUserName(message, username)

        if len(request_text) > 1:
            secret = request_text[1]

        userInfoSteps(message, username, secret)

    except Exception:
        log.error('[user]: %s', traceback.format_exc(), **gv.GetLogInfo(message.chat.id))

def userInfoSteps(message, username, secret):
    tries = gv.SafeGet(message.chat.id, 'user-info', 'tries')
    if tries is not None and tries > 3:
        BOT.send_message(message.chat.id, MESSAGES_USR['exit'], parse_mode='markdown')
        return
    else:
        user_info = gv.SafeGet(message.chat.id, 'user-info')
        user_info['tries'] = tries + 1 if tries is not None else 0

    if username is None:
        BOT.send_message(message.chat.id, MESSAGES_USR['get-user-name'], parse_mode='markdown')
        BOT.register_next_step_handler(message, getUsername)
        return

    elif message.chat.id == VARIABLES.ADMIN:
        info = database.GetUserInfoByAdmin(username)

    elif secret is None:
        BOT.send_message(message.chat.id, MESSAGES_USR["get-auth"], parse_mode='markdown')
        BOT.register_next_step_handler(message, getSecret)
        return

    else:
        isphone, secret = checkSecret(secret)
        if isphone: info = database.GetUserInfoByPhone(username, secret)
        else: info = database.GetUserInfoByPassword(username, secret)

    if len(info) == 1 and message.chat.id != VARIABLES.ADMIN:
        gv.AddUser(message.chat.id, info[0][0])
    
    result = MakeResult(message.chat.id, info)

    log.info('[user]: (%s, %s)', username, secret, **gv.GetLogInfo(message.chat.id))

    BOT.send_message(message.chat.id, result, parse_mode='markdown')

def getUsername(message):
    username = checkUserName(message, message.text)
    userInfoSteps(message, username, None)

def checkUserName(message, username):
    if re.search("^\\d+$", username):
        while len(username) < 4: username = "0" + username
        username = "_" + username + "%"
    
    user_info_query = gv.SafeGet(message.chat.id, 'user-info')
    user_info_query['query'] = username

    if username is None:
        BOT.send_message(message.chat.id, MESSAGES_USR["invalid-account-name"], parse_mode='markdown')

    return username

def getSecret(message):
    user_info_query = gv.SafeGet(message.chat.id, 'user-info', 'query')
    userInfoSteps(message, user_info_query, message.text)

def checkSecret(secret):
    isphone = re.search("^\\+?\\d+$", secret)

    if isphone:
        if len(secret) < 5:
            isphone = False
        elif not secret.startswith('+'):
            if secret.startswith('09'):
                secret = "%" + secret[1:]
            else: secret = "%" + secret

    return (isphone, secret)

def MakeResult(chat_id, info):
    result = []

    if info is None or len(info) == 0:
        return MESSAGES_USR["empty-result"]

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
        
        result.append("{}: {}".format(username.replace('_', '\\_'), account_info))

    return "\n".join(result)
