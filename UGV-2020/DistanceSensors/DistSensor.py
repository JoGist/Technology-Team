import time
import threading
import RPi.GPIO as GPIO
class DistanceSensor():
    def __init__(self, pinTrig, pinEcho):
        self.trigger = pinTrig
        self.echo = pinEcho
        self.distance = -1
        self.pulsedelay = 0.0001
        self.samplingdelay = 0.06
        self.offset = 0
        self.extime = 0
        self.th_flag = 0
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger,GPIO.OUT)
        GPIO.setup(self.echo,GPIO.IN)

    def update(self):
        if(time.time()-self.extime>(self.samplingdelay)):
            timeout = time.time()
            GPIO.output(self.trigger, False)
            GPIO.output(self.trigger, True)
            time.sleep(self.pulsedelay)
            GPIO.output(self.trigger, False)
            #conteggio del tempo iniziale e finale
            try:
                while (GPIO.input(self.echo)==0):
                    if(time.time()-timeout>0.012):
                        break
                    pass
                t_start = time.time()
                while (GPIO.input(self.echo)==1):
                    if(time.time()-timeout>0.012):
                        break
                    pass
                t_end = time.time()

                t_elapsed = t_end - t_start               #calcolo del tempo trascorso
                dist = t_elapsed * 100 * 340/2           #calcolo della distanza

                #se il valore della distanza e' compreso tra 2 e 400 porlo in distance considando anche l'offset
                if(dist>2 and dist<400):
                  self.distance = dist+self.offset
                  #se il valore della distanza non e' compreso tra 2 e 400 porre distance pari a -1
                else:
                  self.distance = -1

            except:
                print("Qualcosa e' andato storto")
            self.extime=time.time()


    def run(self):
        x = threading.Thread(target=self.thread, args=())
        x.start()
    #aggiornamento continuo della distanza
    def thread(self):
        while True:
            self.update()
            if(self.th_flag==1):
                self.th_flag = 0
                exit(0)

    def killthread(self):                            #blocca il thread
        self.th_flag = 1

    def getdistance(self):                           #restituisce il valore della distanza
        return self.distance
