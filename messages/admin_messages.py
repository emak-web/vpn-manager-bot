from dataclasses import dataclass


@dataclass
class AdminMessages:
    WELCOME: str = 'How to use this bot:\n...\n...\n...'
    MAIN_MENU: str = '✅ Main Menu'
    MANAGE_PEERS: str = '✅ Manage Peers'

    CREATE_PEER_NAME: str = 'Type a name for the new peer'
    CREATE_PEER_TG_USERNAME: str = 'Type their telegram username'
    CREATE_PEER_CONFIRM: str = 'Create peer?'
    DELETE_PEER_CONFIRM: str = 'Delete peer?'
    DONE: str = '✅ Done'
    CANCELED: str = '❌ Canceled'
    CHOSE_PEER: str = '👤 *Chose peer*'

    MANAGE_WG: str = '✅ Manage WG'