from API.SITL_SERVER import *
import _thread as thread


def main():
    """ Main Thread to run multiple drones """
    # Number to instance to be run ( change accordingly )
    instances = 1
    lon,lat = 28.5080152,77.0788194
    # IP address of the system on which this is running ( change accordingly )
    SERVER_IP = 'localhost'
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
