import user
import extension
import approvement

from globalvalues import BOT, MESSAGES

user.Init()
extension.Init()
approvement.Init()

@BOT.message_handler(commands=["start"])
def start_message(message):
    BOT.send_message(message.chat.id, "\n".join(MESSAGES["welcome"]), parse_mode='markdown')

BOT.polling()
