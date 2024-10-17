import user
import extension
import approvement
import files
import logging
import notification
import globalvalues as gv

from globalvalues import BOT, MESSAGES

files.InitLogging()
user.Init()
extension.Init()
approvement.Init()
notification.Init()

@BOT.message_handler(commands=["start"])
def start_message(message):
    logging.info('start command', extra=gv.GetLogInfo(message.chat.id))
    BOT.send_message(message.chat.id, "\n".join(MESSAGES["welcome"]), parse_mode='markdown')

@BOT.message_handler(commands=["price"])
def start_message(message):
    logging.info('price command', extra=gv.GetLogInfo(message.chat.id))
    BOT.send_message(message.chat.id, "\n".join(MESSAGES["price"]), parse_mode='markdown')

BOT.infinity_polling(timeout=10, long_polling_timeout = 5)

notification.StartService()
