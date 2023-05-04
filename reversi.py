import random
import numpy as np
from copy import deepcopy
import time

def tablero_inicial():
    t0 = []
    for i in range(0,8):
        fila = []
        for j in range(0,8):
            fila.append('b')
        t0 += [fila] 
    t0[3][3] = 'B'
    t0[4][4] = 'B'
    t0[3][4] = 'N'
    t0[4][3] = 'N'
    return t0

def tablero_random(num_jugadas):
    p = Partida()
    num_jugada = 0
    while (num_jugada<num_jugadas):
        jugadas_legales = p.jugadas_legales()
        jugada = random.choice(list(jugadas_legales))
        p.jugada(jugada[0],jugada[1])
        num_jugada += 1
    return p
    
class Partida:
    def __init__(self):
        self.tablero = tablero_inicial()
        self.turno = 'N'
        
    def es_final(self):
        turno = self.turno
        no_turno = 'B'
        es_final = False
        if (turno=='B'):
            no_turno = 'N'
        if (not bool(self.jugadas_legales())):
            self.turno = no_turno
            if (not bool(self.jugadas_legales())):
                es_final = True
            self.turno = turno
        return es_final
              
    def esta_vacia(self,fila,columna):
        return (self.tablero[fila][columna]=='b')

    def posibles(self,fila,columna,rival):
        posibles = []
        filas = [fila-1,fila,fila+1]
        columnas = [columna-1,columna,columna+1]
        for i in filas:
            for j in columnas:
                if (0<=i<=7 and 0<=j<=7 and self.tablero[i][j]==rival):
                    posibles.append((i,j))
        return posibles

    def hay_linea(self,inicial,df,dc,turno,linea):
        i = inicial[0]+df
        j = inicial[1]+dc
        linea.append(inicial)
        if (0<=i<=7 and 0<=j<=7):
            if (self.tablero[i][j]==turno):
                return (True,linea)
            elif (self.tablero[i][j]=='b'):
                return (False,linea)
            else:
                return self.hay_linea((i,j),df,dc,turno,linea)
        else:
            return (False,linea)
            
    def jugadas_legales(self):
        turno = self.turno
        rival = 'B'
        if (turno=='B'):
            rival = 'N'
        jugadas_legales = {}
        for fila in range(0,8):
            for columna in range(0,8):
                if (self.esta_vacia(fila,columna)):
                    posibles = self.posibles(fila,columna,rival)
                    flag = False
                    for t in posibles:
                        inicial = (fila,columna)
                        df = t[0]-fila
                        dc = t[1]-columna
                        hay_linea = self.hay_linea(inicial,df,dc,turno,[])
                        if (hay_linea[0]):
                            if not flag:
                                jugadas_legales[(fila,columna)] = hay_linea[1]
                                flag = True
                            else:
                                jugadas_legales[(fila,columna)] = jugadas_legales[(fila,columna)] + hay_linea[1]
        return jugadas_legales
    
    def jugada(self,fila,columna):
        jugadas_legales = self.jugadas_legales()
        if ((fila,columna) in jugadas_legales):
            linea = jugadas_legales[(fila,columna)]
            for p in linea:
                self.tablero[p[0]][p[1]] = self.turno
            if (self.turno=='N'):
                self.turno = 'B'
            else:
                self.turno = 'N'
        else:
            print("Jugada ilegal")
            
    def contar_fichas(self,jugador):
        fichas = 0
        for i in range(0,8):
            for j in range(0,8):
                if (self.tablero[i][j]==jugador):
                    fichas = fichas + 1
        return fichas
    
    def heuristica(self,jugador):
        rival = 'N'
        if (jugador=='N'):
            rival = 'B'
        fichas_rival = self.contar_fichas(rival)
        fichas_jugador = self.contar_fichas(jugador)
        valoracion = fichas_jugador-fichas_rival
        if (not self.es_final() or valoracion==0):
            return valoracion
        else:
            return (np.sign(valoracion)*np.inf)
    
    def imprimir_tablero(self):
        sol = ""
        jugadas_legales = self.jugadas_legales()
        for i in range(0,8):
            if (i!=0):
                sol = sol + '\n'
                sol = sol + "---+---+---+---+---+---+---+---\n"
            for j in range(0,8):
                if (self.tablero[i][j]=='b' and j==7):
                    if ((i,j) in jugadas_legales):
                        sol = sol + " O " + str(i+1)
                    else:    
                        sol = sol + "   " + str(i+1)
                elif (self.tablero[i][j]=='b'):
                    if ((i,j) in jugadas_legales):
                        sol = sol + " O |"
                    else:
                        sol = sol + "   |"
                elif (j==7):
                    sol = sol + " " + self.tablero[i][j] + " " + str(i+1)
                else:
                    sol = sol + " " + self.tablero[i][j] + " |"
        sol = sol + "\n a   b   c   d   e   f   g   h "
        print(sol)
        
    def jugar(self,turno,algoritmo,profundidad):
        self.imprimir_tablero()
        if (turno==1):
            jugador = 'N'
        else:
            jugador = 'B'
        aj = Arbol_juego(self)
        while (not self.es_final()):
            jugadas_legales = self.jugadas_legales()
            if (not bool(jugadas_legales)):
                if (self.turno=='N'):
                    self.turno = 'B'
                else:
                    self.turno = 'N'
                aj.llenar_nivel()
                aj = aj.hijos[0][0]
            else:
                if (self.turno==jugador):
                    fila = int(input("Introduzca la fila (1-8): "))
                    columna = input("Introduzca la columna (a-h): ")
                    if ((fila in [1,2,3,4,5,6,7,8]) and (columna in ['a','b','c','d','e','f','g','h'])):
                        casilla = (fila-1,ord(columna)-97)        
                        if (casilla in jugadas_legales):
                            self.jugada(casilla[0],casilla[1])
                            aj.llenar_nivel()
                            for hijo in aj.hijos:
                                if (hijo[1]==casilla):
                                    aj = hijo[0]
                                    break
                            self.imprimir_tablero()
                        else:
                            print("Jugada ilegal")
                            self.imprimir_tablero()
                else:
                    print("\nTurno de la maquina")
                    aj, fila, columna = self.decision_maquina(aj,algoritmo,profundidad)
                    self.jugada(fila,columna)
                    self.imprimir_tablero()      
        final = self.heuristica(jugador)
        if (final!=0):
            if (final==np.inf):
                print("\nHas ganado")
            else:
                print("\nHas perdido")
        else:
            print("\nHas empatado")
            
    def jugar_maquinas(self,algoritmoN,profundidadN,algoritmoB,profundidadB):
        self.imprimir_tablero()
        aj = Arbol_juego(self)
        while (not self.es_final()):
            jugadas_legales = self.jugadas_legales()
            if (not bool(jugadas_legales)):
                if (self.turno=='N'):
                    self.turno = 'B'
                else:
                    self.turno = 'N'
                aj.llenar_nivel()
                aj = aj.hijos[0][0]
            else:
                if (self.turno=='N'):
                    print(f"\nTurno de {algoritmoN} {profundidadN}")
                    aj, fila, columna = self.decision_maquina(aj,algoritmoN,profundidadN)
                    self.jugada(fila,columna)
                    self.imprimir_tablero() 
                else:
                    print(f"\nTurno de {algoritmoB} {profundidadB}")
                    aj, fila, columna = self.decision_maquina(aj,algoritmoB,profundidadB)
                    self.jugada(fila,columna)
                    self.imprimir_tablero()      
        final = self.heuristica('N')
        if (final!=0):
            if (final==np.inf):
                print("\nGana N")
                return 'N'
            else:
                print("\nGana B")
                return 'B'
        else:
            print("\nEmpate")
            return "Empate"

    def decision_maquina(self,aj,algoritmo,profundidad):
        if (algoritmo=="minimax"):
            aj.minimax(profundidad,"max")
            for hijo in aj.hijos:
                if (hijo[0].evaluacion==aj.evaluacion):
                    return hijo[0], hijo[1][0], hijo[1][1]
        elif (algoritmo=="poda_ab"):
            alfa = -np.inf
            beta = np.inf
            aj.poda_alfa_beta(profundidad,alfa,beta,"max")
            for hijo in aj.hijos:
                if (hijo[0].evaluacion==aj.evaluacion):
                    return hijo[0], hijo[1][0], hijo[1][1]
        elif (algoritmo=="pvs"):
            alfa = -np.inf
            beta = np.inf
            aj.principal_variation_search(profundidad,alfa,beta,1)
            for hijo in aj.hijos:
                if (hijo[0].evaluacion==aj.evaluacion):
                    return hijo[0], hijo[1][0], hijo[1][1]
        elif (algoritmo=="MCTS"):
            h = aj.MCTS(profundidad)
            for hijo in aj.hijos:
                if (hijo[0]==h):
                    return hijo[0], hijo[1][0], hijo[1][1]
        else:
            hijo = random.choice(aj.hijos)
            return hijo[0], hijo[1][0], hijo[1][1]

class Arbol_juego:
    def __init__(self,partida):
        self.hijos = []
        self.padre = None
        self.partida = partida
        self.visitado = False
        self.evaluacion = None
        self.Q = 0
        self.N = 0

    def anadir_hijo(self,hijo,jugada):
        (self.hijos).append((hijo,jugada))

    def imprimir_hijos(self):
        for hijo in (self.hijos):
            print(hijo[1])
            (hijo[0].partida).imprimir_tablero()

    def llenar_nivel(self):
        if (len(self.hijos)==0):
            jugadas_legales = (self.partida).jugadas_legales()
            if ((not bool(jugadas_legales)) and (not (self.partida).es_final())):
                p = deepcopy(self.partida)
                if (p.turno=='N'):
                    p.turno = 'B'
                else:
                    p.turno = 'N'
                aj = Arbol_juego(p)
                aj.padre = self
                self.anadir_hijo(aj,None)
            else:
                for jugada in jugadas_legales:
                    fila = jugada[0]
                    columna = jugada[1]
                    p = deepcopy(self.partida)
                    p.jugada(fila,columna)
                    aj = Arbol_juego(p)
                    aj.padre = self
                    self.anadir_hijo(aj,jugada)
    
    def ordenar_hijos(self):
        hijos_ordenados = []
        jugador = (self.partida).turno
        if (len(self.hijos)!=0):
            hijos_ordenados.append(self.hijos[0])
            for hijo in (self.hijos[1::]):
                j = len(hijos_ordenados)
                for i in range(len(hijos_ordenados)):
                    if ((hijo[0].partida).heuristica(jugador)>(hijos_ordenados[i][0].partida).heuristica(jugador)):
                        j = i
                        break
                hijos_ordenados.insert(j,hijo)
        self.hijos = hijos_ordenados
    
    def minimax(self,profundidad,etiqueta):
        if (etiqueta=="max"):
            jugador = (self.partida).turno
        else:
            jugador = 'N'
            if ((self.partida).turno=='N'):
                jugador = 'B'
        if (profundidad==0 or (self.partida).es_final()):
            self.evaluacion = (self.partida).heuristica(jugador)
        else:
            if (etiqueta=="max"):
                valor = -np.inf
                self.llenar_nivel()
                for hijo in self.hijos:
                    (hijo[0]).minimax(profundidad-1,"min")
                    m = (hijo[0]).evaluacion
                    valor = max(valor,m)
                self.evaluacion = valor
            else:
                valor = np.inf
                self.llenar_nivel()
                for hijo in self.hijos:
                    (hijo[0]).minimax(profundidad-1,"max")
                    m = (hijo[0]).evaluacion
                    valor = min(valor,m)
                self.evaluacion = valor
        
    def poda_alfa_beta(self,profundidad,alfa,beta,etiqueta):
        if (etiqueta=="max"):
            jugador = (self.partida).turno
        else:
            jugador = 'N'
            if ((self.partida).turno=='N'):
                jugador = 'B'
        if (profundidad==0 or (self.partida).es_final()):
            self.evaluacion = (self.partida).heuristica(jugador)
        else:
            if (etiqueta=="max"):
                valor = -np.inf
                self.llenar_nivel()
                for hijo in self.hijos:
                    (hijo[0]).poda_alfa_beta(profundidad-1,alfa,beta,"min")
                    m = (hijo[0]).evaluacion
                    valor = max(valor,m)
                    if (valor>beta):
                        break
                    alfa = max(alfa,valor)
                self.evaluacion = valor
            else:
                valor = np.inf
                self.llenar_nivel()
                for hijo in self.hijos:
                    (hijo[0]).poda_alfa_beta(profundidad-1,alfa,beta,"max")
                    m = (hijo[0]).evaluacion
                    valor = min(valor,m)
                    if (valor<alfa):
                        break
                    beta = min(beta,valor)
                self.evaluacion = valor
    
    def principal_variation_search(self,profundidad,alfa,beta,lado):
        self.llenar_nivel()
        self.ordenar_hijos()
        if (lado==1):
            jugador = (self.partida).turno
        else:
            jugador = 'N'
            if ((self.partida).turno=='N'):
                jugador = 'B'
        if (profundidad==0 or (self.partida).es_final()):
            self.evaluacion = lado*(self.partida).heuristica(jugador)
        else:
            (self.hijos[0][0]).principal_variation_search(profundidad-1,-beta,-alfa,-lado)
            valor = (-1)*((self.hijos[0][0]).evaluacion)
            for hijo in (self.hijos[1::]):
                (hijo[0]).principal_variation_search(profundidad-1,-alfa-1,-alfa,-lado)
                valor = (-1)*((hijo[0]).evaluacion)
                if (alfa<valor<beta):
                    (hijo[0]).principal_variation_search(profundidad-1,-beta,-valor,-lado)
                    valor = (-1)*((hijo[0]).evaluacion)
                alfa = max(alfa,valor)
                if (alfa>=beta):
                    break
            alfa = max(alfa,valor)
            self.evaluacion = alfa
    
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
            if (N==0):
                (hijo[0].partida).imprimir_tablero()
                print((hijo[0].partida).turno)
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

def reversi():
    turno = int(input("Introduce tu turno (1-2): "))
    algoritmo = input("Introduce el algoritmo (minimax o poda_ab o pvs o MCTS o random): ")
    if (algoritmo!="MCTS"):
        profundidad = int(input("Introduce la profundidad: "))
    else:
        profundidad = int(input("Introduce el número de iteraciones: "))
    if ((turno==1 or turno==2) and (algoritmo=="minimax" or algoritmo=="poda_ab" or algoritmo=="pvs" or algoritmo=="MCTS" or algoritmo=="random")):
        partida = Partida()
        partida.jugar(turno,algoritmo,profundidad)
        
def reversi_maquinas(num_partidas,algoritmoN,profundidadN,algoritmoB,profundidadB):
    posiciones = [Partida()]
    for i in range(num_partidas-1):
        p = tablero_random(4)
        posiciones.append(p)
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
    return ((algoritmoN,profundidadN,puntos_algoritmoN),(algoritmoB,profundidadB,puntos_algoritmoB))

tope_ab = 8
tope_MCTS = 200

resultados = []
for i in range(1,tope_ab+1):
    for j in range(20,tope_MCTS+1,20):
        resultado = reversi_maquinas(20,"poda_ab",i,"MCTS",j)
        resultados.append(resultado)
