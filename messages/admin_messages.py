from dataclasses import dataclass


@dataclass
class AdminMessages:
    WELCOME: str = 'How to use this bot...'
    MAIN_MENU: str = '✅ Main Menu'
    MANAGE_PEERS: str = '👥 Manage Peers'
    MANAGE_WG: str = '🛠 Manage WireGuard'

    CHOOSE_PEER: str = '👤 Please choose a peer'
    CREATE_PEER_NAME: str = '✏️ Type a name for the new peer:'
    NAME_ALREADY_EXISTS: str = '⚠️ Name already exists, please try again'
    CREATE_PEER_TG_USERNAME: str = '📱 Type their Telegram username:'
    CREATE_PEER_CONFIRM: str = '❓ Create this peer?'
    DELETE_PEER_CONFIRM: str = '❗️ Delete this peer?'
    NO_PEERS: str = 'ℹ️ No peers added yet'
    DONE: str = '✅ Done'
    CANCELED: str = '❌ Operation canceled'
    ERROR: str = '❌ An error occurred'

