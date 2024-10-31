import json
import os
import shutil

TOKEN = "token.txt"
MESSAGES = "messages.json"
CONFIGURATION = "configuration.json"
DATABASE = "database.json"
QUERY_USER_INFO = "user-info.sql"
QUERY_TOPUP_INFO = "topup-info.sql"

def GetToken():
    token = getTextFile('settings', TOKEN)
    token = token.replace('\r', '')
    token = token.replace('\n', '')
    return token

def GetFilePath(*path):
    return os.path.realpath(os.path.join(os.path.dirname(__file__), *path))

def GetMessages():
    copyFromTemp('settings', MESSAGES)
    return getJsonFile('settings', MESSAGES)

def GetConfiguration():
    copyFromTemp('settings', CONFIGURATION)
    return getJsonFile('settings', CONFIGURATION)

def GetDatabaseInfo():
    return getJsonFile('settings', DATABASE)

def GetQueryUserInfo():
    return getTextFile('settings', QUERY_USER_INFO)

def GetQueryTopupInfo():
    return getTextFile('settings', QUERY_TOPUP_INFO)

def LoadData(title):
    if not os.path.exists(GetFilePath('data', title + '.json')): return dict()
    return getJsonFile('data', title + '.json')

def SaveData(title, object):
    if not os.path.exists(GetFilePath('data')):
        os.makedirs(GetFilePath('data'))

    file_name = GetFilePath('data', title + '.json')
    with open(file_name, "w+", encoding="utf-8") as file:
        json.dump(object, file, default=str)

def getTextFile(category, file_name):
    file_name = GetFilePath(category, file_name)
    with open(file_name, "r", encoding="utf-8") as content_file:
        content = content_file.read()
    return content

def getJsonFile(category, file_name):
    file_name = GetFilePath(category, file_name)
    with open(file_name, "r", encoding="utf-8") as content_file:
        content = json.load(content_file)
    return content

def copyFromTemp(category, file_name):
    if file_name is None: return

    parts = file_name.split('.')
    parts[0] += "-template"
    temp_name = ".".join(parts)

    file_path = GetFilePath(category, file_name)
    temp_path = GetFilePath(category, temp_name)

    if not os.path.exists(file_path) and os.path.exists(temp_path):
        shutil.copyfile(temp_path, file_path)
