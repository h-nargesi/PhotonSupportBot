import threading
import mysql.connector as sql
import datetime as dt
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

def GetAllMonthlyUserInfo():
    query = QUERY_USER_INFO.replace("@where", "u.expiration is not null")
    return ReadQuery(query, None)

def GetAllTrafficUserInfo():
    query = QUERY_USER_INFO.replace("@where", " u.reset_type_data is not null")
    return ReadQuery(query, None)

def GetUserInfoByAdmin(username):
    query = QUERY_USER_INFO.replace("@where", "username like %s")
    return ReadQuery(query, (username, ))

def GetAllUserInfoByPhone(phone):
    query = QUERY_USER_INFO.replace("@where", "phone = %s")
    return ReadQuery(query, (phone, ))

def GetUserInfoByPhone(username, phone):
    query = QUERY_USER_INFO.replace("@where", "username like %s and phone like %s")
    return ReadQuery(query, (username, phone))

def GetUserInfoByPassword(username, password):
    query = QUERY_USER_INFO.replace("@where", "username like %s and clear_password = %s")
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
    index_time = dt.datetime.now() - dt.timedelta(seconds=CONFIGURATION['cache-seconds'])

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

        for row in cursor:
            result.append(row)

    except Exception as ex:
        result = [ MESSAGES['reading-error'] ]
        logging.error('database call (%s): %s', ')('.join(values), ex, extra={ 'userid': None, 'username': None })
    
    finally:
        if cursor is not None: cursor.close()
        if cnx is not None: cnx.close()
    
    return result