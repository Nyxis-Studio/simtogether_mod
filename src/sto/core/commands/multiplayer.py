import json
import http.client
import uuid
import sims4
import services
import sto.configs.server_config as server_config

from sims4.localization import LocalizationHelperTuning
from sto.core.networking.client import Client
from sto.core.networking.messages import OutgoingMessages
from sto.core.networking.protocol_buffer_message import ProtocolBufferMessage
from sto.core.networking.sto import build_sto_message
from sto.debug.log import Logger
from ui.ui_dialog import UiDialogOkCancel
from ui.ui_text_input import UiTextInput
from sims4.collections import AttributeDict
from sims4.tuning.tunable import (
    AutoFactoryInit,
    HasTunableSingletonFactory,
)
from ui.ui_dialog_generic import UiDialogTextInputOkCancel

import sto.core.networking.protocolbuffers.Consts_pb2 as StoConstsProtocols
import sto.core.networking.ops as StoOps


class Scum_TextInputLengthName(HasTunableSingletonFactory, AutoFactoryInit):
    __qualname__ = "Scum_TextInputLengthName"

    def build_msg(self, dialog, msg, *additional_tokens):
        msg.max_length = 100
        msg.min_length = 1
        msg.input_too_short_tooltip = LocalizationHelperTuning.get_raw_text(
            "You must enter at least one character!"
        )


@sims4.commands.Command("mp.connect", command_type=sims4.commands.CommandType.Live)
def _connect(_connection=None):
    try:
        client = services.client_manager().get_first_client()

        def enter_dialog_callback(dialog):
            if not dialog.accepted:
                Logger().debug("Dialog cancelled")
                return

            host = dialog.text_input_responses.get("host")
            port = dialog.text_input_responses.get("port")

            try:
                port = int(port)
            except ValueError:
                port = 23890

            server_info_dialog(host, port)

        server_host = UiTextInput(sort_order=0)
        server_host.default_text = None
        server_host.title = lambda **_: LocalizationHelperTuning.get_raw_text(
            "Server IP"
        )
        server_host.max_length = 100
        server_host.initial_value = lambda **_: LocalizationHelperTuning.get_raw_text(
            "127.0.0.1"
        )
        server_host.length_restriction = Scum_TextInputLengthName()
        server_host.restricted_characters = None
        server_host.check_profanity = False
        server_host.height = 10

        server_port = UiTextInput(sort_order=1)
        server_port.default_text = None
        server_port.title = lambda **_: LocalizationHelperTuning.get_raw_text(
            "Server Port"
        )
        server_port.max_length = 100
        server_port.initial_value = lambda **_: LocalizationHelperTuning.get_raw_text(
            "23890"
        )
        server_port.length_restriction = Scum_TextInputLengthName()
        server_port.restricted_characters = None
        server_port.check_profanity = False
        server_port.height = 10

        inputs = AttributeDict({"host": server_host, "port": server_port})
        dialog = UiDialogTextInputOkCancel.TunableFactory().default(
            client.active_sim,
            text=lambda **_: LocalizationHelperTuning.get_raw_text(
                "Enter the server IP and Port to connect to"
            ),
            title=lambda **_: LocalizationHelperTuning.get_raw_text(
                "Connect to server"
            ),
            text_inputs=inputs,
            is_special_dialog=True,
            text_ok=lambda **_: LocalizationHelperTuning.get_raw_text("Search server"),
        )
        dialog.add_listener(enter_dialog_callback)
        dialog.show_dialog()
    except Exception as e:
        Logger().error("Failed on connect command.", e)


def server_info_dialog(host: str, port: int):
    try:
        conn = http.client.HTTPConnection(f"{host}:{str(server_config.GATEWAY_PORT)}")
        conn.request("GET", "/status")

        response = conn.getresponse()

        response = response.read().decode("utf-8")
        json_data = json.loads(response)

        conn.close()

        def enter_dialog_callback(dialog):
            if not dialog.accepted:
                return
            try:
                Logger().info("Init connection to server")
                Client().connect(host, port)

                connect_server = StoOps.ConnectServer(str(uuid.uuid4()))

                message = ProtocolBufferMessage(
                    StoConstsProtocols.MSG_STO_SERVER,
                    build_sto_message(connect_server).SerializeToString(),
                )

                OutgoingMessages().add(message)
            except ConnectionRefusedError:
                from ui.ui_dialog_notification import UiDialogNotification

                client = services.client_manager().get_first_client()

                notification = (
                    UiDialogNotification()
                    .TunableFactory()
                    .default(
                        client.active_sim,
                        title=lambda **_: LocalizationHelperTuning.get_raw_text(
                            "Failed to connect"
                        ),
                        text=lambda **_: LocalizationHelperTuning.get_raw_text(
                            "The server refused the connection."
                        ),
                    )
                )

                notification.show_dialog()
            except Exception as e:
                Logger().error("Failed to connect to server.", e)

        client = services.client_manager().get_first_client()

        name = json_data.get("name")
        description = json_data.get("description")
        player_count = json_data.get("player_count")
        max_player_count = json_data.get("max_player_count")
        version = json_data.get("version")

        dialog = UiDialogOkCancel.TunableFactory().default(
            client.active_sim,
            title=lambda **_: LocalizationHelperTuning.get_raw_text(
                "Connect to {}".format(name)
            ),
            text=lambda **_: LocalizationHelperTuning.get_raw_text(
                f"Do you want to connect to the server {name}? \n\n"
                f"Description: {description} \n"
                f"Players: {player_count}/{max_player_count} \n"
                f"Version: {version}",
            ),
            is_special_dialog=True,
            text_ok=lambda **_: LocalizationHelperTuning.get_raw_text("Connect"),
        )

        dialog.add_listener(enter_dialog_callback)
        dialog.show_dialog()

    except Exception as e:
        Logger().error("Failed on server_info_dialog.", e)


@sims4.commands.Command("mp.disconnect", command_type=sims4.commands.CommandType.Live)
def _disconnect(_connection=None):
    output = sims4.commands.Output(_connection)
    output("Disconnecting from server...")

    try:
        Client().disconnect(
            title="Disconnected",
            message="You have been disconnected from the server",
        )

    except Exception as e:
        Logger().error("Failed on disconnect command.", e)
