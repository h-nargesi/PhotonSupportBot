import threading
import mysql.connector
import datetime as dt
import files

class CacheItem:
    def __init__(self, time, data):
        self.Time = time
        self.Data = data

QUERY_USER_INFO = files.GetQueryUserInfo()
CONFIGURATION = files.getConfiguration()
MESSAGES = files.getMessages()
DATABASE = files.getDatabaseInfo()
CACHE = dict()
LOCK = threading.Lock()

def GetAllUserInfoByPhone(phone):
    query = QUERY_USER_INFO.replace("where", "where phone = %s")
    return ExecuteQuery(query, (phone))

def GetUserInfoByPhone(username, phone):
    query = QUERY_USER_INFO.replace("where", "where username = %s and phone = %s")
    return ExecuteQuery(query, (username, phone))

def GetUSerInfoByPassword(username, password):
    query = QUERY_USER_INFO.replace("where", "where username = %s and clear_password = %s")
    return ExecuteQuery(query, (username, password))

def ExecuteQuery(query, values):
    key = " ".join(values)

    with LOCK:
        ClearCache()
    
    if key in CACHE:
        return CACHE[key].Data
    
    current_item = CacheItem(
        dt.datetime.now(), 
        MESSAGES['please-wait'])

    with LOCK:
        CACHE[key] = current_item

    current_item.Data = QueryDatabase(query, values)
    current_item.Time = dt.datetime.now()

    return current_item.Data

def ClearCache():
    temp = dict()
    index_time = dt.datetime.now() - dt.timedelta(minutes=CONFIGURATION['cache-minutes'])

    for key, value in CACHE.items():
        if value.Time >= index_time:
            temp[key] = value

    return temp

def QueryDatabase(query, values):
    result = []

    try:
        cnx = mysql.connector.connect(**DATABASE)
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

    finally:
        if cursor is not None: cursor.close()
        if cnx is not None: cnx.close()

    return "\n".join(result)