from DistSensor import *
import threading
import time
#definisco una classe in grado di gestire piu' sensori ad ultrasuoni
class SensorsCluster():
    #per evitare il conflitto tra sensori devono essere usati singolarmente
    #priority quindi definisce la priorita' dei sensori, piu' questa e' vicina
    #a zero e piu velocemente le misure saranno effettuate
    #va modificato il valore iniziale dei pri_temp(in modo casuale) oppure tutti
    #verranno eseguiti insieme rallentando anche i sensori ad alta priorita'
    #formato dati sensorlist ((trig1,echo1),(trig2,echo2),...)
    def __init__(self, sensorlist):
        try:
            #intervallo sicuro di non interferenza
            self.safedelay = 0.06 #60ms
            #numero sensori
            self.num = len(sensorlist)
            #array priorita', ogni sensore ha un valore
            self.priority = [1 for i in range(self.num)]
            #coda temporanea di esecuzione
            self.pri_temp = [1 for i in range(self.num)]
            #variabile di stop del thread
            self.th_flag = 0
            #dichiaro un array di oggetti pari al numero di sensori con la classe DistanceSensor
            self.sensor = [DistanceSensor(sensorlist[i][0],sensorlist[i][1]) for i in range(self.num) ]
            #da fare la verifica della dimensione di sensorlist

        except:
            print("Errore di inizializzazione")

    #aggiorna le priorita' di aggiornamento dei sensori
    def pri_update(self, pri_array):
        if(len(pri_array) == self.num):
            self.priority = pri_array.copy()
            self.queue_setup()
        else:
            print("Errore di dimensionamento pri_array")

    #seleziona i prossimi sensori da misurare
    def queue_update(self):
        for i in range(self.num):
            if(self.pri_temp[i] > 0):
                self.pri_temp[i]-=1
            else:
                self.pri_temp[i] = self.priority[i]
            #decrementa il valore di ogni valore di pri_temp a meno che
            #questo sia minore o uguale a 0
    def queue_setup(self):
        temp_array = []
        for i in self.priority:
            if i not in temp_array:
                temp_array.append(i)
        temp_array.sort()
        for elem in temp_array:
            count = 0
            for i in range(self.num):
                if(self.pri_temp[i] == elem):
                    self.pri_temp[i] = (elem + count)%(self.priority[i]+1)
                    count+=1


    #se la pri_temp = 0 nel sensore allora puo' essere misurato e resettata la priorita'
    def exec_queue(self):
        for i in range(self.num):
            if(self.pri_temp[i] == 0):
                #misura sensore i
                self.sensor[i].update()
                #evita il conflitto
                time.sleep(self.safedelay)

    #aggiorna la coda dei sensori ed esegue la misura (thread main)
    def autoupdate(self):
        while 1:
            self.queue_update()
            self.exec_queue()
            if(self.th_flag==1):
                self.th_flag = 0
                exit(0)

    #blocca il thread
    def stop(self):
        #self.th_flag e' la variabile condivisa con il thread che viene controllata
        self.th_flag = 1

    #fa partire il thread
    def run(self):
        x = threading.Thread(target=self.autoupdate, args=())
        x.start()
