import logging
import datetime
import os

def Init():
    directory = os.path.realpath(os.path.join(os.getcwd(), "logs"))
    if not os.path.exists(directory): os.makedirs(directory)
    path = os.path.realpath(os.path.join(directory, '{:%Y-%m-%d}.log'.format(datetime.datetime.now())))

    file_handler = logging.FileHandler(path)
    format = '%(asctime)s | %(levelname)-8s | %(message)s'
    logging.basicConfig(encoding='utf-8', format=format, handlers=[file_handler], level=logging.INFO)

def formatLog(message, *params, **keywords):
    message = message.format(*params, **keywords)
    logging.error(format(message, keywords), extra=keywords)

def debug(message, *params, **keywords):
    logging.debug(format(message, keywords), *params, extra=keywords)

def info(message, *params, **keywords):
    logging.info(format(message, keywords), *params, extra=keywords)

def warning(message, *params, **keywords):
    logging.warning(format(message, keywords), *params, extra=keywords)

def error(message, *params, **keywords):
    logging.error(format(message, keywords), *params, extra=keywords)

def critical(message, *params, **keywords):
    logging.critical(format(message, keywords), *params, extra=keywords)

def format(message, keywords):
    return '%(userid)-10s | %(username)s | %(message)s' % {
        'userid': keywords['userid'] if 'userid' in keywords else None,
        'username': keywords['username'] if 'username' in keywords else None,
        'message': message
    }
