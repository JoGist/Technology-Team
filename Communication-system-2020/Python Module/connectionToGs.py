import socketio             # unica libreria da installare tramite pip install "python-socketio[client]"
import json                 # è il modulo a gestire la conversione quindi JSON è necessario qui
rover = socketio.Client()   # un'istanza client

class socket:                                           # nome discutibile, si può sempre cambiare
    def __init__(self, ip, port):                       # è attraverso la init che il rover si connette
        rover.connect("http://"+ip+":"+str(port))
    def sendData(self, object ):                        # object è proprio un oggetto
        rover.emit("dataToGS",json.dumps(object))       # che viene convertito in JSON qui e inviato
    def disconnect(self):
        rover.disconnect()

    @rover.on('dataToRover')                            # gestisce l'evento dataToRover con la funzione dataToRover
    def dataToRover(data):                              # (non era necessario che avessero lo stesso nome)
        object= json.loads(data)                        # riconverte il JSON in oggetto
        print(object)                                   # qua dovrebbe starci la funzione che poi gestisce i dati
