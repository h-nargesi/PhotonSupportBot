import time
import datetime
import threading
import database
import user
import logging
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
    now = datetime.now()
    # considering UTC time (Asia/Tehran=7:30)
    seconds_of_day = (now.replace(hour=3, minute=30, second=0, microsecond=0) - now).total_seconds()
    if seconds_of_day >= 0: return seconds_of_day
    else: return 86400 + seconds_of_day

def TrafficNextNotif():
    now = datetime.now()
    seconds_of_day = (now - now.replace(hour=0, minute=30, second=0, microsecond=0)).total_seconds()
    return 360 - seconds_of_day % 360

# CHECK USERS

def CheckMonthlyUsers():
    user_info = database.GetAllMonthlyUserInfo(-3)
    if user_info is None or len(user_info) == 0: return
    
    result = {}
    for user in user_info:
        result[user[0]] = user

    return result

def CheckTrafficUsers():
    user_info = database.GetAllTrafficUserInfo(0.1)
    if user_info is None or len(user_info) == 0: return

    result = {}
    for user in user_info:
        result[user[0]] = user

    return result

# INFINITE LOOP

def MonthleyUsers():
    while True:
        notif = CheckMonthlyUsers()
        SendWarningMessage(notif, MESSAGES_NOTIF['time-warning'])

        time.sleep(MonthlyNextNotif())

def TrafficUsers():
    while True:
        notif = CheckTrafficUsers()
        SendWarningMessage(notif, MESSAGES_NOTIF['traffic-warning'])

        time.sleep(TrafficNextNotif())

def SendWarningMessage(notif, message):
    if notif is None or len(notif) < 1: return

    for userinfo in notif:
        chat_id = gv.GetUserByName(userinfo['username'])

        logging_info = gv.GetLogInfo(chat_id)
        logging.info('expiring warning: (%s, chat: %s)', userinfo['username'], chat_id, extra=logging_info)

        if chat_id < 0: continue

        remain = user.MakeResult(chat_id, [userinfo])
        # BOT.send_message(VARIABLES.ADMIN, message.format(remain), parse_mode='markdown')

        if VARIABLES.ADMIN > 0:
            BOT.send_message(VARIABLES.ADMIN, message.format(remain), parse_mode='markdown')
