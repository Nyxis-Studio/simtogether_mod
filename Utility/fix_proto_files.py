import os

PROTO_FILES_PATH = "src/sto/core/networking/protocolbuffers/"


def fix_proto_files():
    for proto_file in os.listdir(PROTO_FILES_PATH):
        if proto_file.endswith("_pb2.py"):
            with open(PROTO_FILES_PATH + proto_file, "r") as file:
                content = file.read()
                content = content.replace('unicode("", "utf-8")', "b''.decode('utf-8')")
                content = content.replace(
                    "message.Message",
                    "message.Message, metaclass=reflection.GeneratedProtocolMessageType",
                )
                content = content.replace(
                    "\n  __metaclass__ = reflection.GeneratedProtocolMessageType", ""
                )

                with open(PROTO_FILES_PATH + proto_file, "w") as file:
                    file.write(content)
