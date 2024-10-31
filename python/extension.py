from globalvalues import BOT, MESSAGES

MESSAGES_EXT = None

def Init():
    global MESSAGES_EXT
    MESSAGES_EXT = MESSAGES["extension"]

@BOT.message_handler(commands=["extension"])
def ExtendUser(message):
    BOT.send_message(message.chat.id, MESSAGES["out-of-service"], parse_mode='markdown')
