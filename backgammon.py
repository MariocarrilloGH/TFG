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
    
    def es_final(self):
        es_final = (self.puntosN==15 or self.puntosB==15)
        return es_final
    
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
    
    def puedes_sacar(self):
        turno = self.turno
        barra = self.barra_turno(turno)
        puedes_sacar = True
        if (len(barra)>0):
            puedes_sacar = False
        else:
            if (turno=='N'):
                l_i = 0
                l_s = 18
            else:
                l_i = 6
                l_s = 24
            for i in range(l_i,l_s):
                if turno in self.tablero[i]:
                    puedes_sacar = False
        return puedes_sacar
    
    def movimiento(self,partida,dado):
        turno = self.turno
        barra = self.barra_turno(turno)
        movimientos = []
        if (len(barra)==0):
            for p in range(0,24):
                if ((len(partida.tablero[p])!=0 and partida.tablero[p][0]==turno and partida.es_posible(p+dado)) or (p+dado>=24 and partida.puedes_sacar())):
                    movimientos.append((p,dado))
        else:
            if (partida.es_posible(dado)):
                movimientos.append((-1,dado))
        return movimientos
        
    def jugadas_legales(self,dado1,dado2):
        turno = self.turno
        partida = deepcopy(self)
        if (turno=='N'):
            rival = 'B'
        else:
            rival = 'N'
        jugadas_legales = []
        if (dado1!=dado2):
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
                if (len(partida.tablero[posicion])==1 and partida.tablero[posicion]==rival):
                    (partida.barra_turno(rival)).append(rival)
                    partida.tablero[posicion] = []
                (partida.tablero[posicion]).append(turno)
                segundo_movimiento = partida.movimiento(partida,dado)
                for segunda in segundo_movimiento:
                    jugada = (primera,segunda)
                    jugadas_legales.append(jugada)
        else:
            dado = dado1
            primer_movimiento = self.movimiento(partida,dado)
            for primera in primer_movimiento:
                partida = deepcopy(self)
                if (primera[0]==-1):
                    (partida.barra_turno(turno)).remove(turno)
                posicion = primera[0]+dado
                if (len(partida.tablero[posicion])==1 and partida.tablero[posicion]==rival):
                    (partida.barra_turno(rival)).append(rival)
                    partida.tablero[posicion] = []
                (partida.tablero[posicion]).append(turno)
                segundo_movimiento = partida.movimiento(partida,dado)
                for segunda in segundo_movimiento:
                    partida = deepcopy(partida)
                    if (primera[0]==-1):
                        (partida.barra_turno(turno)).remove(turno)
                    posicion = primera[0]+dado
                    if (len(partida.tablero[posicion])==1 and partida.tablero[posicion]==rival):
                        (partida.barra_turno(rival)).append(rival)
                        partida.tablero[posicion] = []
                    (partida.tablero[posicion]).append(turno)
                    tercer_movimiento = partida.movimiento(partida,dado)
                    for tercera in tercer_movimiento:
                        partida = deepcopy(self)
                        if (primera[0]==-1):
                            (partida.barra_turno(turno)).remove(turno)
                        posicion = primera[0]+dado
                        if (len(partida.tablero[posicion])==1 and partida.tablero[posicion]==rival):
                            (partida.barra_turno(rival)).append(rival)
                            partida.tablero[posicion] = []
                        (partida.tablero[posicion]).append(turno)
                        cuarto_movimiento = partida.movimiento(partida,dado)
                        for cuarta in cuarto_movimiento:
                            jugada = (primera,segunda,tercera,cuarta)
                            jugadas_legales.append(jugada)
        return jugadas_legales
                
    def jugada(self,jugada,dado1,dado2):
        jugadas_legales = self.jugadas_legales(dado1,dado2)
        if jugada in jugadas_legales:
            turno = self.turno
            if (turno=='N'):
                rival = 'B'
            else:
                rival = 'N'
            for movimiento in jugada:
                ficha = movimiento[0]
                dado = movimiento[1] 
                posicion = ficha+dado
                if (posicion>=24):
                    (self.tablero[ficha]).remove(turno)
                    if (turno=='N'):
                        self.puntosN = self.puntosN + 1
                    else:
                        self.puntosB = self.puntosB + 1
                else:
                    if (ficha==-1):
                        (self.barra_turno(turno)).remove(turno)
                    else:
                        (self.tablero[ficha]).remove(turno)
                    if (len(self.tablero[posicion])==1 and self.tablero[posicion]==rival):
                        (self.barra_turno(rival)).append(rival)
                        self.tablero[posicion] = []
                    (self.tablero[posicion]).append(turno)
            if (self.turno=='N'):
                self.turno = 'B'
            else:
                self.turno = 'N'
        else:
            print("Jugada ilegal")
        
class Arbol_juego:
    def __init__(self,partida):
        self.hijos = []
        self.partida = partida
        self.evaluacion = None
        