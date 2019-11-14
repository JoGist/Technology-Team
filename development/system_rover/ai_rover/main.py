import multiprocessing
import time
import json
import sys, os, socket
from multiprocessing.managers import BaseManager
from sensors.Imu import Imu
from sensors.DistanceSensor import DistanceSensor
from server.Connection import Connection
from socketIO_client import SocketIO, LoggingNamespace

from rover.Rover import Rover

def uploadSensors(rover):
    while True:
        # print ('SENSORS UPDATE')
        rover.uploadDataSensors()
        rover.sendMessage('data_sensors',rover.getDataSensorsJson())
        # rover.testMotors()
        rover.execTask()
        time.sleep(0.1)
        pass
# def artificial_intelligence(rover):
#     print ('start')
#     # while True:
#     #     rover.execTask()
#     #     pass

def startConnection(rover):
    rover.start_connection()
    rover.wait_forever()

def main():
    BaseManager.register('Rover', Rover)
    manager = BaseManager()
    manager.start()

    rover = manager.Rover()

    manager = multiprocessing.Manager()
    process1 = multiprocessing.Process(target=startConnection, args=(rover,))
    process1.daemon = True
    process1.start()

    # process = multiprocessing.Process(target=uploadSensors, args=(rover,))
    # process.daemon = True
    # process.start()

    # process2 = multiprocessing.Process(target=artificial_intelligence, args=(rover,))
    # process2.daemon = True
    # process2.start()

    import logging
    logging.basicConfig(level=logging.DEBUG)

    try:
        while True:
            rover.uploadDataSensors()
            rover.sendMessage('data_sensors',rover.getAllDataJSON())
            # rover.testMotors()
            rover.execTask()
            time.sleep(0.1)
            pass
    except:
        logging.exception("Unexpected exception")
    finally:
        logging.info("Shutting down")
        for process in multiprocessing.active_children():
            logging.info("Shutting down process %r", process)
            process.terminate()
            process.join()
            exec(open("rover/stopMotors.py").read(), globals())
    logging.info("All done")
    # exec(open("rover/stopMotors.py").read(), globals())


if __name__ == '__main__':
    main()
