from threading import Lock

from sto.core.networking.protocol_buffer_message import ProtocolBufferMessage
from sto.core.singleton import SingletonMeta


class HandlerMessages:
    def __init__(self):
        self._locker = Lock()
        self._messages = list()

    def add(self, data: ProtocolBufferMessage):
        with self._locker:
            self._messages.append(data)

    def remove(self, data: ProtocolBufferMessage):
        with self._locker:
            self._messages.remove(data)

    def get_next_message(self):
        with self._locker:
            if len(self._messages) > 0:
                return self._messages.pop(0)
        return None

    @property
    def locker(self):
        return self._locker

    @property
    def messages(self):
        return self._messages


class IncomingMessages(HandlerMessages, metaclass=SingletonMeta):
    pass


class OutgoingMessages(HandlerMessages, metaclass=SingletonMeta):
    pass
