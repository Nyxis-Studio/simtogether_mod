import subprocess

from Utility.fix_proto_files import fix_proto_files
from Utility.clean_proto_files import clean_proto_files

clean_proto_files()

subprocess.run(
    [
        ".\\Utility\\protoc.exe",
        "--proto_path=./",
        "--python_out=./",
        "src/sto/core/networking/protocolbuffers/*.proto",
    ],
    check=True,
)

fix_proto_files()

print("Protobuf files compiled successfully")
