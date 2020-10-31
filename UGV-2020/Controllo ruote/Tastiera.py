#numeroCampioni = tempoSaturazione / costanteCampionamento
#delta = costanteCampionamento (ms) / tempoSaturazione (sec)

from threading import Thread
import time

class Tastiera:
	
	__CAMPIONAMENTO = 1 #ms
    
    controlloRuote = ControlloRuote()
    
    actions = {
        curses.KEY_UP:    controlloRuote.accelera(,
        curses.KEY_DOWN:  controlloRuote.decelera(,
        curses.KEY_LEFT:  controlloRuote.giraADestra(,
        curses.KEY_RIGHT: controlloRuote.giraASinistra(,
        curses.KEY_F:     controlloRuote.frenoAMano(,
    }
    
    def __up():
        controlloRuote.g
    
    def __init__(self):
        self.__numeroCampioni = 1000 / __CAMPIONAMENTO # numero campioni in un secondo
        thread = threading.Thread(target=thread_function, args=())
        thread.start()
        
    def thread_function():
        #input da tastiera, campionamwento a __CAMPIONAMENTO
    