from connectionToGs import socket           # importa il modulo
import time
from random import random
groundStation= socket()                     # si connette automaticamente alla groundstation
print('Io sono il rover')
while True:
    print('\nCollegato: '+str(groundStation.isConnected))

    obj={"campo1":random(),                            # oggetto a caso
        "campo2":random(),
        "sensore1":random(),
        "sensore2":random()
        }
    if groundStation.isConnected:
        groundStation.sendData(obj)                 # esempio di sendData
    time.sleep(3)
groundStation.disconnect()                  # esempio di disconnect che sta fuori dal ciclo quindi non viene mai eseguito
