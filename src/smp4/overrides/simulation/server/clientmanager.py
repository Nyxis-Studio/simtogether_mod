import server.clientmanager

from smp4.configs.server_config import MULTIPLAYER_MOD_ENABLED

def get_first_client(self):
    # Get the original client instead of the stand-in client. Just in-case some EA code is finnicky with multiple clients. Only supports one
    # multiplayer client at the moment.
    for client in self._objects.values():
        if client.id == 1000:
            continue

        return client

def get_first_client_id(self):
    # Get the original client instead of the stand-in client. Just in-case some EA code is finnicky with multiple clients. Only supports one
    # multiplayer client at the moment.
    for client in self._objects.values():
        if client.id == 1000:
            continue

        return client.id

if MULTIPLAYER_MOD_ENABLED:
    server.clientmanager.ClientManager.get_first_client = get_first_client
    server.clientmanager.ClientManager.get_first_client_id = get_first_client_id