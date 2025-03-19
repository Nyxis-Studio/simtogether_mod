import json
import base64


class ProtocolBufferMessage:
    def __init__(self, msg_id: int, msg: bytes, session_id: int = 0, fails: int = 0):
        self.msg_id = msg_id
        self.msg = msg
        self.session_id = session_id
        self.fails = fails

    def to_json(self):
        return json.dumps(
            {
                "msg_id": self.msg_id,
                "msg": base64.b64encode(self.msg).decode(),
                "session_id": self.session_id,
                "fails": self.fails,
            }
        )

    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        return ProtocolBufferMessage(
            data["msg_id"],
            base64.b64decode(data["msg"]),
            data["session_id"],
            data["fails"],
        )

    def encoded(self):
        return self.to_json().encode()
