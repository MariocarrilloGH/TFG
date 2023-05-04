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
    def __init__(self,turno=None):
        self.tablero = tablero_inicial()
        self.barraN = []
        self.barraB = []
        self.puntosN = 0
        self.puntosB = 0
        self.turno = turno
        
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
    
    def movimiento(self,dado):
        turno = self.turno
        barra = self.barra_turno(turno)
        if (turno=='B'):
            dado = (-1)*dado
        movimientos = []
        if (len(barra)==0):
            for p in range(0,24):
                if ((len(self.tablero[p])!=0 and self.tablero[p][0]==turno and self.es_posible(p+dado)) or (p+dado>=24 and self.puedes_sacar())):
                    movimientos.append((p,abs(dado)))
        else:
            if (self.es_posible(dado-1) and turno=='N'):
                movimientos.append((-1,abs(dado)))
            if (self.es_posible(24+dado) and turno=='B'):
                movimientos.append((24,abs(dado)))
        return movimientos
    
    def jugadas_legales(self,dado1,dado2):
        turno = self.turno
        partida = deepcopy(self)
        if (turno=='N'):
            rival = 'B'
        else:
            rival = 'N'
        jugadas_legales = []
        primer_movimiento = (self.movimiento(dado1))+(self.movimiento(dado2))
        for primera in primer_movimiento:
            partida = deepcopy(self)
            if (primera[1]==dado1):
                dado = dado2
            else:
                dado = dado1
            if (turno=='N'):
                posicion = primera[0]+primera[1]
            else:
                posicion = primera[0]-primera[1]
            if (primera[0]==-1 or primera[0]==24):
                (partida.barra_turno(turno)).remove(turno)
            else:
                (partida.tablero[primera[0]]).remove(turno)
            if (len(partida.tablero[posicion])==1 and (rival in partida.tablero[posicion])):
                (partida.barra_turno(rival)).append(rival)
                partida.tablero[posicion] = []
            if (0<=posicion<=23):
                (partida.tablero[posicion]).append(turno)
            segundo_movimiento = partida.movimiento(dado)
            for segunda in segundo_movimiento:
                jugada = (primera,segunda)
                jugadas_legales.append(jugada)
        """else: #Regla de que si los dos dados son iguales se duplican los dados
            dado = dado1
            primer_movimiento = partida.movimiento(dado)
            for primera in primer_movimiento:
                partida1 = deepcopy(self)
                if (turno=='N'):
                    posicion = primera[0]+dado
                else:
                    posicion = primera[0]-dado
                if (primera[0]==-1 or primera[0]==24):
                    (partida1.barra_turno(turno)).remove(turno)
                else:
                    (partida1.tablero[primera[0]]).remove(turno)
                if (len(partida1.tablero[posicion])==1 and (rival in partida1.tablero[posicion])):
                    (partida1.barra_turno(rival)).append(rival)
                    partida1.tablero[posicion] = []
                if (0<=posicion<=23):
                    (partida1.tablero[posicion]).append(turno)
                segundo_movimiento = partida1.movimiento(dado)
                for segunda in segundo_movimiento:
                    partida2 = deepcopy(partida1)
                    if (turno=='N'):
                        posicion = segunda[0]+dado
                    else:
                        posicion = segunda[0]-dado
                    if (segunda[0]==-1 or segunda[0]==24):
                        (partida2.barra_turno(turno)).remove(turno)
                    else:
                        (partida2.tablero[segunda[0]]).remove(turno)
                    if (len(partida2.tablero[posicion])==1 and (rival in partida2.tablero[posicion])):
                        (partida2.barra_turno(rival)).append(rival)
                        partida2.tablero[posicion] = []
                    if (0<=posicion<=23):
                        (partida2.tablero[posicion]).append(turno)
                    tercer_movimiento = partida2.movimiento(dado)
                    for tercera in tercer_movimiento:
                        partida3 = deepcopy(partida2)
                        if (turno=='N'):
                            posicion = tercera[0]+dado
                        else:
                            posicion = tercera[0]-dado
                        if (tercera[0]==-1 or tercera[0]==24):
                            (partida3.barra_turno(turno)).remove(turno)
                        else:
                            (partida3.tablero[tercera[0]]).remove(turno)
                        if (len(partida3.tablero[posicion])==1 and (rival in partida3.tablero[posicion])):
                            (partida3.barra_turno(rival)).append(rival)
                            partida3.tablero[posicion] = []
                        if (0<=posicion<=23):
                            (partida3.tablero[posicion]).append(turno)
                        cuarto_movimiento = partida3.movimiento(dado)
                        for cuarta in cuarto_movimiento:
                            jugada = (primera,segunda,tercera,cuarta)
                            jugadas_legales.append(jugada)"""
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
                if (turno=='N'):
                    posicion = ficha+dado
                else:
                    posicion = ficha-dado
                if (posicion>=24 or posicion<=-1):
                    (self.tablero[ficha]).remove(turno)
                    if (turno=='N'):
                        self.puntosN = self.puntosN+1
                    else:
                        self.puntosB = self.puntosB+1
                else:
                    if (ficha==-1 or ficha==24):
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
            
    def heuristica(self,jugador):
        pasos_negras = len(self.barra_turno('N'))*25
        pasos_blancas = len(self.barra_turno('B'))*25
        for i in range(0,24):
            if (len(self.tablero[i])!=0):
                if (self.tablero[i][0]=='N'):
                    pasos_negras = len(self.tablero[i])*(24-i)
                else:
                    pasos_blancas = len(self.tablero[i])*(i+1)
        if (jugador=='N'):
            puntos = pasos_blancas-pasos_negras
        else:
            puntos = pasos_negras-pasos_blancas
        if (not self.es_final() or puntos==0):
            return puntos
        else:
            return (np.sign(puntos)*np.inf)
        return puntos
        
    def imprimir_tablero(self):
        if (len(self.barraN)<10):
            bN = ' ' + str(len(self.barraN))
        else:
            bN = str(len(self.barraN))
        sol = " 12  11  10   9   8   7 | " + bN + " N |  6   5   4   3   2   1 \n"
        sol = sol + "------------------------+------+-------------------------\n"
        flags1 = [False,False,False,False,False,False,False,False,False,False,False,False]
        for j in range(0,5):
            linea = ""
            for i in range(0,12):
                if (j<len(self.tablero[i])<=5):
                    linea = "  " + (self.tablero[i][j]) + " " + linea
                elif(len(self.tablero[i])<=5 or flags1[i]):
                    linea = "    " + linea
                else:
                    flags1[i] = True
                    if (len(self.tablero[i])<10):
                        num = ' ' + str(len(self.tablero[i]))
                    else:
                        num = str(len(self.tablero[i]))
                    linea = num + (self.tablero[i][j]) + " " + linea
                if (i==5):
                    linea = "|      |" + linea
            sol = sol + linea + "\n"
        sol = sol + "------------------------+------+-------------------------\n"
        flags2 = [False,False,False,False,False,False,False,False,False,False,False,False]
        for j in range(4,-1,-1):
            linea = ""
            for i in range(12,24):
                if (j<len(self.tablero[i])<=5):
                    linea = linea + "  " + (self.tablero[i][j]) + " "
                elif(len(self.tablero[i])<=5 or flags2[i]):
                    linea = linea + "    "
                else:
                    flags2[i] = True
                    if (len(self.tablero[i])<10):
                        num = ' ' + str(len(self.tablero[i]))
                    else:
                        num = str(len(self.tablero[i]))
                    linea = linea + num + (self.tablero[i][j]) + " "
                if (i==17):
                    linea = linea + "|      |"
            sol = sol + linea + "\n"
        sol = sol + "------------------------+------+-------------------------\n"
        if (len(self.barraN)<10):
            bB = ' ' + str(len(self.barraB))
        else:
            bB = str(len(self.barraB))
        sol = sol + " 13  14  15  16  17  18 | " + bB + " B | 19  20  21  22  23  24 "
        print(sol)
        
    def jugar(self,turno,algoritmo,profundidad,iteraciones):
        self.imprimir_tablero()
        if (turno==1):
            jugador = 'N'
        else:
            jugador = 'B'
        aj = Arbol_juego(self)
        (dado1,dado2) = self.turno_inicial()
        print(f'Empieza el jugador {self.turno}')
        while (not self.es_final()):
            print(f'Dado 1: {dado1} | Dado 2: {dado2}')
            jugadas_legales = self.jugadas_legales(dado1,dado2)
            (dado1,dado2) = self.tirar_dados()
            if (not bool(jugadas_legales)):
                if (self.turno=='N'):
                    self.turno = 'B'
                else:
                    self.turno = 'N'
                aj.llenar_nivel() #Esto tengo que revisarlo
                aj = aj.hijos[0][0] 
            else:
                if (self.turno==jugador):
                    ficha1 = int(input("Introduzca la ficha que quiere mover con el dado 1 (1-24): "))
                    ficha2 = int(input("Introduzca la ficha que quiere mover con el dado 2 (1-24): "))
                    if ((ficha1 in range(1,25)) and (ficha2 in range(1,25))):
                        jugada = ((ficha1,dado1),(ficha2,dado2))        
                        if (jugada in jugadas_legales):
                            self.jugada(jugada,dado1,dado2)
                            aj.llenar_nivel() #Esto tengo que revisarlo
                            for hijo in aj.hijos:
                                if (hijo[1]==jugada):
                                    aj = hijo[0]
                                    break
                            self.imprimir_tablero()
                        else:
                            print("Jugada ilegal")
                            self.imprimir_tablero()
                else:
                    print("\nTurno de la maquina")
                    aj, jugada = self.decision_maquina(aj,algoritmo,profundidad,iteraciones)
                    self.jugada(jugada,dado1,dado2)
                    self.imprimir_tablero()      
        final = self.heuristica(jugador)
        if (final!=0):
            if (final==np.inf):
                print("\nHas ganado")
            else:
                print("\nHas perdido")
        else:
            print("\nHas empatado")
    
class Arbol_juego:
    def __init__(self,partida):
        self.hijos = []
        self.partida = partida
        self.evaluacion = None
        self.random = False
        
    def anadir_hijo(self,hijo,jugada):
        (self.hijos).append((hijo,jugada))

    def imprimir_hijos(self):
        for hijo in (self.hijos):
            print(hijo[1])
            (hijo[0].partida).imprimir_tablero()
                
    def llenar_nivel(self):
        if (len(self.hijos)==0):
            combinaciones = [(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(2,2),(2,3),(2,4),(2,5),(2,6),(3,3),(3,4),(3,5),(3,6),(4,4),(4,5),(4,6),(5,5),(5,6),(6,6)]
            for combinacion in combinaciones:
                p = deepcopy(self.partida)
                aj = Arbol_juego(p)
                aj.random = True
                (self.hijos).append((aj,combinacion))
            for hijo in self.hijos:
                dado1 = hijo[1][0]
                dado2 = hijo[1][1]
                jugadas_legales = (self.partida).jugadas_legales(dado1,dado2)
                if (len(jugadas_legales)==0):
                    p = deepcopy(self.partida)
                    if ((p.partida).turno=='N'):
                        (p.partida).turno = 'B'
                    else:
                        (p.partida).turno = 'N'
                    aj = Arbol_juego(p)
                    hijo[0].anadir_hijo(aj,None)
                else:
                    for jugada in jugadas_legales:
                        dado1 = jugada[0][1]
                        dado2 = jugada[1][1]
                        p = deepcopy(self.partida)
                        p.jugada(jugada,dado1,dado2)
                        aj = Arbol_juego(p)
                        hijo[0].anadir_hijo(aj,jugada)
                    
    def expectiminimax(self,profundidad,etiqueta):
        if (etiqueta=="max"):
            jugador = (self.partida).turno
        else:
            jugador = 'N'
            if ((self.partida).turno=='N'):
                jugador = 'B'
        if (profundidad==0 or (self.partida).es_final()):
            self.evaluacion = (self.partida).heuristica(jugador)
        else:
            if (not self.random):
                if (etiqueta=="max"):
                    valor = -np.inf
                    self.llenar_nivel()
                    for hijo in self.hijos:
                        (hijo[0]).expectiminimax(profundidad-1,"min")
                        m = (hijo[0]).evaluacion
                        valor = max(valor,m)
                    self.evaluacion = valor
                else:
                    valor = np.inf
                    self.llenar_nivel()
                    for hijo in self.hijos:
                        (hijo[0]).expectiminimax(profundidad-1,"max")
                        m = (hijo[0]).evaluacion
                        valor = min(valor,m)
                    self.evaluacion = valor
            else:
                valor = 0
                for hijo in self.hijos:
                    (hijo[0]).expectiminimax(profundidad-1,etiqueta)
                    m = (hijo[0]).evaluacion
                    prob = 1/18
                    valor = valor + (prob*m)
                self.evaluacion = valor
                
                