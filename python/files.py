import json
import os
import logging
import datetime

TOKEN = "token.txt"
MESSAGES = "messages.json"
CONFIGURATION = "configuration.json"
DATABASE = "database.json"
QUERY_USER_INFO = "user-info.sql"

def GetToken():
    return GetTextFile(TOKEN)

def getMessages():
    return GetJsonFile(MESSAGES)

def getConfiguration():
    return GetJsonFile(CONFIGURATION)

def getDatabaseInfo():
    return GetJsonFile(DATABASE)

def GetQueryUserInfo():
    return GetTextFile(QUERY_USER_INFO)

def GetTextFile(file_name):
    file_name = GetFilePath(file_name)
    with open(file_name, "r") as content_file:
        content = content_file.read()
    return content

def GetJsonFile(file_name):
    file_name = GetFilePath(file_name)
    with open(file_name, "r") as content_file:
        content = json.load(content_file)
    return content

def GetFilePath(file_name):
    return os.path.realpath(os.path.join(os.getcwd(), "settings", file_name))

def InitLogging():
    directory = os.path.realpath(os.path.join(os.getcwd(), "logs"))
    if not os.path.exists(directory): os.makedirs(directory)
    path = os.path.realpath(os.path.join(directory, '{:%Y-%m-%d}.log'.format(datetime.datetime.now())))

    file_handler = logging.FileHandler(path)
    format = '%(asctime)s | %(levelname)-8s | %(userid)-10s | %(username)s | %(message)s'
    logging.basicConfig(encoding='utf-8', format=format, handlers=[file_handler], level=logging.INFO)
