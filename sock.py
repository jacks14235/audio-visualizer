import socket
import pickle
import sys

HOST = '192.168.1.159'
PORT = 7777


with socket.socket() as sock:
    sock.connect((HOST, int(PORT)))
    while True:
        try:
            arr = pickle.load(sys.stdin.buffer)
            out_flo = sock.makefile(mode='wb')
            pickle.dump(arr, out_flo)
        except pickle.UnpicklingError as p:
            print("ERROR:", p)
        except OSError as e:
            print("OSError", e)