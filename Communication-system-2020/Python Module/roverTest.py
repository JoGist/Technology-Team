from connectionToGs import socket           # importa il modulo
import time
groundStation= socket()                     # si connette automaticamente alla groundstation
while True:
    print('collegato: '+str(groundStation.isConnected))

    obj={"campo1":0,                            # oggetto a caso
        "campo2":2,
        "sensore1":2.032,
        "sensore2":20147
        }

    if groundStation.isConnected:
        groundStation.sendData(obj)                 # esempio di sendData
    time.sleep(2)
groundStation.disconnect()                  # esempio di disconnect
