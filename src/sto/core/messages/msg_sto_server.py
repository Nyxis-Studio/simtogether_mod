import services

from services.fire_service import UiDialogNotification
from sims4.localization import LocalizationHelperTuning
from sto.core.networking.client import Client
from sto.core.networking.protocol_buffer_message import ProtocolBufferMessage
import sto.core.networking.protocolbuffers.Sto_pb2 as StoProtocols

from sto.debug.log import Logger


class MsgStoServer:
    def __init__(self, data: ProtocolBufferMessage):
        self.data = data

    def execute(self):
        sto_update = StoProtocols.StoUpdate()
        sto_update.ParseFromString(self.data.msg)

        for entry in sto_update.entries:
            for operation in entry.operation_list.operations:
                client = services.client_manager().get_first_client()

                if operation.type == StoProtocols.CONNECT_SERVER_RESPONSE:
                    msg = StoProtocols.ConnectServerResponse()
                    msg.ParseFromString(operation.data)

                    if msg.success:
                        Logger().info(
                            "Connected to server with id: {}".format(msg.client_id),
                        )

                        Client().id = msg.client_id
                        Client().set_connected()
                        Client().on_connect()

                        notification = UiDialogNotification.TunableFactory().default(
                            client.active_sim,
                            text=lambda **_: LocalizationHelperTuning.get_raw_text(
                                "Connected to server"
                            ),
                            title=lambda **_: LocalizationHelperTuning.get_raw_text(
                                "You are now connected to the server"
                            ),
                            expand_behavior=UiDialogNotification.UiDialogNotificationExpandBehavior.FORCE_EXPAND,
                            information_level=UiDialogNotification.UiDialogNotificationLevel.PLAYER,
                        )

                        notification.show_dialog()
                    else:
                        Logger().error(
                            "Error connecting to server: {}".format(msg.message),
                        )
                        notification = UiDialogNotification.TunableFactory().default(
                            client.active_sim,
                            text=lambda **_: LocalizationHelperTuning.get_raw_text(
                                "Error connecting to server: {}".format(msg.message)
                            ),
                            title=lambda **_: LocalizationHelperTuning.get_raw_text(
                                "Error connecting to server"
                            ),
                            expand_behavior=UiDialogNotification.UiDialogNotificationExpandBehavior.FORCE_EXPAND,
                            information_level=UiDialogNotification.UiDialogNotificationLevel.PLAYER,
                        )

                        notification.show_dialog()
                elif operation.type == StoProtocols.DISCONNECT:
                    msg = StoProtocols.Disconnect()
                    msg.ParseFromString(operation.data)

                    Client().disconnect(
                        title=msg.title,
                        message=msg.message,
                    )
                elif operation.type == StoProtocols.HEARTBEAT:
                    Client().heartbeat()
                else:
                    Logger().warning(
                        "Unknown operation type: {}".format(operation.type),
                    )
