import random
import numpy as np
from copy import deepcopy

def tablero_inicial():
    t0 = []
    for i in range(0,24):
        palo = []
        if (i==0):
            palo = ['N','N']
        elif (i==5):
            palo = ['B','B','B','B','B']
        elif (i==7):
            palo = ['B','B','B']
        elif (i==11):
            palo = ['N','N','N','N','N']
        elif (i==12):
            palo = ['B','B','B','B','B']
        elif (i==16):
            palo = ['N','N','N']
        elif (i==18):
            palo = ['N','N','N','N','N']
        elif (i==23):
            palo = ['B','B']
        t0 += [palo]
    return t0
    
class Partida:
    def __init__(self):
        self.tablero = tablero_inicial()
        self.barraN = []
        self.barraB = []
        self.puntosN = 0
        self.puntosB = 0
        self.turno = None
        
    def turno_inicial(self):
        dadoN = random.choice([1,2,3,4,5,6])
        dadoB = random.choice([1,2,3,4,5,6])
        if (dadoN<dadoB):
            self.turno = 'B'
            return (dadoN,dadoB)
        elif (dadoB<dadoN):
            self.turno = 'N'
            return (dadoN,dadoB)
        else:
            self.turno_inicial()
    
    def tirar_dados(self):
        dado1 = random.choice([1,2,3,4,5,6])
        dado2 = random.choice([1,2,3,4,5,6])
        return (dado1,dado2)
    
    def es_posible(self,num_palo):
        es_posible = False
        if (0<=num_palo<=23):
            turno = self.turno
            palo = self.tablero[num_palo]
            if ((len(palo)==0) or (palo[0]==turno) or (len(palo)==1)):
                es_posible = True
        return es_posible
    
    def barra_turno(self,turno):
        if (turno=='N'):
            barra = self.barraN
        else:
            barra = self.barraB
        return barra
    
    def movimiento(self,partida,dado):
        turno = self.turno
        barra = self.barra_turno(turno)
        movimientos = []
        if (len(barra)==0):
            for p in range(0,24):
                if (len(partida.tablero[p])!=0 and partida.tablero[p][0]==turno and partida.es_posible(p+dado)):
                    movimientos.append((p,dado))
        else:
            if (partida.es_posible(dado)):
                movimientos.append((-1,dado))
        return movimientos
        
    def jugadas_legales(self,dado1,dado2): #Añadir el caso de que ambos dados sean iguales y los casos con todas las fichas en el final ya
        turno = self.turno
        partida = deepcopy(self)
        if (turno=='N'):
            rival = 'B'
        else:
            rival = 'N'
        jugadas_legales = []
        primer_movimiento = (self.movimiento(partida,dado1))+(self.movimiento(partida,dado2))
        for primera in primer_movimiento:
            partida = deepcopy(self)
            if (primera[1]==dado1):
                dado = dado2
            else:
                dado = dado1
            if (primera[0]==-1):
                (partida.barra_turno(turno)).remove(turno)
            posicion = primera[0]+primera[1]
            if (len(partida.tablero[posicion])>0 and partida.tablero[posicion]!=turno):
                (partida.barra_turno(rival)).append(rival)
                partida.tablero[posicion] = []
            (partida.tablero[posicion]).append(turno)
            segundo_movimiento = partida.movimiento(partida,dado)
            for segunda in segundo_movimiento:
                jugada = (primera,segunda)
                jugadas_legales.append(jugada)
        return jugadas_legales
                
        