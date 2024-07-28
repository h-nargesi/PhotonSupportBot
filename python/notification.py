import time
import datetime
import threading
import database

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
    user_info = database.GetAllMonthlyUserInfo()
    if user_info is None or len(user_info) == 0: return
    
    result = {}
    for user in user_info:
        if user[3] > 48: continue
        result[user[0]] = user

    return result

def CheckTrafficUsers():
    user_info = database.GetAllTrafficUserInfo()
    if user_info is None or len(user_info) == 0: return

    usernames = [info[0] for info in user_info]
    topups = dict()
    for record in database.GetTopUps(usernames):
        topups[record[0]] = record
    
    result = {}
    for user in user_info:
        min = topups[record[0]][1] if record[0] in topups else 1
        if user[2] > min: continue
        result[user[0]] = user

    return result

# INFINITE LOOP

def MonthleyUsers():
    while True:
        time.sleep(MonthlyNextNotif())

def TrafficUsers():
    while True:
        time.sleep(TrafficNextNotif())