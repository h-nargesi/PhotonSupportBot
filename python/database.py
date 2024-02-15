import threading
import mysql.connector as sql
import datetime as dt
import re
import files
import logging

from globalvalues import MESSAGES, CONFIGURATION

class CacheItem:
    def __init__(self, time, data):
        self.Time = time
        self.Data = data

QUERY_USER_INFO = files.GetQueryUserInfo()
DATABASE = files.getDatabaseInfo()
CACHE = dict()
LOCK = threading.Lock()

def GetUserInfoByAdmin(username):
    query = QUERY_USER_INFO.replace("@where", "username = %s")
    return ReadQuery(query, (username, ))

def GetAllUserInfoByPhone(phone):
    query = QUERY_USER_INFO.replace("@where", "phone = %s")
    return ReadQuery(query, (phone, ))

def GetUserInfo(username, secret):
    isphone = re.search("^\+\d+$", secret)
    if isphone: return GetUserInfoByPhone(username, secret)
    else: return GetUserInfoByPassword(username, secret)

def GetUserInfoByPhone(username, phone):
    query = QUERY_USER_INFO.replace("@where", "username = %s and phone = %s")
    return ReadQuery(query, (username, phone))

def GetUserInfoByPassword(username, password):
    query = QUERY_USER_INFO.replace("@where", "username = %s and clear_password = %s")
    return ReadQuery(query, (username, password))

def ExtendUser(user):
    return user

def ReadQuery(query, values):
    key = " ".join(values)

    with LOCK:
        ClearCache()
    
    if key in CACHE and CACHE[key].Data is not None and len(CACHE[key].Data) > 0:
        return CACHE[key].Data
    
    current_item = CacheItem(
        dt.datetime.now(), 
        MESSAGES['user']['please-retry'])

    with LOCK:
        CACHE[key] = current_item

    current_item.Data = QueryDatabase(query, values)
    current_item.Time = dt.datetime.now()

    return current_item.Data

def ClearCache():
    global CACHE

    temp = dict()
    index_time = dt.datetime.now() - dt.timedelta(minutes=CONFIGURATION['cache-minutes'])

    for key, value in CACHE.items():
        if value.Time >= index_time:
            temp[key] = value

    CACHE = temp

def QueryDatabase(query, values):
    result = []

    try:
        cnx = sql.connect(**DATABASE)
        cursor = cnx.cursor()
        cursor.execute(query, values)

        for (username, left_days, left_hours, giga_left) in cursor:
            account_info = ""

            if left_days is not None and left_days > 0:
                account_info += " and *{} days*".format(left_days)
            if left_hours is not None and (left_hours > 0 or left_days <= 0):
                account_info += " and *{} hours*".format(left_hours)
            if giga_left is not None:
                account_info += " and *{} GB*".format(giga_left)

            if len(account_info) > 0: account_info = "{} remains".format(account_info[5:])
            else: account_info = "*no limit!*"
            
            result.append("{}: {}".format(username, account_info))

    except Exception as ex:
        result = [ MESSAGES['reading-error'] ]
        logging.error('database call (%s): %s', ')('.join(values), ex, extra={ 'userid': None })
    
    finally:
        if cursor is not None: cursor.close()
        if cnx is not None: cnx.close()

    return "\n".join(result)