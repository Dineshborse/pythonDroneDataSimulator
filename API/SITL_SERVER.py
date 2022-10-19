import socket
from dronekit import connect
import json
import dronekit_sitl
import select
from math import degrees


from urllib import request
from time import sleep
from threading import Timer


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


'''
@brief:
This class deals with Networking and uses TCP/IP Protocols (SOCKET STREAM)
Change accordingly
'''


class Network:
    # IP ADDRESS AND PORT NUMBER OF THE SERVER (MACHINE ON WHICH THIS SCRIPT IS RUNNING)
    def __init__(self, ip, port):
        self.CONNECTION_LIST = []
        self.ip = ip
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (self.ip, self.port)
        self.server.bind(self.server_address)
        self.server.listen(10)
        print(bcolors.FAIL + 'SERVER STARTED AT {0}:{1}'.format(self.ip, self.port) + bcolors.ENDC)

        self.CONNECTION_LIST.append(self.server)
        self.client = None

    """ Method to Send JSON Data """

    def send_data(self, d):

        try:
            if self.client.send(d):
                return True
            else:
                return False
        except ConnectionResetError:
            print("CLIENT OFFLINE...")
            self.client = None




''' 
@Brief:
Class which creates regular interval function exection
'''

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

''' 
@Brief:
Class which creates simulated Drone and send it's realtime data
'''


class Drone(Network):
    def __init__(self, ip, port, lat, lon):
        self.sitl = dronekit_sitl.start_default(lat, lon)
        self.connection_string = self.sitl.connection_string()
        print(bcolors.OKGREEN + bcolors.BOLD + ">>>> Connecting with the UAV <<<" + bcolors.ENDC)
        self.vehicle = connect(self.sitl.connection_string(), wait_ready=True)
        # Network.__init__(self, ip, port)

    # return JSON OBJECT CONTAINING DRONE'S REALTIME DATA
    def get_data(self):
        data = dict()
        data['mode'] = self.vehicle.mode.name
        data['roll'] = degrees(self.vehicle.attitude.roll)
        data['pitch'] = degrees(self.vehicle.attitude.pitch)
        data['yaw'] = degrees(self.vehicle.attitude.yaw)
        data['heading'] = self.vehicle.heading
        data['long'] = self.vehicle.location.global_relative_frame.lon
        data['lat'] = self.vehicle.location.global_relative_frame.lat
        data['alt'] = self.vehicle.location.global_relative_frame.alt
        data_send = json.dumps(data)
        return data_send
        #return data


# def run_server(drone):
#     isconnected = True
#     while isconnected:

#         read_sockets, write_sockets, error_sockets = select.select(drone.CONNECTION_LIST, [], [])
#         for sock in read_sockets:

#             if sock == drone.server:
#                 # Handle the case in which there is a new connection recieved
#                 # through server
#                 drone.client, addr = drone.server.accept()
#                 drone.CONNECTION_LIST.append(drone.client)
#                 print(
#                     bcolors.OKBLUE + bcolors.BOLD + bcolors.UNDERLINE + "Client (%s, %s) connected" % addr + bcolors.ENDC)

#             else:

#                 try:
#                     # Send JSON DATA TO WEB GCS whenever GCS request 'GET'
#                     ack = drone.client.recv(1024).decode()
#                     if ack == 'GET':
#                         drone.send_data(drone.get_data().encode())

#                 except KeyboardInterrupt:
#                     drone.server.close()
#                     del drone
#                     print('Server Stopped...')
#                     exit()

#                 except ConnectionResetError:
#                     drone.client.close()
#                     drone.CONNECTION_LIST.remove(sock)
#                     continue
#                     print('Client disconnected !')
#                     isconnected = False


def httpSendData(drone):
    # req = request.Request('http://localhost:5000/data', method="POST")
    req = request.Request('http://54.250.32.160:5000/data', method="POST")
    req.add_header('Content-Type', 'application/json')
    # data = {
    # "mode": 'STABILIZE',
    # "roll": "1",
    # "pitch": "2",
    # "yaw": "-22.21",
    # "heading": "337",
    # "long": "77.078819",
    # "lat": "28.508015",
    # "alt": "0.01"
    # }


    # data = json.dumps(data)
    # data = data.encode()
    r = request.urlopen(req, data=drone.get_data().encode())
    content = r.read()
    print(content)


def run_server(drone):
    isconnected = True
    rt = RepeatedTimer(0.2, httpSendData,drone) # it auto-starts, no need of rt.start()
    while isconnected:
        pass
