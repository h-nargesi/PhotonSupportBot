import time
import datetime
import threading
import database
import user
import log
import globalvalues as gv

from globalvalues import BOT, MESSAGES, VARIABLES

MESSAGES_NOTIF = None

def Init():
    global MESSAGES_NOTIF
    MESSAGES_NOTIF = MESSAGES["expiring-warning"]

def StartService():
    threading.Thread(target = MonthleyUsers).start()
    threading.Thread(target = TrafficUsers).start()
    return

# NEXT TIME

def MonthlyNextNotif():
    now = datetime.datetime.now()
    # considering UTC time (Asia/Tehran=7:30)
    seconds_of_day = (now.replace(hour=3, minute=30, second=0, microsecond=0) - now).total_seconds()
    if seconds_of_day >= 0: return seconds_of_day
    else: return 86400 + seconds_of_day

def TrafficNextNotif():
    now = datetime.datetime.now()
    seconds_of_day = (now - now.replace(hour=0, minute=30, second=0, microsecond=0)).total_seconds()
    return 60 - seconds_of_day % 60

# CHECK USERS

def CheckMonthlyUsers():
    user_info = database.GetAllMonthlyUserInfo(-10)
    if user_info is None or len(user_info) == 0: return {}
    
    result = {}
    for user in user_info:
        result[user[0]] = user

    return result

def CheckTrafficUsers():
    user_info = database.GetAllTrafficUserInfo(0.1)
    if user_info is None or len(user_info) == 0: return {}

    result = {}
    for user in user_info:
        result[user[0]] = user

    return result

# INFINITE LOOP

def MonthleyUsers():
    while True:
        notif = CheckMonthlyUsers()
        log.info('monthly user checked: expiring count = %s', len(notif))
        SendWarningMessage(notif, MESSAGES_NOTIF['time-warning'])

        time.sleep(MonthlyNextNotif())

def TrafficUsers():
    while True:
        notif = CheckTrafficUsers()
        log.info('traffic user checked: expiring count = %s', len(notif))
        SendWarningMessage(notif, MESSAGES_NOTIF['traffic-warning'])

        time.sleep(TrafficNextNotif())

def SendWarningMessage(notif, message):
    if notif is None or len(notif) < 1: return

    for username in notif:
        userinfo = notif[username]
        chat_id = gv.GetUserByName(username)

        log.info('expiring warning: (%s, chat: %s) %s', username, chat_id, userinfo, **gv.GetLogInfo(chat_id))

        remain = user.MakeResult(chat_id, [userinfo])

        # if chat_id > 0:
        #     BOT.send_message(VARIABLES.ADMIN, message.format(remain), parse_mode='markdown')

        if VARIABLES.ADMIN > 0:
            BOT.send_message(VARIABLES.ADMIN, message.format(remain), parse_mode='markdown')
