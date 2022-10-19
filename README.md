 


# Problem Statement

### Minimum Requirement:
* Create a web application which accept data containing following fields in JSON format using TCP Socket and show 
them in interactive widgets as per your choice.
```js
        data['mode']    = mode of flying (String)
        data['roll']    = roll angle (degrees)
        data['pitch']   = pitch angle (degrees)
        data['yaw']     = yaw angle (degrees)
        data['heading'] = current heading (degrees)
        data['long']    = current longitude (degrees)
        data['lat']     = current latitude (degrees)
        data['alt']     = current altitude ASL (meters)

```
* Using GPS coorinates plot a plotter on map. So application looks similar to following

![demo_example](./imgs/Dashboard2.png "Fleet page")

### Extrapoint (Intermediate)
* Use indicators to display data like heading, altitude, roll angle.
* ![demo_example](./imgs/2.png "Fleet page")
Heading
![demo_example](./imgs/3.png "Fleet page")
Altitude
![demo_example](./imgs/4.png "Fleet page")
Roll angle
* For the reference and helper libraries go to [/templates](./templates/) for measurement panel.
#### Just for reference you can use following 

## Understand how data is processed and accessed using following two ways:-
- In node Js
```js
/*
*======	JSON DATA FIELDS ====================
*
* 	data['mode']    =  vehicle mode name
*  	data['roll']    = roll angle 
*       data['pitch']   = pitch angle
*       data['yaw']     = yaw angle
*       data['heading'] = vehicle heading
*       data['long']    = current longitude
*       data['lat']     = current latitude
*       data['alt']     = current altitude
*============================================
*/

var net = require('net');

var client = new net.Socket();
client.connect(5000, '127.0.0.1', function() {
	console.log('Connected');
	client.write('GET'); // send acknowledge to request data
});


// Call this callback to fetch data

client.on('data', function(data) {
	client.write('GET'); // send acknowledge to request data
	console.log('Received: ' + data);
	var jsondata = JSON.parse(data);
	console.log(jsondata.mode); // "mode" field is parsed
	//client.destroy(); // kill client after server's response
});





client.on('close', function() {
	console.log('Connection closed');
});

```

- And in Python:-

```python
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

#Server IP Address
host = '127.0.0.1'
#Server Port number
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

```


Understand the Helper Codes and templates
-------------------

### API reference

This consists of Drone class inherits from Network class that creates a drone instance and send it's simulated realtime data.

```python
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
            
            
class Drone(Network):
    def __init__(self, ip, port):
        self.sitl = dronekit_sitl.start_default()
        self.connection_string = self.sitl.connection_string()
        print(bcolors.OKGREEN + bcolors.BOLD + ">>>> Connecting with the UAV <<<" + bcolors.ENDC)
        self.vehicle = connect(self.connection_string, wait_ready=True)
        Network.__init__(self, ip, port)

    # return JSON OBJECT CONTAINING DRONE'S REALTIME DATA
    def get_data(self):
        data = dict()
        data['mode'] = self.vehicle.mode.name
        data['roll'] = self.vehicle.attitude.roll
        data['pitch'] = self.vehicle.attitude.pitch
        data['yaw'] = self.vehicle.attitude.yaw
        data['heading'] = self.vehicle.heading
        data['long'] = self.vehicle.location.global_relative_frame.lon
        data['lat'] = self.vehicle.location.global_relative_frame.lon
        data['alt'] = self.vehicle.location.global_relative_frame.alt
        data_send = json.dumps(data)
        return data_send
```
It will send eight parameters to the application in JSON objects
```python
        
        data = dict()
        data['mode'] = self.vehicle.mode.name
        data['roll'] = self.vehicle.attitude.roll
        data['pitch'] = self.vehicle.attitude.pitch
        data['yaw'] = self.vehicle.attitude.yaw
        data['heading'] = self.vehicle.heading
        data['long'] = self.vehicle.location.global_relative_frame.lon
        data['lat'] = self.vehicle.location.global_relative_frame.lat
        data['alt'] = self.vehicle.location.global_relative_frame.alt
       
```



Main Thread
-------------------
This is the main thread named as "drone_server.py" which creates multiple threads as per number of drones to be created
and creates multiple tcp sockets and listening for clients. Run this code for your application.

```python

from API.SITL_SERVER import *
import _thread as thread


def main():
    """ Main Thread to run multiple drones """
    # Number to instance to be run ( change accordingly )
    instances = 2
    lon,lat = 28.5080152,77.0788194
    # IP address of the system on which this is running ( change accordingly )
    SERVER_IP = '127.0.0.1'
    # Starting port number (always use above 1023 and avoid standard ports)
    Start_port = 5000
    Drones = [None] * instances
    for i in range(instances):
        Drones[i] = Drone(SERVER_IP, Start_port + i,lat+i,lon+i)
        thread.start_new_thread(run_server, (Drones[i],))

    while 1:
        pass


if __name__ == '__main__':
    main()
```















