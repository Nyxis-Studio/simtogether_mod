import socket
import threading
import time
import services

from sims4.localization import LocalizationHelperTuning
from sto.core.networking.messages import IncomingMessages, OutgoingMessages
from sto.core.networking.protocol_buffer_message import ProtocolBufferMessage
from sto.core.networking.sto import build_sto_message
from sto.core.singleton import SingletonMeta
from sto.debug.log import Logger

import sto.core.networking.protocolbuffers.Consts_pb2 as StoConstsProtocols
import sto.core.networking.ops as StoOps


class Client(metaclass=SingletonMeta):
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.id = -1

        self.host = "localhost"
        self.port = 23890
        self.socket.bind(("0.0.0.0", 0))

        self.alive = True
        self._connected = False

        self._last_heartbeat = time.time()

        self.listen_thread = None
        self.listen_stop_event = threading.Event()

        self.send_thread = None
        self.send_stop_event = threading.Event()

        self.heartbeat_thread = None
        self.heartbeat_stop_event = threading.Event()

        self.stop_event = threading.Event()

        Logger().info("Client started at {}:{}".format(self.host, self.port))

        self._listen_init_threading()

    def connect(self, host, port):
        try:
            self.host = host
            self.port = port

            Logger().info(
                "Connecting to {}:{}".format(self.host, self.port),
            )

            if self.send_thread is not None and self.send_thread.is_alive():
                self.send_stop_event.set()
                self.send_thread.join()

            self.send_stop_event.clear()
            self._send_init_threading()

        except Exception as e:
            Logger().error("Error connecting to server:", e)

    def _listen_init_threading(self):
        self.listen_thread = threading.Thread(target=self._listen_loop, args=[])
        self.listen_thread.start()

    def _send_init_threading(self):
        self.send_thread = threading.Thread(target=self._send_loop, args=[])
        self.send_thread.start()

    def _heartbeat_init_threading(self):
        self.heartbeat_thread = threading.Thread(target=self._heartbeat_loop, args=[])
        self.heartbeat_thread.start()

    def _heartbeat_loop(self):
        Logger().debug("Heartbeat loop started")
        while (
            self.alive
            and self.is_connected()
            and not self.stop_event.is_set()
            and not self.heartbeat_stop_event.is_set()
        ):
            try:
                if time.time() - self._last_heartbeat > 25:
                    self.disconnect("Connection lost", "Connection lost")
                    break

                request_server_info = StoOps.Heartbeat()

                message = ProtocolBufferMessage(
                    StoConstsProtocols.MSG_STO_SERVER,
                    build_sto_message(request_server_info).SerializeToString(),
                )
                OutgoingMessages().add(message)
            except Exception as e:
                Logger().error("Error sending heartbeat to server", e)

            time.sleep(1)

        Logger().debug("Heartbeat loop stopped")

    def _send_loop(self):
        Logger().debug("Sending loop started")
        while (
            self.alive
            and not self.stop_event.is_set()
            and not self.send_stop_event.is_set()
        ):
            try:
                next_message = OutgoingMessages().get_next_message()

                if next_message is None:
                    time.sleep(0.1)
                    continue

                self.socket.sendto(next_message.encoded(), (self.host, self.port))
            except Exception as e:
                Logger().error(
                    "Error sending message to server",
                    e,
                )

        Logger().debug("Sending loop stopped")

    def _listen_loop(self):
        Logger().debug("Listening loop started")
        while (
            self.alive
            and not self.stop_event.is_set()
            and not self.listen_stop_event.is_set()
        ):
            try:
                data, _ = self.socket.recvfrom(99999)

                data = ProtocolBufferMessage.from_json(data.decode())

                IncomingMessages().add(data)
            except ConnectionResetError:
                continue
            except Exception as e:
                Logger().error("Error listening to server", e)
        Logger().debug("Listening loop stopped")

    def set_connected(self):
        self._connected = True

    def is_connected(self) -> bool:
        return self._connected

    def disconnect(self, title: str, message: str):
        self._connected = False

        self.heartbeat_stop_event.set()
        self.send_stop_event.set()

        from ui.ui_dialog_notification import UiDialogNotification

        client = services.client_manager().get_first_client()

        notification = (
            UiDialogNotification()
            .TunableFactory()
            .default(
                client.active_sim,
                title=lambda **_: LocalizationHelperTuning.get_raw_text(title),
                text=lambda **_: LocalizationHelperTuning.get_raw_text(message),
            )
        )

        notification.show_dialog()

    def kill(self):
        self._connected = False
        self.alive = False
        self.stop_event.set()

        self.listen_stop_event.set()
        self.send_stop_event.set()
        self.heartbeat_stop_event.set()

    def is_killed(self) -> bool:
        for thread in self.threads:
            if thread.is_alive():
                return False

        return True

    def on_connect(self):
        self._last_heartbeat = time.time()
        self._heartbeat_init_threading()

    def heartbeat(self):
        self._last_heartbeat = time.time()
