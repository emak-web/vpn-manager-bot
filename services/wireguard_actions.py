import re 
import subprocess
import os

from config_reader import config
from services.db_connector import db


def get_vpn_status():
    status = subprocess.check_output(config.wg_status, shell=True)
    status = str(status)
    status = status.replace('       ', '')
    status = status[re.search('Active:', status).end():re.search('Docs:', status).start()-2]
    return status


def get_peers():
    status = subprocess.check_output(config.wg_peers, shell=True)
    status = str(status)

    try:
        status = status[re.search('peer:', status).start():-1]
    except AttributeError:
        pass

    status = status.replace(r'\n', '\n')
    status = status.replace('  ', '')
    
    users = db.get_users_publickeys()

    for user in users:
        fullname = user[1]
        username = user[2]
        status = status.replace(user[0], f'{fullname} @{username}')

    return status


def get_peer(fullname: str, username: str):
    status = get_peers()
    result = ''

    for peer in re.finditer(f'peer: {fullname} @{username}', status):
        new = status[peer.start():]

        try:
            end = [m.start() for m in re.finditer(f'peer:', new)][1]
        except IndexError:
            end = -1
            
        result += new[:end]
    
    result = result.replace(f'peer: {fullname} @{username}', f'Пользователь: {fullname}')
    result = result.replace('endpoint: ', 'Конечная точка: ')
    result = result.replace('allowed ips: ', 'Разрешенный IP: ')
    result = result.replace('latest handshake: ', 'Последнее рукопожатие: ')
    result = result.replace('transfer: ', 'Данные: ')
    result = result.replace('received', 'получено')
    result = result.replace('sent', 'отправлено')
    
    return result


def restart_wireguard():
    os.system(config.wg_restart)
