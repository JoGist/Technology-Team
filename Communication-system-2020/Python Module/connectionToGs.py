## Per funzionare bisogna impostare l'avvio automatico allo startup del programma main in python con PRIVILEGI D'AMMINISTRATORE altrimenti non sempre trova l'ip
import threading            # serve per far funzionare in background la ricerca della groundstation
import time                 # serve per creare un timer di pochi secondi dopo ogini scansione della rete per non appensantire
import socketio             # libreria da installare tramite pip install "python-socketio[client]"
import json                 # e' il modulo a gestire la conversione quindi JSON e' necessario qui
import nmap                 # libreria da installare tramite pip install python-nmap

class socket:                                               # nome discutibile, si puo' sempre cambiare
    def __init__(self):                                     # e' attraverso la init che il rover si connette
        rover = socketio.Client()                           # un'istanza client di Socket.io
        nm=nmap.PortScanner()
        self.isConnected = False                            # di default non c'è connessione
        thread = threading.Thread(target=self.connectThread, args=[nm, rover])          # scelta della funzione che verrà eseguita in background
        thread.start()                                      # avvio del thread
        @rover.on('dataToRover')                            # gestisce l'evento dataToRover con la funzione dataToRover
        def dataToRover(data):                              # (non era necessario che avessero lo stesso nome)
            object= json.loads(data)                        # riconverte il JSON in oggetto
            print(object)                                   # qua dovrebbe starci la funzione che poi gestisce i dati
        @rover.on('disconnect')                             # gestisce la disconnessione della grounstation
        def onDisconnect():
            rover.disconnect()                              # se non si chiude il socket alla successiva riconessione della GS si riconnetterà
            self.isConnected = False                        # automaticamente in modi imprevedibili, quindi meglio che ce la gestiamo noi
            restartThread = threading.Thread(target=self.connectThread, args=[nm, rover])   # sono costretto a definire un altro thread per regole oscure di python
            restartThread.start()

    def sendData(self, object ):                        # object e' proprio un oggetto
        rover.emit("dataToGS",json.dumps(object))       # che viene convertito in JSON qui e inviato
    def disconnect(self):
        rover.disconnect()

    def connectThread(self, nm, rover):                             # funzione che cerca l'ip
        port=3333                                                   # che ha la porta scelta aperta
        while not self.isConnected:
            scan=nm.scan("192.168.1.0-255",str(port),arguments='-T5')  # il comando magico che trova l'ip della GS: nmap è il software che scansiona la rete
            for ip in scan['scan'].keys():                          # sulla porta scelta in maniera aggressiva (T5)
                if scan['scan'][ip]['tcp'][port]['state']=='open':  # il risultato è un oggetto dove da qualche parte c'è l'ip con la porta aperta scelta
                    rover.connect("http://"+ip+":"+str(port))
                    self.isConnected=True
            time.sleep(2)                                           # pausa tra una scansione e l'altra
