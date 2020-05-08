## Per funzionare bisogna impostare l'avvio automatico allo startup del programma main in python con PRIVILEGI D'AMMINISTRATORE altrimenti non sempre trova l'ip
from subprocess import PIPE, run
import socketio             # unica libreria da installare tramite pip install "python-socketio[client]"
import json                 # e' il modulo a gestire la conversione quindi JSON e' necessario qui
rover = socketio.Client()   # un'istanza client

class socket:                                           # nome discutibile, si puo' sempre cambiare
    def __init__(self):                                 # e' attraverso la init che il rover si connette
        ip = ""
        while ip == "":                                # ciclo che cerca l'ip della GS e si ferma solo quando ne trova una online
            cmd = "nmap -p3333 -T5 192.168.1.0-255 | grep open -B 4 | grep 192 | cut -c22-" # il comando magico che trova l'ip della GS: nmap è il software che scansiona la rete
            result = run([cmd], stdout=PIPE, stderr=PIPE, shell=True)                       # sulla porta 3333 in maniera aggressiva (T5). Il resto del comando si occupa di estrarre l'ip dal risultato di nmap
            ip=result.stdout.decode().strip("\n")
        port = 3333                                     # la porta che ci decideremo di impostare per le groundstation
        rover.connect("http://"+ip+":"+str(port))
    def sendData(self, object ):                        # object e' proprio un oggetto
        rover.emit("dataToGS",json.dumps(object))       # che viene convertito in JSON qui e inviato
    def disconnect(self):
        rover.disconnect()

    @rover.on('dataToRover')                            # gestisce l'evento dataToRover con la funzione dataToRover
    def dataToRover(data):                              # (non era necessario che avessero lo stesso nome)
        object= json.loads(data)                        # riconverte il JSON in oggetto
        print(object)                                   # qua dovrebbe starci la funzione che poi gestisce i dati
