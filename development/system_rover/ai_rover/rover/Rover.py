from sensors.Imu import Imu
from sensors.DistanceSensor import DistanceSensor
from actuators.Motors import Motors
from actuators.Pantilt import Pantilt
import json, math
from socketIO_client import SocketIO, LoggingNamespace
import time
import random

class Rover(): #constructor
    def __init__(self):
        self.typeTask = 1
        self.degree_target = 0
        self.pantilt_degree_target_x = 0
        self.pantilt_degree_target_y = 0
        self.theta = 0
        self.distances = []
        self.angles = []
        self.index = 0
        self.speed = 0
        self.speedLimit = 250
        #sensors libraries
        self.imu = Imu()
        self.distance_sensor = DistanceSensor()
        self.pantilt = Pantilt()
        self.motors = Motors()
        self.socketIO = SocketIO('localhost', 3001, LoggingNamespace)
        self.pantilt.setOrientation(0,0);

    #Start Sensors

    def uploadDataSensors(self):
        self.imu.uploadData()
        self.distance_sensor.uploadData()
    def getDataSensors(self):
        data_updated = self.imu.getData()
        data_updated['distance'] = self.distance_sensor.getData()
    def getDataSensorsJson(self):
        data_updated = self.imu.getData()
        data_updated['distance'] = self.distance_sensor.getData()
        jsonarray = json.dumps(data_updated)
        return jsonarray
    def getAllDataJSON(self):
        data_updated = self.imu.getData()
        data_updated['distance'] = self.distance_sensor.getData()
        data_updated['motors'] = self.motors.getSpeedMotors()
        data_updated['rotation_motors'] = self.motors.getRotationsMotors()
        jsonarray = json.dumps(data_updated)
        return jsonarray

    #End Sensors


    #Start Funcs

    def updateSpeedMotors(self):                                                #Updatesmotor's speed each time
        self.motors.setSpeedMotors(self.speed,self.speed,
                                        self.speed,self.speed)                  #it is executed
        self.motors.updateSpeedAllMotors()

    def getOrientation(self):                                                   #Compass function, returns the orientation
        fusionPose = self.imu.getData()['fusionPose'][2]
        #calibrazione bussola
        if fusionPose >= -3.14159/2:
            fusionPose = fusionPose - 3.14159/2
        else:
            fusionPose = fusionPose + 3.14159*3/2
        self.theta = math.degrees(fusionPose)
        return self.theta

    def decideTurn(self):
        speed1 = 120;
        speed2 = 160;
        if self.degree_target >= 0:
            if self.theta >= self.degree_target - 180 and self.theta < self.degree_target:
                self.motors.setTurnRight()
                if self.theta >= self.degree_target - 30:
                    self.speed = speed1
                else:
                    self.speed = speed2
            else:
                self.motors.setTurnLeft()
                if self.degree_target < 150 and self.theta <= self.degree_target + 30 and self.theta > self.degree_target:
                    self.speed = speed1
                elif self.degree_target > 150 and self.theta <= self.degree_target - 330:
                    self.speed = speed1
                elif self.degree_target > 150 and self.theta >= self.degree_target:
                    self.speed = speed1
                else:
                    self.speed = speed2
        else:
            if self.theta <= self.degree_target + 180 and self.theta > self.degree_target:
                self.motors.setTurnLeft()
                if self.theta <= self.degree_target + 30:
                    self.speed = speed1
                else:
                    self.speed = speed2
            else:
                self.motors.setTurnRight()
                if self.degree_target > -150 and self.theta >= self.degree_target - 30 and self.theta < self.degree_target:
                    self.speed = speed1
                elif self.degree_target < -150 and self.theta >= self.degree_target + 330:
                    self.speed = speed1
                elif self.degree_target < -150 and self.theta <= self.degree_target:
                    self.speed = speed1
                else:
                    self.speed = speed2
        print(str(self.degree_target)+", "+str(self.theta)+", "+str(self.speed))

    def reachedDegreeTarget(self):                                              #Returns true if the orietation is
        return (self.theta >= self.degree_target - 5  and                       #close to the degree target
                    self.theta <= self.degree_target + 5)

    def addAnglesandDist(self):                                                 #Creation of angles and ditances arrays
        self.angles.append(self.getOrientation())
        self.distances.append(self.imu.getData()['distance'])
        data_updated = {}
        data_updated['angle'] = self.getOrientation()
        data_updated['distance'] = self.distance_sensor.getData()
        jsonarray = json.dumps(data_updated)
        self.sendMessage('scan_distances_data_by_main',jsonarray)

    def saveDistandAngles(self):                                                #Saves angles.dat and distance.dat files
        thefile = open('distances.dat', 'w+')
        for item in self.distances:
            thefile.write("%s " % item)
        thefile = open('angles.dat', 'w+')
        for item in self.angles:
            thefile.write("%s " % item)

    #End Funcs


    #Start Tasks

    def init_TaskOnlyData(self):
        self.speed = 0
        self.motors.stopMotors()
        self.motors.setVelocity(self.speed)
    def execTaskOnlyData(self):
        self.motors.stopMotors()


    def init_TaskAzimutZero(self):
        self.theta = self.getOrientation()
        self.decideTurn()
        self.updateSpeedMotors()
    def execTaskAzimutZero(self):
        self.init_TaskAzimutZero()
        if self.reachedDegreeTarget():
            self.motors.stopMotors()
            self.typeTask = 1
        else:
            self.motors.updateSpeedAllMotors()
        #print(str(self.degree_target)+", "+str(self.theta)+", "+str(self.speed))


    def init_StartAndStop(self):
        self.motors.setForward()
        self.speed = 160
    def execStartAndStop(self):
        distance = self.imu.getData()['distance']
        # print('distance',distance,self.speed)
        if distance > 40:
            self.motors.setVelocity(self.speed)
        else:
            self.motors.stopMotors()


    def init_ScanDistances(self):
        self.degree_target = self.getOrientation()
        self.motors.setTurnRight()
        self.speed = 120
    def execScanDistances(self):
        self.updateSpeedMotors()
        self.addAnglesandDist()
        if (self.degree_target < 150 and self.index == 0 and
                self.getOrientation() >= self.degree_target + 30):
            self.index = 1
        elif (self.degree_target >= 150 and self.index == 0 and
                self.getOrientation() >= self.degree_target - 330):
            self.index = 1
        if (self.index == 1 and self.getOrientation() >=self.degree_target  and
                self.getOrientation() <= self.degree_target + 10):
            self.motors.stopMotors()
            self.saveDistandAngles()
            self.distances = []
            self.angles = []
            self.typeTask = 1
            self.index = 0


    def init_PantiltOrientation(self):
        l = 2 + 1

    def execPantiltOrientation(self):
        self.pantilt.setOrientation(self.pantilt_degree_target_x, self.pantilt_degree_target_y)
        self.typeTask = 1

    def init_PantitlFollowOrientation(self):
        self.theta = self.getOrientation()
    def execPantitlFollowOrientation(self):
        print('exetFollow')
        self.theta = self.getOrientation()
        pantilt_orientation = int(self.theta - self.degree_target)
        print(pantilt_orientation)
        self.pantilt.setOrientation(-pantilt_orientation,0);


    ''' junk function
    def init_YesOrNo(self):
        lol = 0
    def execYesOrNo(self):
        yon = random.random()
        if yon > 0.5:
            self.pantilt.setOrientation(0, 45)
            time.sleep(0.2)
            self.pantilt.setOrientation(0, -45)
            time.sleep(0.2)
            self.pantilt.setOrientation(0, 45)
            time.sleep(0.2)
            self.pantilt.setOrientation(0, -45)
            time.sleep(0.2)
            self.pantilt.setOrientation(0, 0)
        else:
            self.pantilt.setOrientation(-45, 0)
            time.sleep(0.2)
            self.pantilt.setOrientation(45, 0)
            time.sleep(0.2)
            self.pantilt.setOrientation(-45, 0)
            time.sleep(0.2)
            self.pantilt.setOrientation(45, 0)
            time.sleep(0.2)
            self.pantilt.setOrientation(0, 0)
        self.typeTask = 1

    def init_Yes(self):
        lol = 0
    def execYes(self):
        self.pantilt.setOrientation(0, 45)
        time.sleep(0.2)
        self.pantilt.setOrientation(0, -45)
        time.sleep(0.2)
        self.pantilt.setOrientation(0, 45)
        time.sleep(0.2)
        self.pantilt.setOrientation(0, -45)
        time.sleep(0.2)
        self.pantilt.setOrientation(0, 0)
        self.typeTask = 1
    def init_No(self):
        lol = 0
    def execNo(self):

        self.pantilt.setOrientation(-45, 0)
        time.sleep(0.2)
        self.pantilt.setOrientation(45, 0)
        time.sleep(0.2)
        self.pantilt.setOrientation(-45, 0)
        time.sleep(0.2)
        self.pantilt.setOrientation(45, 0)
        time.sleep(0.2)
        self.pantilt.setOrientation(0, 0)
        self.typeTask = 1
        '''

    def execTask(self):
        # print('task',self.typeTask)
        # if self.typeTask == 1:
        #     self.execTaskOnlyData()
        if self.typeTask == 2:
            self.execTaskAzimutZero()
        elif self.typeTask == 3:
            self.execStartAndStop()
        elif self.typeTask == 4:
            self.execScanDistances()
        elif self.typeTask == 5:
            self.execPantiltOrientation()
        elif self.typeTask == 6:
            self.execPantitlFollowOrientation()
        '''
        elif self.typeTask == 7:
            self.execYesOrNo()
        elif self.typeTask == 10:
            self.execYes()
        elif self.typeTask == 11:
            self.execNo()
        '''
    #End Tasks


    #Start Connection

    def on_connect(self, *args):
        print('connect')
    def on_disconnect(*args):
        print('disconnect')
    def on_reconnect(self, *args):
        print('reconnect')
    def on_aaa_response(self, *args):
        print('on_aaa_response', args)

        #data from ground station
    def on_task_response(self,*args):
        # print('task_rover',args)
        for arg in args:
            data = arg
        data  = json.loads(data)
        print(data['typeTask'])
        if data['typeTask'] == 'only_data':
            self.typeTask = 1
            self.init_TaskOnlyData()
            pass
        elif data['typeTask'] == 'azimut_zero':
            self.typeTask = 2
            self.degree_target = int(data['degree_target'])
            print(self.degree_target)
            self.init_TaskAzimutZero()
            pass
        elif data['typeTask'] == 'start_and_stop':
            self.typeTask = 3
            self.init_StartAndStop()
            pass
        elif data['typeTask'] == 'scan_distances':
            self.typeTask = 4
            self.init_ScanDistances()
            pass
        elif data['typeTask'] == 'pantilt_orientation':
            self.typeTask = 5
            self.pantilt_degree_target_x = int(data['pantilt_degree_target_x'])
            self.pantilt_degree_target_y = int(data['pantilt_degree_target_y'])
            self.init_PantiltOrientation()
            pass
        elif data['typeTask'] == 'pantilt_follow_orientation':
            self.typeTask = 6
            self.degree_target = int(data['degree_target'])
            self.init_PantitlFollowOrientation()
            pass
        elif data['typeTask'] == 'yes_or_no':
            self.typeTask = 7
            self.init_YesOrNo()
            pass
        elif data['typeTask'] == 'yes':
            self.typeTask = 10
            self.init_Yes()
            pass
        elif data['typeTask'] == 'no':
            self.typeTask = 11
            self.init_No()
            pass
        print('Task:',self.typeTask)

    def on_motors_response(self,*args):
        for arg in args:
            data = arg
        data  = json.loads(data)
        # print(data['command'])
        if data['command']=='stop':
            self.speed = 0
            self.motors.stopMotors()
            self.motors.setVelocity(self.speed)

        if data['command']=='up_arrow':
            if self.speed<self.speedLimit:
                self.speed = self.speed + 15;
                self.motors.setVelocity(self.speed)
        if data['command']=='down_arrow':
            if -self.speed>-self.speedLimit:
                self.speed = self.speed - 15;
                self.motors.setVelocity(self.speed)

        if data['command']=='left_arrow':
            if -self.speed>-self.speedLimit:
                self.speed = self.speed - 15;
                self.motors.setRotation(self.speed)
        if data['command']=='right_arrow':
            if self.speed<self.speedLimit:
                self.speed = self.speed + 15;
                self.motors.setRotation(self.speed)

    def on_bbb_response(*args):
        print('on_bbb_response', args)

    def start_connection(self):
        self.socketIO = SocketIO('localhost', 3001, LoggingNamespace)
        self.socketIO.on('connect', self.on_connect)
        self.socketIO.on('disconnect', self.on_disconnect)
        self.socketIO.on('reconnect', self.on_reconnect)
        self.socketIO.on('task_rover', self.on_task_response)
        self.socketIO.on('command', self.on_motors_response)

    def sendMessage(self,task,data):
        self.socketIO.emit(task, data, self.on_bbb_response)

    def wait_forever(self):
        self.socketIO.wait()

    #End Connection
