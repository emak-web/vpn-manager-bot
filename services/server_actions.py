import psutil
import os

def get_server_status():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory()

    used = str((ram.total-ram.available)/(1024**3))[:4]

    return f'CPU usage: {cpu}%\nRAM usage: {ram.percent}% ({used}GB)'


def restart_server():
    os.system('sudo reboot')
