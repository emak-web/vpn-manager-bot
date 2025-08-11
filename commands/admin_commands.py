from dataclasses import dataclass


@dataclass
class AdminCommands:
    # /start
    MAIN_MENU: str = '🏠 Main Menu'
    MANAGE_PEERS: str = '👥 Manage Peers'
    MANAGE_WG: str = '🛠 Manage WireGuard'

    # Manage peers
    CREATE_PEER: str = '👤 Create peer'
    DELETE_PEER: str = '🗑 Delete peer'
    GENERATE_CONFIG: str = '📝 Generate config'
    SHOW_PEERS: str = '👥 Show peers'
    CONFIRM: str = '✅ Confirm'
    CANCEL: str = '❌ Cancel'

    # Manage WireGuard
    START_WG: str = '▶️ Start'
    STOP_WG: str = '🛑 Stop'
    RESTART_WG: str = '🔄 Restart'
    STATUS_WG: str = '📊 Status'
    SHOW_CONNECTIONS_WG: str = '🔍 Show connections'

