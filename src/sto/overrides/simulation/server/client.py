import omega
import server.client

from sto.configs.server_config import MULTIPLAYER_MOD_ENABLED
from sto.core.networking.client import Client
from sto.core.networking.messages import OutgoingMessages
from sto.core.networking.protocol_buffer_message import ProtocolBufferMessage


def send_message(self, msg_id, msg):
    if self.active:
        if Client().is_connected():
            message = ProtocolBufferMessage(msg_id, msg.SerializeToString(), self.id)
            OutgoingMessages().add(message)
        else:
            omega.send(self.id, msg_id, msg.SerializeToString())


if MULTIPLAYER_MOD_ENABLED:
    server.client.Client.send_message = send_message
