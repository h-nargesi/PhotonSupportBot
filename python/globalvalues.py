import telebot
import files

class GlobalVariables:
    ADMIN = -1

TOKEN = files.GetToken()
BOT = telebot.TeleBot(TOKEN)
MESSAGES = files.getMessages()
USERS = dict()
VARIABLES = GlobalVariables()
CONFIGURATION = files.getConfiguration()
