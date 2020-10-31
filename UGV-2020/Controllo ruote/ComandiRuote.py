class ComandiRuote:
	
    #self.__campionamento = 1 #ms
    self.__tempoSatAvanti = 5 #sec
    self.__tempoSatIndietro = 7 #sec
    self.__tempoSatFreno = 3 #sec
    self.__tempoSatSterzo = 10 #sec
    
    self.__deltaAvanti = 0
    self.__deltaIndietro = 0
    self.__deltaFreno = 0
    self.__deltaSterzo = 0
    
	def __init__(self, campionamento):
        self.__campionamento = campionamento #ms
        self.__delta = self.__campionamento / self.__tempoSaturazione # delta = costanteCampionamento (ms) / tempoSaturazione (sec)
    
    def getDeltaSatAvanti():
        return self.__deltaAvanti
    
    def setTempoSatAvanti(tempo):
        self.__tempoSatAvanti = tempo
        self.__deltaAvanti = self.__campionamento / tempo
    
    def getDeltaSatIndietro():
        return self.__deltaIndietro
    
    def setTempoSatIndietro(tempo):
        self.__tempoSatIndietro = tempo
        self.__deltaIndietro = self.__campionamento / tempo
    
    def getDeltaSatFreno():
        return self.__deltaFreno
    
    def setTempoSatFreno(tempo):
        self.__tempoSatFreno = tempo
        self.__deltaFreno = self.__campionamento / tempo
    
    def getDeltaSatSterzo():
        return self.__deltaSterzo
    
    def setTempoSatSterzo(tempo):
        self.__tempoSatSterzo = tempo
        self.__deltaSterzo = self.__campionamento / tempo
    
    
    