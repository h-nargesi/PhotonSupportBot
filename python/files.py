import json
import os
import logging
import datetime
import shutil

TOKEN = "token.txt"
MESSAGES = "messages.json"
CONFIGURATION = "configuration.json"
DATABASE = "database.json"
QUERY_USER_INFO = "user-info.sql"
QUERY_TOPUP_INFO = "topup-info.sql"

def GetToken():
    token = GetTextFile(TOKEN)
    token = token.replace('\r', '')
    token = token.replace('\n', '')
    return token

def getMessages():
    copyFromTemp(MESSAGES)
    return GetJsonFile(MESSAGES)

def getConfiguration():
    copyFromTemp(CONFIGURATION)
    return GetJsonFile(CONFIGURATION)

def getDatabaseInfo():
    return GetJsonFile(DATABASE)

def GetQueryUserInfo():
    return GetTextFile(QUERY_USER_INFO)

def GetQueryTopupInfo():
    return GetTextFile(QUERY_TOPUP_INFO)

def GetTextFile(file_name):
    file_name = GetFilePath(file_name)
    with open(file_name, "r", encoding="utf-8") as content_file:
        content = content_file.read()
    return content

def GetJsonFile(file_name):
    file_name = GetFilePath(file_name)
    with open(file_name, "r", encoding="utf-8") as content_file:
        content = json.load(content_file)
    return content

def GetFilePath(file_name):
    return os.path.realpath(os.path.join(os.path.dirname(__file__), "settings", file_name))

def InitLogging():
    directory = os.path.realpath(os.path.join(os.path.dirname(__file__), "logs"))
    if not os.path.exists(directory): os.makedirs(directory)
    path = os.path.realpath(os.path.join(directory, '{:%Y-%m-%d}.log'.format(datetime.datetime.now())))

    file_handler = logging.FileHandler(path)
    format = '%(asctime)s | %(levelname)-8s | %(userid)-10s | %(username)s | %(message)s'
    logging.basicConfig(encoding='utf-8', format=format, handlers=[file_handler], level=logging.INFO)

def copyFromTemp(file_name):
    if file_name is None: return

    parts = file_name.split('.')
    parts[0] += "-template"
    temp_name = ".".join(parts)
    
    file_path = GetFilePath(file_name)
    temp_path = GetFilePath(temp_name)

    if not os.path.exists(file_path) and os.path.exists(temp_path):
        shutil.copyfile(temp_path, file_path)
