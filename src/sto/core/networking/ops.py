import sto.core.networking.protocolbuffers.Sto_pb2 as sto_procotol

from distributor.ops import Op


class ConnectServer(Op):
    def __init__(self, client_hash):
        super().__init__()
        self.op = sto_procotol.ConnectServer()
        self.op.hash = client_hash

    def write(self, msg):
        self.serialize_op(msg, self.op, sto_procotol.CONNECT_SERVER)


class Heartbeat(Op):
    def __init__(self):
        super().__init__()

    def write(self, msg):
        msg.type = sto_procotol.HEARTBEAT
