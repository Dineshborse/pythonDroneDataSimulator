import socket
import json
from math import degrees


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


host = '127.0.0.1'
port = 5000

# create a socket at client side
# using TCP / IP protocol
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# connect it to server and port
# number on local computer.
s.connect((host, port))

while True:
    try:
        # Send request to receive data
        if s.send('GET'.encode()):
            msg = s.recv(1024)
        else:
            print('Request fails !!!')

        data = msg.decode()
        # JSON formatted data
        data = json.loads(data)
        print(bcolors.OKGREEN + "DATA" + bcolors.FAIL + bcolors.BOLD + str(data) + bcolors.ENDC)

    except KeyboardInterrupt:
        # disconnect the client
        s.close()
