import mysql.connector
import files

QUERY_USER_INFO = files.GetQueryUserInfo()
CONFIGURATION = files.getConfiguration()
DATABASE = files.getDatabaseInfo()

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
    result = []

    try:
        cnx = mysql.connector.connect(**DATABASE)
        cursor = cnx.cursor()
        cursor.execute(query, values)

        for (username, left_days, left_hours, giga_left) in cursor:
            user_result = ""

            if left_days is not None and left_days > 0:
                user_result += " and {} days".format(left_days)
            if left_hours is not None and (left_hours > 0 or left_days <= 0):
                user_result += " and {} hours".format(left_hours)
            if giga_left is not None:
                user_result += " and {} GB".format(giga_left)

            if len(user_result) > 0: user_result = "*{}* remains".format(user_result[5:])
            else: user_result = "no limit!"
            
            result.append("{}: {}".format(username, user_result))

    finally:
        if cursor is not None: cursor.close()
        if cnx is not None: cnx.close()

    return result
