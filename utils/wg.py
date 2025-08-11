import subprocess
from config.config import settings

class WireGuard:
    def __init__(self):
        self.start_cmd = settings['wg_start_cmd']
        self.stop_cmd = settings['wg_stop_cmd']
        self.restart_cmd = settings['wg_restart_cmd']
        self.status_cmd = settings['wg_status_cmd']
        self.show_connections_cmd = settings['wg_show_connections_cmd']
    
    def run_cmd(self, cmd, input=None):
        process = subprocess.run(
            cmd, input = input, encoding = 'utf8',
            stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell=True
        )
        return_code = process.returncode
        output = process.stdout

        return return_code, output

    def start(self):
        return self.run_cmd(self.start_cmd)[0]
    
    def stop(self):
        return self.run_cmd(self.stop_cmd)[0]
    
    def restart(self):
        return self.run_cmd(self.restart_cmd)[0]
    
    def status(self):
        return self.run_cmd(self.status_cmd)
    
    def show_connections(self):
        return self.run_cmd(self.show_connections_cmd)
    