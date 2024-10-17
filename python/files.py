import json
import os
import shutil

TOKEN = "token.txt"
MESSAGES = "messages.json"
CONFIGURATION = "configuration.json"
DATABASE = "database.json"
QUERY_USER_INFO = "user-info.sql"

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

def GetTextFile(file_name):
    file_name = GetFilePathSettings(file_name)
    with open(file_name, "r", encoding="utf-8") as content_file:
        content = content_file.read()
    return content

def GetJsonFile(file_name):
    file_name = GetFilePathSettings(file_name)
    with open(file_name, "r", encoding="utf-8") as content_file:
        content = json.load(content_file)
    return content

def GetFilePathSettings(file_name):
    return GetFilePath('settings', file_name)

def GetFilePath(*path):
    return os.path.realpath(os.path.join(os.path.dirname(__file__), *path))

def copyFromTemp(file_name):
    if file_name is None: return

    parts = file_name.split('.')
    parts[0] += "-template"
    temp_name = ".".join(parts)
    
    file_path = GetFilePathSettings(file_name)
    temp_path = GetFilePathSettings(temp_name)

    if not os.path.exists(file_path) and os.path.exists(temp_path):
        shutil.copyfile(temp_path, file_path)
