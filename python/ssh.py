import paramiko
import time
import re
import os
import logging
import files
import subprocess

SERVERS = files.getMikrotikServers()

def ExecuteSshAllServers(commands):
    for server in SERVERS:
        ExecuteSsh(server, commands)
    return

def ExecuteSsh(server, commands, callback = None, callback_param = None):
    if commands is None or len(commands) == 0: return None

    single_mode = isinstance(commands, str)
    if single_mode: commands = [commands]

    host = server['host']
    port = int(server['ssh']) if 'ssh' in server else 22
    username = server['username']
    password = server['password']

    logging.info(f'ssh {username}@{host} -p {port}')

    sshconn = None
    result = []

    try:
        sshconn = paramiko.SSHClient()
        sshconn.load_system_host_keys()
        sshconn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshconn.connect(host, username=username, password=password, port=port)

        index = 0
        for command in commands:
            logging.info(command)
            stdout = sshconn.exec_command(command)[1]
            rs = stdout.read().decode("utf-8")
            logging.debug(rs)
            if callback is not None:
                param = callback_param[index] if callback_param is not None else None
                rs = callback(index, command, rs, param)
                index += 1
            result.append(rs)

    finally:
        if sshconn is not None: sshconn.close()

    if single_mode: result = result[0]

    return result
