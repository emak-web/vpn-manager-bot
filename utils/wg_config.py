import subprocess
import ipaddress
from enum import Enum, auto

from config.config import settings
from messages.admin_messages import AdminMessages


class State(Enum):
    NONE = auto()
    INTERFACE = auto()
    PEER = auto()


class WireGuardConfig:
    def __init__(self):
        self.path = settings['wg_config_path']
        self.ip = settings['ip']
        self.dns = settings['dns']
        self.gen_privatekey_cmd = settings['wg_gen_privatekey_cmd']
        self.gen_publickey_cmd = settings['wg_gen_publickey_cmd']
        self.sync_cmd = settings['wg_sync_cmd']
        self.lines = []
        self.interface = {}
        self.peers = []
        self.load()
    
    def load(self):
        with open(self.path, 'r') as file:
            content = file.readlines()

        self.lines = content
        self.parse()

    def save(self):
        self.generate()
        with open(self.path, 'w') as file:
            file.writelines(self.lines)

        self.sync_config()

    def sync_config(self):
        self.run_cmd(self.sync_cmd)

    def parse(self):
        state = State.NONE
        current_peer = None
        pending_data = {}

        for line in self.lines:
            line = line.strip()

            if line.startswith('['):
                if line == '[Interface]':
                    state = State.INTERFACE
                elif line == '[Peer]':
                    if current_peer:
                        self.peers.append({**current_peer, **pending_data})
                    else:
                        self.interface = {**self.interface, **pending_data}
                    current_peer = {}
                    pending_data = {}
                    state = State.PEER

            elif line.startswith('#_'):
                key, value = line[2:].split('=', 1)
                pending_data[key.strip()] = value.strip()

            elif '=' in line:
                key, value = line.split('=', 1)
                if state == State.INTERFACE:
                    self.interface[key.strip()] = value.strip()
                elif state == State.PEER:
                    current_peer[key.strip()] = value.strip()
        
        if current_peer:
            self.peers.append({**current_peer, **pending_data})
        else:
            self.interface = {**self.interface, **pending_data}

    def generate_interface(self):
        self.lines.append(f'[Interface]\n')
        self.lines.append(f'#_PublicKey = {self.interface.get("PublicKey", self.gen_publickey(self.interface.get("PrivateKey", None)))}\n')
        self.lines.append(f'PrivateKey = {self.interface.get("PrivateKey", None)}\n')
        self.lines.append(f'Address = {self.interface.get("Address", None)}\n')
        self.lines.append(f'ListenPort = {self.interface.get("ListenPort", None)}\n')
        self.lines.append(f'PostUp = {self.interface.get("PostUp", None)}\n')
        self.lines.append(f'PostDown = {self.interface.get("PostDown", None)}\n')

    def generate_peers(self):
        for peer in self.peers:
            self.lines.append(f'\n')
            self.lines.append(f'[Peer]\n')
            self.lines.append(f'#_Name = {peer.get("Name", None)}\n')
            self.lines.append(f'#_TGUsername = {peer.get("TGUsername", None)}\n')
            self.lines.append(f'#_PrivateKey = {peer.get("PrivateKey", None)}\n')
            self.lines.append(f'PublicKey = {peer.get("PublicKey", None)}\n')
            self.lines.append(f'AllowedIPs = {peer.get("AllowedIPs", None)}\n')

    def generate(self):
        self.lines = []
        self.generate_interface()
        self.generate_peers()
                    
    def run_cmd(self, cmd, input=None):
        process = subprocess.run(
            cmd, input = input, encoding = 'utf8',
            stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell=True
        )
        return_code = process.returncode
        output = process.stdout

        return return_code, output

    def gen_publickey(self, privatekey):
        rc, publickey = self.run_cmd(self.gen_publickey_cmd, privatekey.strip())
        if rc:
            raise RuntimeError('Failed to generate public key')
        
        return publickey.strip()

    def generate_key_pair(self):
        rc, privatekey = self.run_cmd(self.gen_privatekey_cmd)
        if rc:
            raise RuntimeError('Failed to generate private key')
        
        publickey = self.gen_publickey(privatekey)

        return privatekey.strip(), publickey.strip()

    def name_exists(self, name):
        for peer in self.peers:
            if peer['Name'] == name:
                return True
        
        return False

    def generate_config(self, interface, peer):
        config = ''

        config += f'[Interface]\n'
        config += f'PrivateKey = {peer["PrivateKey"]}\n'
        config += f'Address = {peer["AllowedIPs"]}\n'
        config += f'DNS = {self.dns}\n'
        config += f'\n'
        config += f'[Peer]\n'
        config += f'PublicKey = {interface.get("PublicKey", self.gen_publickey(self.interface.get("PrivateKey", None)))}\n'
        config += f'Endpoint = {self.ip}:{interface["ListenPort"]}\n'
        config += f'AllowedIPs = 0.0.0.0/0\n'
        config += f'PersistentKeepalive = 20\n'
        
        return config
    
    def generate_config_by_name(self, name):
        for peer in self.peers:
            if peer['Name'] == name:
                return self.generate_config(self.interface, peer)
            
    def get_next_peer_ip(self, peers, network='10.0.0.0/24'):
        if peers:
            return str(ipaddress.ip_address(peers[-1]['AllowedIPs'].split('/')[0]) + 1) + '/32'
        
        return str(list(ipaddress.ip_network(network).hosts())[0] + 1) + '/32'

    def create_peer(self, name, tg_username=None):
        ip = self.get_next_peer_ip(self.peers)
        privatekey, publickey = self.generate_key_pair()

        self.peers.append({
            'Name': name,
            'TGUsername': tg_username,
            'PrivateKey': privatekey, 
            'PublicKey': publickey,
            'AllowedIPs': ip
        })

        self.save()

    def delete_peer(self, name):
        for i, peer in enumerate(self.peers):
            if peer.get('Name', None) == name:
                self.peers.pop(i)
                self.save()
        
    def get_peers(self):
        return [(peer.get('Name', None), peer.get('TGUsername', None)) for peer in self.peers]

    def show_peers(self):
        result = AdminMessages.NO_PEERS

        if self.peers:
            result = '👥 *Peers List*\n\n'

            for i, peer in enumerate(self.peers, 1):
                result += f'{i}. 👤 *{peer.get("Name", None)}* — {peer.get("TGUsername", None)}\n'
        
        return result
    
