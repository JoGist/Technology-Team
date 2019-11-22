import multiprocessing
import socket

def handle(connection, address, imu, distance, distance2):
    # import logging
    # logging.basicConfig(level=logging.DEBUG)
    # logger = logging.getLogger("process-%r" % (address,))
    try:
        # logger.debug("Connected %r at %r", connection, address)
        while True:
            data = connection.recv(1024)
            if (data == '' or not data):
                # logger.debug("Socket closed remotely")
                break
            # logger.debug("Received data %r", data)
            connection.sendall(data)
            # logger.debug("Sent data")
    except:
        # logger.exception("Problem handling request")
    finally:
        # logger.debug("Closing socket")
        connection.close()

class Server(object):
    def __init__(self, hostname, port, imu, distance_sensor, distance2_sensor):
        import logging
        self.logger = logging.getLogger("server")
        self.hostname = hostname
        self.port = port
        self.imu = imu
        self.distance_sensor = distance_sensor
        self.distance2_sensor = distance2_sensor

    def start(self):
        self.logger.debug("listening")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.hostname, self.port))
        self.socket.listen(1)

        while True:
            conn, address = self.socket.accept()
            self.logger.debug("Got connection")
            process = multiprocessing.Process(target=handle, args=(conn, address, imu, distance_sensor, distance2_sensor))
            process.daemon = True
            process.start()
            self.logger.debug("Started process %r", process)
