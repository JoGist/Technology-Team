from connectionToGs import socket           # importa il modulo

groundStation= socket("localhost",3000)     # di fatto esegue la init passandogli ip e porta

obj={"campo1":0,                            # oggetto a caso
    "campo2":2,
    "sensore1":2.032,
    "sensore2":20147
    }

groundStation.sendData(obj)                 # esempio di sendData
groundStation.disconnect()                  # esempio di disconnect
