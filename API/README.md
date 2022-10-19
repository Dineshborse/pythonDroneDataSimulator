--------------
About this API:
--------------
### SITL_SERVER:

* This file contrains two classes which creates a virtual Drone and send JSON data to Web Application on connecting
    - IP address of the machine on which it is running and Port number is required
    - This IP address and port number is used to connect from Web Application
    - This script consists of two class Parent class Network and child class Drone


### JSON DATA:
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

* python libraries required:
  - dronekit:
```bash
pip install dronekit or pip3 install dronekit
```
if fails to install using pip then build it from source-
```commandline 
git clone https://github.com/dronekit/dronekit-python.git
cd dronekit-python
python setup.py build
python setup.py install
```

- dronekit_sitl:

  ```commandline
  pip install dronekit_sitl or pip3 install dronekit_sitl
  ```
