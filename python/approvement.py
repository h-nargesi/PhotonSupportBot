import database
import log
import globalvalues as gv

from globalvalues import TOKEN, BOT, MESSAGES, USERS, VARIABLES

MESSAGES_APV = None
CALLBACK = ["approve", "ignore"]

def Init():
    global MESSAGES_APV
    MESSAGES_APV = MESSAGES["admin"]

@BOT.message_handler(commands=["approve"])
def PaymentApprovement(message):
    logging_info = gv.GetLogInfo(message.chat.id)

    if VARIABLES.ADMIN != message.chat.id:
        log.warning('[approve]: invalid-access for (%s)', ')('.join(request_text), **logging_info)
        BOT.send_message(message.chat.id, MESSAGES_APV["invalid-access"], parse_mode='markdown')
        return

    request_text = message.text.split(" ")[1:]
    log.info('[approve]: (%s)', ')('.join(request_text), **logging_info)

    if len(request_text) < 1: return

    if request_text[0] == 'list':
        list = []
        for value in USERS.values():
            if 'payment' in value:
                list.append("*{user}*:\n/approve {chat_id}\n{info}".format_map(value['payment']))
        result = "\n\n".join(list)
        if result is None or len(result) < 1: result = MESSAGES_APV["empty-list"]
        BOT.send_message(message.chat.id, result, parse_mode='markdown')
        return
    
    if not request_text[0].isnumeric():
        BOT.send_message(message.chat.id, MESSAGES_APV["invalid-chat-id"], parse_mode='markdown')
        return
    
    approvePayment(request_text[0])
    
@BOT.callback_query_handler(func=lambda call: call.data.startwith("approve"))
def callbackQueryHandler(call):
    approvePayment(call.data.split(".")[1])
    return

@BOT.message_handler(commands=["admin"])
def RegisterAdmin(message):
    request_text = message.text.split(" ")[1:]
    logging_info = gv.GetLogInfo(message.chat.id)

    if len(request_text) != 1 or request_text[0] != TOKEN.split(":")[1]:
        log.critical('[admin]: unsucessfull try to set admin', **logging_info)
        BOT.send_message(message.chat.id, MESSAGES_APV["invalid-pass"], parse_mode='markdown')
        return

    VARIABLES.ADMIN = message.chat.id
    log.info('[admin]: has been set', **logging_info)
    BOT.send_message(message.chat.id, MESSAGES_APV["set"], parse_mode='markdown')

def approvePayment(user_id):
    user_id = int(user_id)

    if user_id not in USERS or 'payment' not in USERS[user_id]:
        BOT.send_message(VARIABLES.ADMIN, MESSAGES_APV["invalid-user"], parse_mode='markdown')
        return

    payment = USERS[user_id].pop('payment')
    database.ExtendUser(payment['user'])

    BOT.send_message(user_id, MESSAGES_APV["approved"], parse_mode='markdown')
    BOT.send_message(VARIABLES.ADMIN, MESSAGES_APV["approved"], parse_mode='markdown')
