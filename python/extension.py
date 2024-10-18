from telebot import types
from globalvalues import BOT, MESSAGES, USERS, VARIABLES

MESSAGES_EXT = None

def Init():
    global MESSAGES_EXT
    MESSAGES_EXT = MESSAGES["extension"]

@BOT.message_handler(commands=["extension"])
def ExtendUser(message):
    BOT.send_message(message.chat.id, MESSAGES["out-of-service"], parse_mode='markdown')

    # logging_info = { 'userid': message.chat.id }
    # request_text = message.text.split(" ")[1:]
    
    # logging.info('extension command: (%s)', ')('.join(request_text), extra=logging_info)

    # if VARIABLES.ADMIN < 0:
    #     BOT.send_message(message.chat.id, MESSAGES["global-error"], parse_mode='markdown')
    #     return
    
    # if len(request_text) == 0:
    #     output = MESSAGES_EXT['get-user-name']
    #     if message.chat.id in USERS and 'name' in USERS[message.chat.id]:
    #         output += MESSAGES_EXT['default-user'].format(USERS[message.chat.id]['name'])
    #     BOT.send_message(message.chat.id, output, parse_mode='markdown')
        
    #     BOT.register_next_step_handler(message, getUsername)

    # elif len(request_text) == 1:
    #     message.text = request_text[0]
    #     getUsername(message)
    
    # else:
    #     BOT.send_message(message.chat.id, MESSAGES["invlid-request"], parse_mode='markdown')

def getUsername(message):
    username = message.text if message.text != '.' else USERS[message.chat.id]['name']
    
    if message.chat.id in USERS:
        USERS[message.chat.id]['payment'] = { 'user': username }
    else:
        USERS[message.chat.id] = { 'payment': { 'user': username } }

    BOT.send_message(message.chat.id, MESSAGES_EXT["get-payment-pic"], parse_mode='markdown')
    BOT.register_next_step_handler(message, getPaymentInfo)

def getPaymentInfo(message):
    payment = USERS[message.chat.id]['payment']
    payment['info'] = message.text
    payment['chat_id'] = message.chat.id
    BOT.send_message(message.chat.id, MESSAGES_EXT["wait-for-approvement"], parse_mode='markdown')
    
    notification = "{chat_id}: *{user}*\n{info}".format_map(payment)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text=MESSAGES_EXT["request-btn"], callback_data="approve.{}".format(message.chat.id)))
    
    BOT.send_message(VARIABLES.ADMIN, notification, parse_mode='markdown', reply_markup=keyboard)

