import sto.core.networking.sync
import game_services
import services

from sto.configs.server_config import MULTIPLAYER_MOD_ENABLED
from sims4 import core_services
from sto.core.networking.sync import client_sync


def on_tick():
    service_manager = game_services.service_manager
    sto.core.networking.sync.client_online = False

    if service_manager is None:
        return

    client_manager = services.client_manager()

    if client_manager is None:
        return

    client = client_manager.get_first_client()

    if client is None:
        return
    sto.core.networking.sync.client_online = True

    client_sync()


if MULTIPLAYER_MOD_ENABLED:
    core_services.on_tick = on_tick
