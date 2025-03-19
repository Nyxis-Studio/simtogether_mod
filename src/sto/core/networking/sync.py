import re

import time
import omega
import services

from sto.core.networking.messages import IncomingMessages
import sto.core.networking.protocolbuffers.Consts_pb2 as StoConstsProtocols

ALPHABETIC_REGEX = re.compile("[a-zA-Z]")


time_since_last_update = time.time()


def client_sync():
    global time_since_last_update

    should_update = time.time() - time_since_last_update > 0.1
    if should_update:
        time_since_last_update = time.time()
    else:
        return

    client_manager = services.client_manager()
    client = None

    if client_manager is not None:
        client = client_manager.get_first_client()

        if client is None:
            return
    else:
        return

    incoming_messages = IncomingMessages()

    for data in incoming_messages.messages:
        if data.msg_id < StoConstsProtocols.MSG_STO_SERVER:
            omega.send(client.id, data.msg_id, data.msg)
            incoming_messages.remove(data)
        else:
            from sto.core.messages.msg_sto_server import MsgStoServer

            MsgStoServer(data).execute()
            incoming_messages.remove(data)
