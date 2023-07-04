import random
import numpy as np
from copy import deepcopy
from PIL import Image
from PIL import ImageDraw
import time

def tablero_inicial():
    t0 = []
    for i in range(0,24):
        palo = []
        if (i==0):
            palo = ['N']
        elif (i==1):
            palo = ['N']
        elif (i==2):
            palo = ['N']
        elif (i==21):
            palo = ['B']
        elif (i==22):
            palo = ['B']
        elif (i==23):
            palo = ['B']
        t0 += [palo]
    return t0
    
def tablero_random(num_jugadas):
    p = deepcopy(Partida(tablero_inicial(),'N'))
    num_jugada = 0
    while (num_jugada<num_jugadas):
        (dado1,dado2) = p.tirar_dados()
        jugadas_legales = p.jugadas_legales(dado1,dado2)
        jugada = random.choice(list(jugadas_legales))
        p.jugada(jugada,dado1,dado2)
        num_jugada += 1
    return p

class Partida:
    def __init__(self,tablero=tablero_inicial(),turno=None):
        self.tablero = tablero
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
            return self.turno_inicial()
    
    def es_final(self):
        es_final = (self.puntosN==3 or self.puntosB==3)
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
                if ((len(self.tablero[p])!=0 and self.tablero[p][0]==turno) and (self.es_posible(p+dado) or (p+dado>=24 and self.puedes_sacar()) or (p+dado<=-1 and self.puedes_sacar()))):
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
        if (dado1!=dado2):
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
                if (0<=posicion<=23 and len(partida.tablero[posicion])==1 and (rival in partida.tablero[posicion])):
                    (partida.barra_turno(rival)).append(rival)
                    partida.tablero[posicion] = []
                if (0<=posicion<=23):
                    (partida.tablero[posicion]).append(turno)
                else:
                    if (turno=='N'):
                        partida.puntosN = partida.puntosN+1
                    else:
                        partida.puntosB = partida.puntosB+1
                if (partida.es_final()):
                    jugada = (primera,)
                    jugadas_legales.append(jugada)
                else:
                    segundo_movimiento = partida.movimiento(dado)
                    for segunda in segundo_movimiento:
                        jugada = (primera,segunda)
                        jugadas_legales.append(jugada)
        else: #Regla de que si los dos dados son iguales se duplican los dados
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
                if (0<=posicion<=23 and len(partida1.tablero[posicion])==1 and (rival in partida1.tablero[posicion])):
                    (partida1.barra_turno(rival)).append(rival)
                    partida1.tablero[posicion] = []
                if (0<=posicion<=23):
                    (partida1.tablero[posicion]).append(turno)
                else:
                    if (turno=='N'):
                        partida1.puntosN = partida1.puntosN+1
                    else:
                        partida1.puntosB = partida1.puntosB+1
                if (partida1.es_final()):
                    jugada = (primera,)
                    jugadas_legales.append(jugada)
                else:
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
                        if (0<=posicion<=23 and len(partida2.tablero[posicion])==1 and (rival in partida2.tablero[posicion])):
                            (partida2.barra_turno(rival)).append(rival)
                            partida2.tablero[posicion] = []
                        if (0<=posicion<=23):
                            (partida2.tablero[posicion]).append(turno)
                        else:
                            if (turno=='N'):
                                partida2.puntosN = partida2.puntosN+1
                            else:
                                partida2.puntosB = partida2.puntosB+1
                        if (partida2.es_final()):
                            jugada = (primera,segunda)
                            jugadas_legales.append(jugada)
                        else:
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
                                if (0<=posicion<=23 and len(partida3.tablero[posicion])==1 and (rival in partida3.tablero[posicion])):
                                    (partida3.barra_turno(rival)).append(rival)
                                    partida3.tablero[posicion] = []
                                if (0<=posicion<=23):
                                    (partida3.tablero[posicion]).append(turno)
                                else:
                                    if (turno=='N'):
                                        partida3.puntosN = partida3.puntosN+1
                                    else:
                                        partida3.puntosB = partida3.puntosB+1
                                if (partida3.es_final()):
                                    jugada = (primera,segunda,tercera)
                                    jugadas_legales.append(jugada)
                                else:
                                    cuarto_movimiento = partida3.movimiento(dado)
                                    for cuarta in cuarto_movimiento:
                                        jugada = (primera,segunda,tercera,cuarta)
                                        jugadas_legales.append(jugada)
        return jugadas_legales
                
    def jugada(self,jugada,dado1,dado2,jugadas_legales=None):
        if (jugadas_legales==None):
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
                    if (len(self.tablero[posicion])==1 and (rival in self.tablero[posicion])):
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
        pasos_negras = len(self.barra_turno('N'))*30
        extra_negras = 0
        pasos_blancas = len(self.barra_turno('B'))*30
        extra_blancas = 0
        for i in range(0,24):
            if (len(self.tablero[i])!=0):
                if (self.tablero[i][0]=='N'):
                    pasos_negras += len(self.tablero[i])*(24-i)
                    if (len(self.tablero[i])>1):
                        extra_negras += 1
                    elif (self.esta_pasada(i,'N')):
                       extra_negras += 2 
                else:
                    pasos_blancas += len(self.tablero[i])*(i+1)
                    if (len(self.tablero[i])>1):
                        extra_blancas += 1
                    elif (self.esta_pasada(i,'B')):
                       extra_blancas += 2 
        if (jugador=='N'):
            puntos = pasos_blancas-pasos_negras+extra_negras-extra_blancas
            signo = self.puntosN-self.puntosB
        else:
            puntos = pasos_negras-pasos_blancas+extra_blancas-extra_negras
            signo = self.puntosB-self.puntosN
        if (not self.es_final()):
            return puntos
        else:
            return (np.sign(signo)*100)
    
    def esta_pasada(self,posicion,ficha):
        esta_pasada = True
        if (ficha=='N'):
            rival = 'B'
            for i in range(posicion+1,24):
                if (rival in self.tablero[i]):
                    esta_pasada = False
                    break
        elif (ficha=='B'):
            rival = 'N'
            for i in range(posicion-1,-1,-1):
                if (rival in self.tablero[i]):
                    esta_pasada = False
                    break
        else:
            esta_pasada = False
        return esta_pasada
        
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
                elif(len(self.tablero[i])<=5 or flags2[i-12]):
                    linea = linea + "    "
                else:
                    flags2[i-12] = True
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
    
    def imagen_tablero(self,dado1=None,dado2=None):
        tablero_vacio = Image.open("tablero_vacio_backgammon.png")
        hay_dados = (dado1!=None and dado2!=None)
        if hay_dados:
            coordenada_X1 = 6+213+3+32+3+71-12
            coordenada_X2 = 6+213+3+32+3+71*2-12
            coordenada_Y = 206-12
            img_dado1 = Image.open("dado_"+str(dado1)+".png")
            tablero_vacio.paste(img_dado1, (coordenada_X1, coordenada_Y))
            img_dado2 = Image.open("dado_"+str(dado2)+".png")
            tablero_vacio.paste(img_dado2, (coordenada_X2, coordenada_Y))
        for p in range(0,len(self.barraN)):
            coordenada_X = 222
            coordenada_Y = 6+(32*p)
            ficha = ImageDraw.Draw(tablero_vacio)
            ficha.ellipse((coordenada_X, coordenada_Y, coordenada_X+32, coordenada_Y+32), fill = (90,91,121))
        for p in range(0,len(self.barraB)):
            coordenada_X = 222
            coordenada_Y = 374-(32*p)
            ficha = ImageDraw.Draw(tablero_vacio)
            ficha.ellipse((coordenada_X, coordenada_Y, coordenada_X+32, coordenada_Y+32), fill = (244,243,239))
        for i in range(0,24):
            l = len(self.tablero[i])
            for j in range(0,l):
                if (0<=i<6):
                    coordenada_X = 50+(35*(11-i))
                    coordenada_Y = 6+(32*j)
                elif (6<=i<12):
                    coordenada_X = 9+(35*(11-i))
                    coordenada_Y = 6+(32*j)
                elif (12<=i<18):
                    coordenada_X = 9+(35*(i-12))
                    coordenada_Y = 374-(32*j)
                else:
                    coordenada_X = 50+(35*(i-12))
                    coordenada_Y = 374-(32*j)
                if (self.tablero[i][j]=='N'):
                    ficha = ImageDraw.Draw(tablero_vacio)
                    ficha.ellipse((coordenada_X, coordenada_Y, coordenada_X+32, coordenada_Y+32), fill = (90,91,121))
                else:
                    ficha = ImageDraw.Draw(tablero_vacio)
                    ficha.ellipse((coordenada_X, coordenada_Y, coordenada_X+32, coordenada_Y+32), fill = (244,243,239))
        archivo = input("Introduce el nombre del archivo: ")
        tablero_vacio.save(archivo+".png")
    
    def jugar(self,fichas,algoritmo,profundidad):
        self.imprimir_tablero()
        inicial = True
        ilegal = False
        jugador = fichas
        aj = Arbol_juego(self)
        while (not self.es_final()):
            if inicial:
                (dado1,dado2) = self.turno_inicial()
                print(f'Empieza el jugador {self.turno}\n')
                inicial = False
            else:
                if not ilegal:
                    (dado1,dado2) = self.tirar_dados()
                else:
                    ilegal = False
            print(f'Dado 1: {dado1} | Dado 2: {dado2}')
            aj.llenar_nivel()
            for hijo in aj.hijos:
                if (hijo[1]==(dado1,dado2) or hijo[1]==(dado2,dado1)):
                    aj = hijo[0]
                    break
            jugadas_legales = self.jugadas_legales(dado1,dado2)
            if (not bool(jugadas_legales)):
                print("Salta el turno")
                aj = aj.hijos[0][0] 
                if (self.turno=='N'):
                    self.turno = 'B'
                else:
                    self.turno = 'N'
                self.imprimir_tablero()
            else:
                if (self.turno==jugador):
                    ficha1 = int(input("Introduzca la ficha que quiere mover con el dado 1 (1-24): "))
                    ficha2 = int(input("Introduzca la ficha que quiere mover con el dado 2 (1-24): "))
                    if ((ficha1 in range(0,26)) and (ficha2 in range(0,26))):
                        ficha1 = ficha1-1
                        ficha2 = ficha2-1
                        jugada = ((ficha1,dado1),(ficha2,dado2))        
                        if (jugada in jugadas_legales):
                            self.jugada(jugada,dado1,dado2)
                            for hijo in aj.hijos:
                                if (hijo[1]==jugada):
                                    aj = hijo[0]
                                    break
                            self.imprimir_tablero()
                        else:
                            ilegal = True
                            print("Jugada ilegal")
                            self.imprimir_tablero()
                else:
                    print("\nTurno de la maquina")
                    aj, jugada = self.decision_maquina(aj,algoritmo,profundidad)
                    self.jugada(jugada,dado1,dado2)
                    self.imprimir_tablero()      
        final = self.heuristica(jugador)
        if (final!=0):
            if (final==100):
                print("\nHas ganado")
            else:
                print("\nHas perdido")
        else:
            print("\nHas empatado")
    
    def jugar_maquinas(self,algoritmoN,profundidadN,algoritmoB,profundidadB):
        ambosMCTS = (algoritmoN=="MCTS" and algoritmoB=="MCTS")
        self.imprimir_tablero()
        if (self.turno==None):
            inicial = True
        else:
            inicial = False
        aj = Arbol_juego(self)
        while (not self.es_final()):
            if inicial:
                (dado1,dado2) = self.turno_inicial()
                print(f'Empieza el jugador {self.turno}\n')
                inicial = False
            else:
                (dado1,dado2) = self.tirar_dados()
            print(f'Dado 1: {dado1} | Dado 2: {dado2}')
            aj.llenar_nivel()
            for hijo in aj.hijos:
                if (hijo[1]==(dado1,dado2) or hijo[1]==(dado2,dado1)):
                    aj = hijo[0]
                    break
            jugadas_legales = self.jugadas_legales(dado1,dado2)
            if (not bool(jugadas_legales)):
                print("Salta el turno")
                aj = aj.hijos[0][0] 
                if (self.turno=='N'):
                    self.turno = 'B'
                else:
                    self.turno = 'N'
                self.imprimir_tablero()
            else:
                if (self.turno=='N'):
                    print(f"\nTurno de {algoritmoN} {profundidadN}")
                    aj, jugada = self.decision_maquina(aj,algoritmoN,profundidadN,ambosMCTS)
                    self.jugada(jugada,dado1,dado2)
                    self.imprimir_tablero() 
                else:
                    print(f"\nTurno de {algoritmoB} {profundidadB}")
                    aj, jugada = self.decision_maquina(aj,algoritmoB,profundidadB,ambosMCTS)
                    self.jugada(jugada,dado1,dado2)
                    self.imprimir_tablero()      
        final = self.heuristica('N')
        if (final!=0):
            if (final==100):
                print("\nGana N")
                return 'N'
            else:
                print("\nGana B")
                return 'B'
        else:
            print("\nEmpate")
            return "Empate"
    
    def decision_maquina(self,aj,algoritmo,profundidad,ambosMCTS):
        if (algoritmo=="expectiminimax"):
            aj.expectiminimax(profundidad,"max")
            for hijo in aj.hijos:
                if (hijo[0].evaluacion==aj.evaluacion):
                    return hijo[0], hijo[1]
        elif (algoritmo=="expectiminimax_limitado"):
            aj.expectiminimax_limitado(profundidad,"max")
            for hijo in aj.hijos:
                if (hijo[0].evaluacion==aj.evaluacion):
                    return hijo[0], hijo[1]
        elif (algoritmo=="MCTS"):
            h = aj.MCTS(profundidad)
            for hijo in aj.hijos:
                if (hijo[0]==h and ambosMCTS):
                    p = deepcopy(hijo[0].partida)
                    aj = Arbol_juego(p)
                    return aj, hijo[1]
                elif (hijo[0]==h):
                    return hijo[0], hijo[1]
        else:
            aj.llenar_nivel()
            hijo = random.choice(aj.hijos)
            return hijo[0], hijo[1]

class Arbol_juego:
    def __init__(self,partida):
        self.hijos = []
        self.padre = None
        self.partida = partida
        self.evaluacion = None
        self.random = True
        self.visitado = False
        self.Q = 0
        self.N = 0
        
    def anadir_hijo(self,hijo,jugada):
        (self.hijos).append((hijo,jugada))

    def imprimir_hijos(self):
        for hijo in (self.hijos):
            print(hijo[1])
            (hijo[0].partida).imprimir_tablero()
            
    def imagen_hijos(self):
        for hijo in (self.hijos):
            (hijo[0].partida).imagen_tablero()
                
    def llenar_nivel(self):
        if (len(self.hijos)==0):
            combinaciones = [(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(2,2),(2,3),(2,4),(2,5),(2,6),(3,3),(3,4),(3,5),(3,6),(4,4),(4,5),(4,6),(5,5),(5,6),(6,6)]
            for combinacion in combinaciones:
                p = deepcopy(self.partida)
                aj = Arbol_juego(p)
                aj.random = False
                aj.padre = self
                (self.hijos).append((aj,combinacion))
            for hijo in self.hijos:
                dado1 = hijo[1][0]
                dado2 = hijo[1][1]
                jugadas_legales = (self.partida).jugadas_legales(dado1,dado2)
                if (len(jugadas_legales)==0):
                    p = deepcopy(self.partida)
                    if (p.turno=='N'):
                        p.turno = 'B'
                    else:
                        p.turno = 'N'
                    aj = Arbol_juego(p)
                    aj.padre = hijo[0]
                    hijo[0].anadir_hijo(aj,None)
                else:
                    for jugada in jugadas_legales:
                        p = deepcopy(self.partida)
                        p.jugada(jugada,dado1,dado2,jugadas_legales)
                        aj = Arbol_juego(p)
                        aj.padre = hijo[0]
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
                self.llenar_nivel()
                for hijo in self.hijos:
                    (hijo[0]).expectiminimax(profundidad-1,etiqueta)
                    m = (hijo[0]).evaluacion
                    prob = 1/21
                    valor = valor + (prob*m)
                self.evaluacion = valor
                
    def expectiminimax_limitado(self,profundidad,etiqueta):
        casos_eliminados = [(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(1,3),(1,4),(1,5),(2,4),(2,5),(2,6),(3,5),(3,6),(4,6)]
        num_eliminados = len(casos_eliminados)
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
                        (hijo[0]).expectiminimax_limitado(profundidad-1,"min")
                        m = (hijo[0]).evaluacion
                        valor = max(valor,m)
                    self.evaluacion = valor
                else:
                    valor = np.inf
                    self.llenar_nivel()
                    for hijo in self.hijos:
                        (hijo[0]).expectiminimax_limitado(profundidad-1,"max")
                        m = (hijo[0]).evaluacion
                        valor = min(valor,m)
                    self.evaluacion = valor
            else:
                valor = 0
                self.llenar_nivel()
                for hijo in self.hijos:
                    if (not hijo[1] in casos_eliminados):
                        (hijo[0]).expectiminimax_limitado(profundidad-1,etiqueta)
                        m = (hijo[0]).evaluacion
                        prob = 1/(21-num_eliminados)
                        valor = valor + (prob*m)
                self.evaluacion = valor
    
    def MCTS(self,iteraciones):
        iteracion = 0
        turno = (self.partida).turno
        while (iteracion<iteraciones):
            primera = (iteracion==0)
            hoja = self.atravesar(primera)
            resultado_simulacion = hoja.rollout(turno)
            hoja.retropropagacion(resultado_simulacion)
            iteracion += 1
        return (self.mejor_hijo())

    def atravesar(self,primera):
        nodo = self
        if primera:
            nodo.llenar_nivel()
        else:
            while (nodo.compl_expandido()):
                nodo.llenar_nivel()
                nodo = nodo.max_uct()
        return (nodo.sin_visitar())
    
    def rollout(self,turno):
        nodo = self
        while (not (nodo.partida).es_final()):
            nodo.llenar_nivel()
            nodo = nodo.rollout_policy()
        return (nodo.resultado(turno))
    
    def rollout_policy(self):
        nodo = self
        hijo = random.choice(nodo.hijos)
        return hijo[0]
    
    def resultado(self,turno):
        resultado = (self.partida).heuristica(turno)
        return (np.sign(resultado))
    
    def retropropagacion(self,resultado):
        self.update_stats(resultado)
        if (not (self.padre==None)):
            (self.padre).retropropagacion(resultado)
        
    def compl_expandido(self):
        if (len(self.hijos)==0):
            expandido = False
        else:    
            expandido = True
            for hijo in (self.hijos):
                if (not hijo[0].visitado):
                    expandido = False
                    break
        return expandido
    
    def max_uct(self):
        max_uct = -np.inf
        mejor_hijo = None
        c = np.sqrt(2)
        Np = self.N
        for hijo in (self.hijos):
            Q = hijo[0].Q
            N = hijo[0].N
            uct = (Q/N)+(c*np.sqrt(np.log(Np)/N))
            if (uct>=max_uct):
                max_uct = uct
                mejor_hijo = hijo[0]
        return mejor_hijo
    
    def sin_visitar(self):
        sin_visitar = self
        for hijo in (self.hijos):
            if (not hijo[0].visitado):
                sin_visitar = hijo[0]
                hijo[0].visitado = True
                break
        return sin_visitar
    
    def mejor_hijo(self):
        max_visitas = -np.inf
        mejor_hijo = None
        for hijo in (self.hijos):
            if (hijo[0].N>=max_visitas):
                max_visitas = hijo[0].N
                mejor_hijo = hijo[0]
        return mejor_hijo
    
    def update_stats(self, resultado):
        self.N = self.N + 1
        if (resultado==1):
            self.Q = self.Q + 1
        elif (resultado==0):
            self.Q = self.Q + 0.5
        else:
            self.Q = self.Q + 0
                
def hypergammon():
    fichas = input("Introduce tu color (N o B): ")
    algoritmo = input("Introduce el algoritmo (expectiminimax o MCTS o random): ")
    if (algoritmo!="MCTS"):
        profundidad = int(input("Introduce la profundidad: "))
    else:
        profundidad = int(input("Introduce el número de iteraciones: "))
    if ((fichas=='N' or fichas=='B') and (algoritmo=="expectiminimax" or algoritmo=="MCTS" or algoritmo=="random")):
        partida = Partida()
        partida.jugar(fichas,algoritmo,profundidad)       
        
def hypergammon_maquinas(posiciones,algoritmoN,profundidadN,algoritmoB,profundidadB):
    puntos_algoritmoN = 0
    puntos_algoritmoB = 0
    for posicion in posiciones:
        resultado = posicion.jugar_maquinas(algoritmoN,profundidadN,algoritmoB,profundidadB)
        if (resultado=='N'):
            puntos_algoritmoN += 1
        elif (resultado=='B'):
            puntos_algoritmoB += 1
        else:
            puntos_algoritmoN += 0.5
            puntos_algoritmoB += 0.5
    return (((algoritmoN,profundidadN),puntos_algoritmoN),((algoritmoB,profundidadB),puntos_algoritmoB))


tiempos_expectiminimax = {'expectiminimax 1': 0.0002368821038140191,
'expectiminimax 2': 0.7719471262704308,
'expectiminimax 3': 0.9240370213813425}

tiempos_expectiminimax_limitado = {'expectiminimax_limitado 1': 0.00015363326439490684,
'expectiminimax_limitado 2': 0.7447383063180106,
'expectiminimax_limitado 3': 0.8291703462600708,
'expectiminimax_limitado 4': 60.8937874480130561}

tiempos_MCTS = {'MCTS 60': 59.78140670602971}

p0 = deepcopy(Partida())
p1 = Partida([[],['N'],[],[],[],[],['N'],[],[],[],[],['N'],[],[],[],['B'],[],[],['B'],[],[],[],['B'],[]],'N')
p2 = Partida([[],['N'],[],[],[],[],['N'],[],['N'],[],[],[],[],[],[],[],[],['B'],['B'],[],[],[],['B'],[]],'N')
p3 = Partida([[],[],['N'],[],[],[],[],[],[],[],['N', 'N'],[],[],['B'],[],[],[],[],[],['B'],['B'],[],[],[]],'N')
p4 = Partida([[],[],[],['N'],[],[],[],['N'],['N'],[],['B'],[],[],[],[],[],['B'],[],[],[],['B'],[],[],[]],'N')
p5 = Partida([[],[],[],[],['B'],[],[],[],[],[],[],[],[],[],[],['N'],[],['B'],[],['B'],[],['N'],[],['N']],'N')
p6 = Partida([[],[],['N'],['B'],['N'],['N'],[],[],[],[],[],[],['B'],[],[],[],[],['B'],[],[],[],[],[],[]],'N')
p7 = Partida([[],[],[],[],[],[],[],['N'],[],['N', 'N'],[],[],[],[],[],['B'],[],['B'],[],[],['B'],[],[],[]],'B')
p8 = Partida([[],[],[],[],['N'],[],['N'],[],[],[],[],[],['B'],[],['N'],[],['B'],[],[],['B'],[],[],[],[]],'B')
p9 = Partida([[],[],[],[],[],[],[],['N'],[],[],['N'],[],[],[],[],['N'],['B'],['B'],[],[],[],[],[],[]],'B')
p9.barraB = ['B']

posiciones_iniciales = [p0,p1,p2,p3,p4,p5,p6,p7,p8,p9]


"""resultados1EEl = []
for i in [1,2,3]:
    for j in [1,2,3,4]:
        posiciones = deepcopy(posiciones_iniciales)
        resultado = hypergammon_maquinas(posiciones,"expectiminimax",i,"expectiminimax_limitado",j)
        resultados1EEl.append(resultado)

resultados2EEl = []
for i in [1,2,3]:
    for j in [1,2,3,4]:
        posiciones = deepcopy(posiciones_iniciales)
        resultado = hypergammon_maquinas(posiciones,"expectiminimax_limitado",j,"expectiminimax",i)
        resultados2EEl.append(resultado)

resultadosEEl = []
for r1 in resultados1EEl:
    for r2 in resultados2EEl:
        if (r1[0][0]==r2[1][0] and r1[1][0]==r2[0][0]):
            resultadosEEl.append(((r1[0][0],r1[0][1]+r2[1][1]),(r2[0][0],r1[1][1]+r2[0][1])))"""
            
resultados1EEl = [((('expectiminimax', 1), 5), (('expectiminimax_limitado', 1), 5)),
((('expectiminimax', 1), 6), (('expectiminimax_limitado', 2), 4)),
((('expectiminimax', 1), 5), (('expectiminimax_limitado', 3), 5)),
((('expectiminimax', 1), 5), (('expectiminimax_limitado', 4), 5)),
((('expectiminimax', 2), 7), (('expectiminimax_limitado', 1), 3)),
((('expectiminimax', 2), 6), (('expectiminimax_limitado', 2), 4)),
((('expectiminimax', 2), 5), (('expectiminimax_limitado', 3), 5)),
((('expectiminimax', 2), 4), (('expectiminimax_limitado', 4), 6)),
((('expectiminimax', 3), 7), (('expectiminimax_limitado', 1), 3)),
((('expectiminimax', 3), 7), (('expectiminimax_limitado', 2), 3)),
((('expectiminimax', 3), 8), (('expectiminimax_limitado', 3), 2)),
((('expectiminimax', 3), 6), (('expectiminimax_limitado', 4), 4))]

resultados2EEl = [((('expectiminimax_limitado', 1), 4), (('expectiminimax', 1), 6)),
((('expectiminimax_limitado', 2), 2), (('expectiminimax', 1), 8)),
((('expectiminimax_limitado', 3), 8), (('expectiminimax', 1), 2)),
((('expectiminimax_limitado', 4), 7), (('expectiminimax', 1), 3)),
((('expectiminimax_limitado', 1), 5), (('expectiminimax', 2), 5)),
((('expectiminimax_limitado', 2), 4), (('expectiminimax', 2), 6)),
((('expectiminimax_limitado', 3), 7), (('expectiminimax', 2), 3)),
((('expectiminimax_limitado', 4), 7), (('expectiminimax', 2), 3)),
((('expectiminimax_limitado', 1), 4), (('expectiminimax', 3), 6)),
((('expectiminimax_limitado', 2), 4), (('expectiminimax', 3), 6)),
((('expectiminimax_limitado', 3), 6), (('expectiminimax', 3), 4)),
((('expectiminimax_limitado', 4), 2), (('expectiminimax', 3), 8))]

resultadosEEl = [((('expectiminimax', 1), 11), (('expectiminimax_limitado', 1), 9)),
((('expectiminimax', 1), 14), (('expectiminimax_limitado', 2), 6)),
((('expectiminimax', 1), 7), (('expectiminimax_limitado', 3), 13)),
((('expectiminimax', 1), 8), (('expectiminimax_limitado', 4), 12)),
((('expectiminimax', 2), 12), (('expectiminimax_limitado', 1), 8)),
((('expectiminimax', 2), 12), (('expectiminimax_limitado', 2), 8)),
((('expectiminimax', 2), 8), (('expectiminimax_limitado', 3), 12)),
((('expectiminimax', 2), 7), (('expectiminimax_limitado', 4), 13)),
((('expectiminimax', 3), 13), (('expectiminimax_limitado', 1), 7)),
((('expectiminimax', 3), 13), (('expectiminimax_limitado', 2), 7)),
((('expectiminimax', 3), 12), (('expectiminimax_limitado', 3), 8)),
((('expectiminimax', 3), 14), (('expectiminimax_limitado', 4), 6))] #Resultados de ejecutar el código de arriba


"""resultados1ElM = []
for i in [1,2,3,4]:
    for j in [60]:
        posiciones = deepcopy(posiciones_iniciales)
        resultado = hypergammon_maquinas(posiciones,"expectiminimax_limitado",i,"MCTS",j)
        resultados1ElM.append(resultado)

resultados2ElM = []
for i in [1,2,3,4]:
    for j in [60]:
        posiciones = deepcopy(posiciones_iniciales)
        resultado = hypergammon_maquinas(posiciones,"MCTS",j,"expectiminimax_limitado",i)
        resultados2ElM.append(resultado)

resultadosElM = []
for r1 in resultados1ElM:
    for r2 in resultados2ElM:
        if (r1[0][0]==r2[1][0] and r1[1][0]==r2[0][0]):
            resultadosElM.append(((r1[0][0],r1[0][1]+r2[1][1]),(r2[0][0],r1[1][1]+r2[0][1])))"""

resultados1ElM = [((('expectiminimax_limitado', 1), 6), (('MCTS', 60), 4)),
((('expectiminimax_limitado', 2), 8), (('MCTS', 60), 2)),
((('expectiminimax_limitado', 3), 9), (('MCTS', 60), 1)),
((('expectiminimax_limitado', 4), 8), (('MCTS', 60), 2))]

resultados2ElM = [((('MCTS', 60), 7), (('expectiminimax_limitado', 1), 3)),
((('MCTS', 60), 5), (('expectiminimax_limitado', 2), 5)),
((('MCTS', 60), 4), (('expectiminimax_limitado', 3), 6)),
((('MCTS', 60), 3), (('expectiminimax_limitado', 4), 7))]
            
resultadosElM = [((('expectiminimax_limitado', 1), 9), (('MCTS', 60), 11)),
((('expectiminimax_limitado', 2), 13), (('MCTS', 60), 7)),
((('expectiminimax_limitado', 3), 15), (('MCTS', 60), 5)),
((('expectiminimax_limitado', 4), 15), (('MCTS', 60), 5))] #Resultados de ejecutar el código de arriba


"""resultados1EM = []
for i in [1,2,3]:
    for j in [60]:
        posiciones = deepcopy(posiciones_iniciales)
        resultado = hypergammon_maquinas(posiciones,"expectiminimax",i,"MCTS",j)
        resultados1EM.append(resultado)

resultados2EM = []
for i in [1,2,3]:
    for j in [60]:
        posiciones = deepcopy(posiciones_iniciales)
        resultado = hypergammon_maquinas(posiciones,"MCTS",j,"expectiminimax",i)
        resultados2EM.append(resultado)

resultadosEM = []
for r1 in resultados1EM:
    for r2 in resultados2EM:
        if (r1[0][0]==r2[1][0] and r1[1][0]==r2[0][0]):
            resultadosEM.append(((r1[0][0],r1[0][1]+r2[1][1]),(r2[0][0],r1[1][1]+r2[0][1])))"""

resultados1EM = [((('expectiminimax', 1), 7), (('MCTS', 60), 3)),
((('expectiminimax', 2), 8), (('MCTS', 60), 2)),
((('expectiminimax', 3), 8), (('MCTS', 60), 2))]
            
resultados2EM = [((('MCTS', 60), 6), (('expectiminimax', 1), 4)),
((('MCTS', 60), 4), (('expectiminimax', 2), 6)),
((('MCTS', 60), 2), (('expectiminimax', 3), 8))]

resultadosEM = [((('expectiminimax', 1), 11), (('MCTS', 60), 9)),
((('expectiminimax', 2), 14), (('MCTS', 60), 6)),
((('expectiminimax', 3), 16), (('MCTS', 60), 4))] #Resultados de ejecutar el código de arriba


"""resultados1MM = []
posiciones = deepcopy(posiciones_iniciales)
resultado = hypergammon_maquinas(posiciones,"MCTS",60,"MCTS",60)
resultados1MM.append(resultado)"""

resultados1MM = [((('MCTS', 60), 6), (('MCTS', 60), 4))] #Resultados de ejecutar el código de arriba


"""resultados1EE = []
v = [1,2,3]
for i in [1,2,3]:
    v.remove(i)
    for j in v:
        posiciones = deepcopy(posiciones_iniciales)
        resultado = hypergammon_maquinas(posiciones,"expectiminimax",i,"expectiminimax",j)
        resultados1EE.append(resultado)

resultados2EE = []
v = [1,2,3]
for i in [1,2,3]:
    v.remove(i)
    for j in v:
        posiciones = deepcopy(posiciones_iniciales)
        resultado = hypergammon_maquinas(posiciones,"expectiminimax",j,"expectiminimax",i)
        resultados2EE.append(resultado)

resultadosEE = []
for r1 in resultados1EE:
    for r2 in resultados2EE:
        if (r1[0][0]==r2[1][0] and r1[1][0]==r2[0][0]):
            resultadosEE.append(((r1[0][0],r1[0][1]+r2[1][1]),(r2[0][0],r1[1][1]+r2[0][1])))"""
            
resultados1EE = [((('expectiminimax', 1), 8), (('expectiminimax', 1), 2)),
((('expectiminimax', 1), 2), (('expectiminimax', 2), 8)),
((('expectiminimax', 1), 6), (('expectiminimax', 3), 4)),
((('expectiminimax', 2), 7), (('expectiminimax', 2), 3)),
((('expectiminimax', 2), 6), (('expectiminimax', 3), 4)),
((('expectiminimax', 3), 3), (('expectiminimax', 3), 7))]

resultados2EE = [((('expectiminimax', 2), 4), (('expectiminimax', 1), 6)),
((('expectiminimax', 3), 8), (('expectiminimax', 1), 2)),
((('expectiminimax', 3), 7), (('expectiminimax', 2), 3))]

resultadosEE = [((('expectiminimax', 1), 8), (('expectiminimax', 2), 12)),
((('expectiminimax', 1), 8), (('expectiminimax', 3), 12)),
((('expectiminimax', 2), 9), (('expectiminimax', 3), 11))] #Resultados de ejecutar el código de arriba


"""resultados1ElEl = []
v = [1,2,3,4]
for i in [1,2,3,4]:
    v.remove(i)
    for j in v:
        posiciones = deepcopy(posiciones_iniciales)
        resultado = hypergammon_maquinas(posiciones,"expectiminimax_limitado",i,"expectiminimax_limitado",j)
        resultados1ElEl.append(resultado)

resultados2ElEl = []
v = [1,2,3,4]
for i in [1,2,3,4]:
    v.remove(i)
    for j in v:
        posiciones = deepcopy(posiciones_iniciales)
        resultado = hypergammon_maquinas(posiciones,"expectiminimax_limitado",j,"expectiminimax_limitado",i)
        resultados2ElEl.append(resultado)

resultadosElEl = []
for r1 in resultados1ElEl:
    for r2 in resultados2ElEl:
        if (r1[0][0]==r2[1][0] and r1[1][0]==r2[0][0]):
            resultadosElEl.append(((r1[0][0],r1[0][1]+r2[1][1]),(r2[0][0],r1[1][1]+r2[0][1])))"""
            
resultados1ElEl = [((('expectiminimax_limitado', 1), 7), (('expectiminimax_limitado', 1), 3)),
((('expectiminimax_limitado', 1), 7), (('expectiminimax_limitado', 2), 3)),
((('expectiminimax_limitado', 1), 4), (('expectiminimax_limitado', 3), 6)),
((('expectiminimax_limitado', 1), 4), (('expectiminimax_limitado', 4), 6)),
((('expectiminimax_limitado', 2), 5), (('expectiminimax_limitado', 2), 5)),
((('expectiminimax_limitado', 2), 5), (('expectiminimax_limitado', 3), 5)),
((('expectiminimax_limitado', 2), 5), (('expectiminimax_limitado', 4), 5)),
((('expectiminimax_limitado', 3), 5), (('expectiminimax_limitado', 3), 5)),
((('expectiminimax_limitado', 3), 4), (('expectiminimax_limitado', 4), 6)),
((('expectiminimax_limitado', 4), 6), (('expectiminimax_limitado', 4), 4))]

resultados2ElEl = [((('expectiminimax_limitado', 2), 4), (('expectiminimax_limitado', 1), 6)),
((('expectiminimax_limitado', 3), 8), (('expectiminimax_limitado', 1), 2)),
((('expectiminimax_limitado', 4), 6), (('expectiminimax_limitado', 1), 4)),
((('expectiminimax_limitado', 3), 6), (('expectiminimax_limitado', 2), 4)),
((('expectiminimax_limitado', 4), 7), (('expectiminimax_limitado', 2), 3)),
((('expectiminimax_limitado', 4), 8), (('expectiminimax_limitado', 3), 2))]

resultadosElEl = [((('expectiminimax_limitado', 1), 13), (('expectiminimax_limitado', 2), 7)),
((('expectiminimax_limitado', 1), 6), (('expectiminimax_limitado', 3), 14)),
((('expectiminimax_limitado', 1), 8), (('expectiminimax_limitado', 4), 12)),
((('expectiminimax_limitado', 2), 9), (('expectiminimax_limitado', 3), 11)),
((('expectiminimax_limitado', 2), 8), (('expectiminimax_limitado', 4), 12)),
((('expectiminimax_limitado', 3), 6), (('expectiminimax_limitado', 4), 14))] #Resultados de ejecutar el código de arriba


"""resultados1ER = []
for i in [1,2,3]:
    posiciones = deepcopy(posiciones_iniciales)
    resultado = hypergammon_maquinas(posiciones,"expectiminimax",i,"random",0)
    resultados1ER.append(resultado)

resultados2ER = []
for i in [1,2,3]:
    posiciones = deepcopy(posiciones_iniciales)
    resultado = hypergammon_maquinas(posiciones,"random",0,"expectiminimax",i)
    resultados2ER.append(resultado)

resultadosER = []
for r1 in resultados1ER:
    for r2 in resultados2ER:
        if (r1[0][0]==r2[1][0] and r1[1][0]==r2[0][0]):
            resultadosER.append(((r1[0][0],r1[0][1]+r2[1][1]),(r2[0][0],r1[1][1]+r2[0][1])))"""
            
resultados1ER = [((('expectiminimax', 1), 10), (('random', 0), 0)),
((('expectiminimax', 2), 9), (('random', 0), 1)),
((('expectiminimax', 3), 9), (('random', 0), 1))]

resultados2ER = [((('random', 0), 1), (('expectiminimax', 1), 9)),
((('random', 0), 3), (('expectiminimax', 2), 7)),
((('random', 0), 1), (('expectiminimax', 3), 9))]

resultadosER = [((('expectiminimax', 1), 19), (('random', 0), 1)),
((('expectiminimax', 2), 16), (('random', 0), 4)),
((('expectiminimax', 3), 18), (('random', 0), 2))] #Resultados de ejecutar el código de arriba


"""resultados1ElR = []
for i in [1,2,3,4]:
    posiciones = deepcopy(posiciones_iniciales)
    resultado = hypergammon_maquinas(posiciones,"expectiminimax_limitado",i,"random",0)
    resultados1ElR.append(resultado)

resultados2ElR = []
for i in [1,2,3,4]:
    posiciones = deepcopy(posiciones_iniciales)
    resultado = hypergammon_maquinas(posiciones,"random",0,"expectiminimax_limitado",i)
    resultados2ElR.append(resultado)

resultadosElR = []
for r1 in resultados1ElR:
    for r2 in resultados2ElR:
        if (r1[0][0]==r2[1][0] and r1[1][0]==r2[0][0]):
            resultadosElR.append(((r1[0][0],r1[0][1]+r2[1][1]),(r2[0][0],r1[1][1]+r2[0][1])))"""
            
resultados1ElR = [((('expectiminimax_limitado', 1), 8), (('random', 0), 2)),
((('expectiminimax_limitado', 2), 9), (('random', 0), 1)),
((('expectiminimax_limitado', 3), 9), (('random', 0), 1)),
((('expectiminimax_limitado', 4), 9), (('random', 0), 1))]

resultados2ElR = [((('random', 0), 2), (('expectiminimax_limitado', 1), 8)),
((('random', 0), 2), (('expectiminimax_limitado', 2), 8)),
((('random', 0), 2), (('expectiminimax_limitado', 3), 8)),
((('random', 0), 2), (('expectiminimax_limitado', 4), 8))]

resultadosElR = [((('expectiminimax_limitado', 1), 16), (('random', 0), 4)),
((('expectiminimax_limitado', 2), 17), (('random', 0), 3)),
((('expectiminimax_limitado', 3), 17), (('random', 0), 3)),
((('expectiminimax_limitado', 4), 17), (('random', 0), 3))] #Resultados de ejecutar el código de arriba


"""resultados1MR = []
for i in [60]:
    posiciones = deepcopy(posiciones_iniciales)
    resultado = hypergammon_maquinas(posiciones,"MCTS",i,"random",0)
    resultados1MR.append(resultado)
posiciones = deepcopy(posiciones_iniciales)
resultado = hypergammon_maquinas(posiciones,"random",0,"random",0)
resultados1MR.append(resultado)

resultados2MR = []
for i in [60]:
    posiciones = deepcopy(posiciones_iniciales)
    resultado = hypergammon_maquinas(posiciones,"random",0,"MCTS",i)
    resultados2MR.append(resultado)

resultadosMR = []
for r1 in resultados1MR:
    for r2 in resultados2MR:
        if (r1[0][0]==r2[1][0] and r1[1][0]==r2[0][0]):
            resultadosMR.append(((r1[0][0],r1[0][1]+r2[1][1]),(r2[0][0],r1[1][1]+r2[0][1])))"""
            
resultados1MR = [((('MCTS', 60), 9), (('random', 0), 1)),
((('random', 0), 6), (('random', 0), 4))]

resultados2MR = [((('random', 0), 3), (('MCTS', 60), 7))]

resultadosMR = [((('MCTS', 60), 16), (('random', 0), 4))] #Resultados de ejecutar el código de arriba

