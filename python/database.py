import mysql.connector
import datetime as dt
import files

class CacheItem:
    Time = None
    Data = None

QUERY_USER_INFO = files.GetQueryUserInfo()
CONFIGURATION = files.getConfiguration()
DATABASE = files.getDatabaseInfo()
CACHE = dict()

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
    ClearCache()
    
    key = " ".join(values)
    if key in CACHE:
        return CACHE[key].data

    result = []

    try:
        cnx = mysql.connector.connect(**DATABASE)
        cursor = cnx.cursor()
        cursor.execute(query, values)

        for (username, left_days, left_hours, giga_left) in cursor:
            account_info = ""

            if left_days is not None and left_days > 0:
                account_info += " and {} days".format(left_days)
            if left_hours is not None and (left_hours > 0 or left_days <= 0):
                account_info += " and {} hours".format(left_hours)
            if giga_left is not None:
                account_info += " and {} GB".format(giga_left)

            if len(account_info) > 0: account_info = "*{}* remains".format(account_info[5:])
            else: account_info = "no limit!"
            
            result.append("{}: {}".format(username, account_info))

    finally:
        if cursor is not None: cursor.close()
        if cnx is not None: cnx.close()

    result = "\n".join(result)
    CACHE[key] = {
        'time': dt.datetime.now(),
        'data': result
    }

    return result

def ClearCache():
    cache = dict()
    index_time = dt.datetime.now() - dt.timedelta(minutes=5)

    for key, value in CACHE:
        if value.time >= index_time:
            cache[key] = value

    CACHE = cache