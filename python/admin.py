import database
import logging
import ssh
import globalvalues as gv

from globalvalues import TOKEN, MESSAGES, BOT, VARIABLES

MESSAGES_ADMIN = None
CALLBACK = ["approve", "ignore"]

def Init():
    global MESSAGES_ADMIN
    MESSAGES_ADMIN = MESSAGES["admin"]

@BOT.message_handler(commands=["admin"])
def RegisterAdmin(message):
    request_text = message.text.split(" ")[1:]

    match request_text:
        case "to-mikrotik":
            TransferUsersToMikrotik(message)
            return

    if len(request_text) != 1 or request_text[0] != TOKEN.split(":")[1]:
        BOT.send_message(message.chat.id, MESSAGES_ADMIN["invalid-pass"], parse_mode='markdown')
        return

    VARIABLES.ADMIN = message.chat.id
    BOT.send_message(message.chat.id, MESSAGES_ADMIN["set"], parse_mode='markdown')

def TransferUsersToMikrotik(message):
    logging_info = gv.GetLogInfo(message.chat.id)

    if VARIABLES.ADMIN != message.chat.id:
        logging.warning('approve command: invalid-access for (%s)', ')('.join("to-mikrotik"), extra=logging_info)
        BOT.send_message(message.chat.id, MESSAGES_ADMIN["invalid-access"], parse_mode='markdown')
        return
    
    user_list = database.GetQueryValidUserList()
    command = [f"/ppp secret add name={user[0]} profile=VPN-Profile password={user[1]}" for user in user_list]
    command = "/ppp secret remove [find]" + "\n".join(command)
    ssh.ExecuteSshAllServers(command)

    BOT.send_message(message.chat.id, MESSAGES_ADMIN["transfer-done"], parse_mode='markdown')
