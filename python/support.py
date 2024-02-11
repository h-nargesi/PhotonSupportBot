import telebot
import database
import files

TOKEN = files.GetToken()
MESSAGES = files.getMessages()

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, MESSAGES["welcome"], parse_mode='markdown')

@bot.message_handler(commands=["user"])
def echo_message(message):
    request_text = message.text.split(" ")[1:]
    messages = MESSAGES["user"];

    if (len(request_text) == 2):
        info = database.GetUSerInfoByPassword(request_text[0], request_text[1])
        if info is None or len(info) < 1: info = messages["empty-result"]
        bot.send_message(message.chat.id, info, parse_mode='markdown')

    # elif (len(request_text) == 1):
    #     info = database.GetUserInfoByPhone(request_text[0], "")
    #     print(message.entities[0])
    #     bot.send_message(message.chat.id, info)
    
    else: bot.send_message(message.chat.id, messages["empty-request"], parse_mode='markdown')

bot.polling()
