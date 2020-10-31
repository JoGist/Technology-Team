import RPi.GPIO as GPIO

class Ruota:

	self.__potenza = 0 #POTENZA (dutyCycle)
	
	def __init__(self, pinAvanti, pinIndietro):    
        GPIO.setmode(GPIO.BOARD)
        
        GPIO.setup(pinAvanti, GPIO.OUT)
        self.__avanti = GPIO.PWM(pinAvanti, 50)  #frequency=50Hz
        
        GPIO.setup(pinIndietro, GPIO.OUT)
        self.__indietro = GPIO.PWM(pinIndietro, 50)  #frequency=50Hz
    
    def start():
        self.__avanti.start(0)
        self.__indietro.start(0)
    
    def stop():
        self.__avanti.stop()
        self.__indietro.stop()
    
    
    def getPotenza():
        return __potenza
    
    def setPotenza(potenza):
        self.__potenza = potenza
        if(potenza > 0):
            self.__avanti.ChangeDutyCycle(potenza)
            self.__indietro.ChangeDutyCycle(0)
        elif(potenza < 0):
            self.__avanti.ChangeDutyCycle(0)
            self.__indietro.ChangeDutyCycle(potenza * (-1))
        else:
            self.__avanti.ChangeDutyCycle(0)
            self.__indietro.ChangeDutyCycle(0)
    
    
    def avanti(delta):
        setPotenza(self.__potenza + delta)
    
    # derivabile
    def indietro(delta):
        setPotenza(self.__potenza - delta)
        
    def cleanUp():
        GPIO.cleanup()
