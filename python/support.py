import log
import user
import extension
import approvement
import globalvalues as gv

from globalvalues import BOT, MESSAGES

log.Init()
user.Init()
extension.Init()
approvement.Init()

@BOT.message_handler(commands=["start"])
def StartMessage(message):
    log.info('[start]', extra=gv.GetLogInfo(message.chat.id))
    BOT.send_message(message.chat.id, "\n".join(MESSAGES["welcome"]), parse_mode='markdown')

@BOT.message_handler(commands=["price"])
def PrintPrice(message):
    log.info('[price]', extra=gv.GetLogInfo(message.chat.id))
    BOT.send_message(message.chat.id, "\n".join(MESSAGES["price"]), parse_mode='markdown')

BOT.infinity_polling(timeout=10, long_polling_timeout = 5)