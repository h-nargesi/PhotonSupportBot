import user
import extension
import approvement
import files
import logging

from globalvalues import BOT, MESSAGES

files.InitLogging()
user.Init()
extension.Init()
approvement.Init()

@BOT.message_handler(commands=["start"])
def start_message(message):
    logging.info('start command', extra={ 'userid': message.chat.id })
    BOT.send_message(message.chat.id, "\n".join(MESSAGES["welcome"]), parse_mode='markdown')

@BOT.message_handler(commands=["price"])
def start_message(message):
    logging.info('bank command', extra={ 'userid': message.chat.id })
    BOT.send_message(message.chat.id, "\n".join(MESSAGES["price"]), parse_mode='markdown')

BOT.polling()
