import os

PROTO_FILES_PATH = "src/sto/core/networking/protocolbuffers/"


def clean_proto_files():
    for proto_file in os.listdir(PROTO_FILES_PATH):
        if proto_file.endswith("_pb2.py"):
            os.remove(PROTO_FILES_PATH + proto_file)
