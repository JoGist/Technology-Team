class ControlloreRuote:
    
    antDx = Ruota(1,2)
    antSx = Ruota(3,4)
    posDx = Ruota(5,6)
    posSx = Ruota(7,8)
    
    def __init__(self):

    def accensione():
        antDx.start()
        antSx.start()
        posDx.start()
        posSx.start()
        
    def spegnimento():
        antDx.stop()
        antSx.stop()
        posDx.stop()
        posSx.stop()
    
    
    def giraADestra(delta):
        antDx.indietro(delta)
        antSx.avanti(delta)
        posDx.indietro(delta)
        posSx.avanti(delta)
    
    def accelera(delta):
        antDx.avanti(delta)
        antSx.avanti(delta)
        posDx.avanti(delta)
        posSx.avanti(delta)
    
    # derivabile
    def decelera(delta):
        antDx.indietro(delta)
        antSx.indietro(delta)
        posDx.indietro(delta)
        posSx.indietro(delta)
    
    def frenoAMano():
        

    def avantiCostante(potenza):
        antDx.setPotenza(potenza)
        antSx.setPotenza(potenza)
        posDx.setPotenza(potenza)
        posSx.setPotenza(potenza)
    
    # derivabile
    def indietroCostante(potenza):
        antDx.setPotenza(-potenza)
        antSx.setPotenza(-potenza)
        posDx.setPotenza(-potenza)
        posSx.setPotenza(-potenza)    
    
    def giraInSensoOrarioDaFermoCostante(potenza):
        antDx.setPotenza(-potenza)
        antSx.setPotenza(potenza)
        posDx.setPotenza(-potenza)
        posSx.setPotenza(potenza)
    
    # derivabile
    def giraInSensoAntiOrarioDaFermoCostante(potenza):
        antDx.setPotenza(potenza)
        antSx.setPotenza(-potenza)
        posDx.setPotenza(potenza)
        posSx.setPotenza(-potenza)
        
    def cleanUp():
        antDx.cleanUp()
        antSx.cleanUp()
        posDx.cleanUp()
        posSx.cleanUp()