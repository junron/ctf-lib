import os
from binascii import a2b_hex
from typing import Union, Callable
import pwnlib.tubes.process

SetupFunction = Callable[[], pwnlib.tubes.process.process]


def decode_to_ascii(input: Union[str, int, bytes]) -> bytes:
    if type(input) == int:
        input = hex(input)
    if type(input) == bytes:
        input = input.decode("utf-8")
    if input[:2] == "0x":
        input = input[2:]
    return a2b_hex(input)[::-1]


def get_pie_base(pid: int) -> int:
    return int(os.popen("pmap {}| awk '{{print $1}}'".format(pid)).readlines()[1], 16)


def get_libc_base(pid: int) -> int:
    data = [x for x in os.popen(f"pmap {pid}").readlines() if "libc" in x]
    if data:
        return int(data[0].split(" ")[0], 16)


def get_ld_base(pid: int) -> int:
    data = [x for x in os.popen(f"pmap {pid}").readlines() if "ld" in x]
    if data:
        return int(data[0].split(" ")[0], 16)


# Parses `connect_str`, which is in one of the following forms:
# <host>:<port>
# <host> <port>
# nc <host <port>
def remote(connect_str: str) -> pwnlib.tubes.remote:
    connect_str.strip()
    if connect_str.startswith("nc"):
        connect_str = connect_str.split(" ")[1]
    if " " in connect_str:
        host, port = connect_str.split(" ")
    else:
        host, port = connect_str.split(":")
    return pwnlib.tubes.remote.remote(host.strip(), int(port.strip()))
