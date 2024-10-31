import log
import globalvalues as gv

from globalvalues import TOKEN, BOT, MESSAGES, VARIABLES

MESSAGES_APV = None
CALLBACK = ["approve", "ignore"]

def Init():
    global MESSAGES_APV
    MESSAGES_APV = MESSAGES["admin"]

@BOT.message_handler(commands=["approve"])
def PaymentApprovement(message):
    BOT.send_message(message.chat.id, MESSAGES["out-of-service"], parse_mode='markdown')

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
