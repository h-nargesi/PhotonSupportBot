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
QUERY_TOPUP_INFO = files.GetQueryTopupInfo()
DATABASE = files.getDatabaseInfo()
CACHE = dict()
LOCK = threading.Lock()

CATEGORY_USER_INFO_QUERY = 'USER'
CATEGORY_TOPUP_INFO_QUERY = 'TOPUP'

def GetAllMonthlyUserInfo():
    query = QUERY_USER_INFO.replace("@where", "u.expiration is not null")
    return ReadQuerySingleCache(query, CATEGORY_USER_INFO_QUERY, None)

def GetAllTrafficUserInfo():
    query = QUERY_USER_INFO.replace("@where", " u.reset_type_data is not null")
    return ReadQuerySingleCache(query, CATEGORY_USER_INFO_QUERY, None)

def GetUserInfoByAdmin(username):
    query = QUERY_USER_INFO.replace("@where", "username like %s")
    return ReadQuerySingleCache(query, CATEGORY_USER_INFO_QUERY, (username, ))

def GetAllUserInfoByPhone(phone):
    query = QUERY_USER_INFO.replace("@where", "phone = %s")
    return ReadQuerySingleCache(query, CATEGORY_USER_INFO_QUERY, (phone, ))

def GetUserInfoByPhone(username, phone):
    query = QUERY_USER_INFO.replace("@where", "username like %s and phone like %s")
    return ReadQuerySingleCache(query, CATEGORY_USER_INFO_QUERY, (username, phone))

def GetUserInfoByPassword(username, password):
    query = QUERY_USER_INFO.replace("@where", "username like %s and clear_password = %s")
    return ReadQuerySingleCache(query, CATEGORY_USER_INFO_QUERY, (username, password))

def GetTopUps(usernames):
    query = QUERY_TOPUP_INFO.replace("@where", f"u.username in ('{"', '".join(usernames)}')")
    return QueryDatabase(query, None)

def ExtendUser(user):
    return user

def ReadQuerySingleCache(query, category, values):
    if category is None: return QueryDatabase(query, values)

    with LOCK:
        ClearCache()
    
    key = f'{category}|{" ".join(values) if values is not None else "None"}'

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

# def ReadQueryMultipleCache(query, category, values_set):
#     if category is None: return QueryDatabase(query, values)

#     with LOCK:
#         ClearCache()

#     temp = []
#     result = []
#     keys = []

#     for values in values_set:
#         key = f'{category}|{" ".join(values) if values is not None else "None"}'

#         if key in CACHE and CACHE[key].Data is not None and len(CACHE[key].Data) > 0:
#             result.append(CACHE[key].Data)
#             continue

#         temp.append(values)
#         keys.append(key)
    
#         current_item = CacheItem(
#             dt.datetime.now(), 
#             MESSAGES['user']['please-retry'])

#         with LOCK:
#             CACHE[key] = current_item
    
#     values_set = temp

#     current_item.Data = QueryDatabase(query, values_set)
#     current_item.Time = dt.datetime.now()

#     return current_item.Data

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