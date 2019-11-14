from socketIO_client import SocketIO, LoggingNamespace

class Connection():
    def __init__(self):
        self.socketIO = SocketIO('localhost', 3001, LoggingNamespace)
        # self.socketIO
        # self.socketIO = SocketIO('localhost', 3001, LoggingNamespace)
        # self.socketIO.on('connect', on_connect)
        # self.socketIO.on('disconnect', on_disconnect)
        # self.socketIO.on('reconnect', self.on_reconnect)
        #
        # self.socketIO.on('news', self.on_news_response)


    def on_connect(*args):
        print('connect')

    def on_disconnect(*args):
        print('disconnect')

    def on_reconnect(*args):
        print('reconnect')

    def on_aaa_response(*args):
        print('on_aaa_response', args)

    def on_task_response(*args):
        print('task_rover',args)

    def on_bbb_response(*args):
        print('on_bbb_response', args)


    def start(self,rover,task_rover):
        self.socketIO = SocketIO('localhost', 3001, LoggingNamespace)
        self.socketIO.on('connect', self.on_connect)
        self.socketIO.on('disconnect', self.on_disconnect)
        self.socketIO.on('reconnect', self.on_reconnect)
        self.rover = rover
        self.socketIO.on('task_rover', task_rover, self.rover)

    def sendMessage(self,task,data):
        self.socketIO.emit(task, data, self.on_bbb_response)

    def wait_forever(self):
        self.socketIO.wait()
