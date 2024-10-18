import log
import user
import extension
import approvement
import notification
import globalvalues as gv

from globalvalues import BOT, MESSAGES

log.Init()
user.Init()
extension.Init()
approvement.Init()
notification.Init()

@BOT.message_handler(commands=["start"])
def StartMessage(message):
    log.info('[start]', **gv.GetLogInfo(message.chat.id))
    BOT.send_message(message.chat.id, "\n".join(MESSAGES["welcome"]), parse_mode='markdown')

@BOT.message_handler(commands=["price"])
def PrintPrice(message):
    log.info('[price]', **gv.GetLogInfo(message.chat.id))
    BOT.send_message(message.chat.id, "\n".join(MESSAGES["price"]), parse_mode='markdown')

notification.StartService()

BOT.infinity_polling(timeout=10, long_polling_timeout = 5)
