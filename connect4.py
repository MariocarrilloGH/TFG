import random
import numpy as np
from copy import deepcopy
import time

def tablero_inicial():
    t0 = []
    for i in range(0,6):
        fila = []
        for j in range(0,7):
            fila.append('b')
        t0 += [fila] 
    return t0

def tablero_random(num_jugadas):
    p = deepcopy(Partida())
    num_jugada = 0
    while (num_jugada<num_jugadas):
        jugadas_legales = p.jugadas_legales()
        jugada = random.choice(list(jugadas_legales))
        p.jugada(jugada)
        num_jugada += 1
    return p
    
class Partida:
    def __init__(self,tablero=tablero_inicial(),turno='N'):
        self.tablero = tablero
        self.turno = turno
        
    def es_final(self):
        jugadas_legales = self.jugadas_legales()
        es_final = (len(jugadas_legales)==0)
        if not es_final:
            break1 = False
            for i in range(0,3):
                if break1:
                    break
                for j in range(0,7):
                    ficha = self.tablero[i][j]
                    if (ficha!='b'):
                        linea1 = self.linea((i,j),0,-1,ficha,[])
                        linea2 = self.linea((i,j),1,-1,ficha,[])
                        linea3 = self.linea((i,j),1,0,ficha,[])
                        linea4 = self.linea((i,j),1,1,ficha,[])
                        if (len(linea1)>=4 or len(linea2)>=4 or len(linea3)>=4 or len(linea4)>=4):
                            es_final = True
                            break1 = True
                            break
            if not es_final:
                break2 = False
                for i in range(3,6):
                    if break2:
                        break
                    for j in range(0,7):
                        ficha = self.tablero[i][j]
                        if (ficha!='b'):
                            linea0 = self.linea((i,j),0,-1,ficha,[])
                            if (len(linea0)>=4):
                                es_final = True
                                break2 = True
                                break
        return es_final

    def linea(self,inicial,df,dc,ficha,linea):
        i = inicial[0]+df
        j = inicial[1]+dc
        linea.append(inicial)
        if (0<=i<=5 and 0<=j<=6):
            if (self.tablero[i][j]==ficha):
                linea = self.linea((i,j),df,dc,ficha,linea)
        return linea
            
    def jugadas_legales(self):
        jugadas_legales = []
        for j in range(0,7):
            if (self.tablero[0][j]=='b'):
                jugadas_legales.append(j)
        return jugadas_legales
    
    def jugada(self,columna):
        jugadas_legales = self.jugadas_legales()
        if (columna in jugadas_legales):
            for i in range(5,-1,-1):
                if (self.tablero[i][columna]=='b'):
                    self.tablero[i][columna] = self.turno
                    break
            if (self.turno=='N'):
                self.turno = 'B'
            else:
                self.turno = 'N'
        else:
            print("Jugada ilegal")
    
    def heuristica(self,jugador):
        lineas_2_j = 0
        lineas_3_j = 0
        lineas_2_r = 0
        lineas_3_r = 0
        break1 = False
        es_final = True
        signo = 0
        for j in range(0,7):
            if (self.tablero[0][j]=='b'):
                es_final = False
        if not es_final:
            for i in range(0,6):
                if break1:
                    break
                for j in range(0,7):
                    ficha = self.tablero[i][j]
                    if (ficha!='b'):
                        linea1 = self.linea((i,j),0,-1,ficha,[])
                        hueco_der1 = self.linea((i,j),0,1,'b',[])
                        hueco_izq1 = self.linea(linea1[-1],0,-1,'b',[])
                        posible1 = (((len(hueco_der1)-1)+(len(hueco_izq1)-1)+len(linea1))>=4)
                        linea2 = self.linea((i,j),1,-1,ficha,[])
                        hueco_der2 = self.linea((i,j),-1,1,'b',[])
                        hueco_izq2 = self.linea(linea2[-1],1,-1,'b',[])
                        posible2 = (((len(hueco_der2)-1)+(len(hueco_izq2)-1)+len(linea2))>=4)
                        linea3 = self.linea((i,j),1,0,ficha,[])
                        hueco_der3 = self.linea((i,j),-1,0,'b',[])
                        hueco_izq3 = self.linea(linea3[-1],1,0,'b',[])
                        posible3 = (((len(hueco_der3)-1)+(len(hueco_izq3)-1)+len(linea3))>=4)
                        linea4 = self.linea((i,j),1,1,ficha,[])
                        hueco_der4 = self.linea((i,j),-1,-1,'b',[])
                        hueco_izq4 = self.linea(linea4[-1],1,1,'b',[])
                        posible4 = (((len(hueco_der4)-1)+(len(hueco_izq4)-1)+len(linea4))>=4)
                        if (len(linea1)>=4 or len(linea2)>=4 or len(linea3)>=4 or len(linea4)>=4):
                            signo = -1
                            if (ficha==jugador):
                                signo = 1
                            es_final = True
                            break1 = True
                            break
                        if (ficha==jugador):
                            lineas_2_j = lineas_2_j + (len(linea1)==2 and posible1) + (len(linea2)==2 and posible2) + (len(linea3)==2 and posible3) + (len(linea4)==2 and posible4)
                            lineas_3_j = lineas_3_j + (len(linea1)==3 and posible1) + (len(linea2)==3 and posible2) + (len(linea3)==3 and posible3) + (len(linea4)==3 and posible4)
                        else:
                            lineas_2_r = lineas_2_r + (len(linea1)==2 and posible1) + (len(linea2)==2 and posible2) + (len(linea3)==2 and posible3) + (len(linea4)==2 and posible4)
                            lineas_3_r = lineas_3_r + (len(linea1)==3 and posible1) + (len(linea2)==3 and posible2) + (len(linea3)==3 and posible3) + (len(linea4)==3 and posible4)
        lineas_2_j = lineas_2_j - 2*lineas_3_j
        lineas_2_r = lineas_2_r - 2*lineas_3_r
        valoracion = (1/6)*(lineas_2_j-lineas_2_r)+(5/6)*(lineas_3_j-lineas_3_r)
        if not es_final:
            return valoracion
        elif (signo==0):
            return 0
        else:
            return (signo*np.inf)
    
    def imprimir_tablero(self):
        sol = ""
        for i in range(0,6):
            if (i!=0):
                sol = sol + '\n'
                sol = sol + "---+---+---+---+---+---+---\n"
            for j in range(0,7):
                if (self.tablero[i][j]=='b' and j==6):
                    sol = sol + "   "
                elif (self.tablero[i][j]=='b'):
                    sol = sol + "   |"
                elif (j==6):
                    sol = sol + " " + self.tablero[i][j] + " "
                else:
                    sol = sol + " " + self.tablero[i][j] + " |"
        sol = sol + "\n 1   2   3   4   5   6   7 "
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
                print("Salta el turno")
                aj.llenar_nivel()
                aj = aj.hijos[0][0]
                if (self.turno=='N'):
                    self.turno = 'B'
                else:
                    self.turno = 'N'
                self.imprimir_tablero()
            else:
                if (self.turno==jugador):
                    columna = int(input("Introduzca la columna (1-7): "))
                    if (columna in [1,2,3,4,5,6,7,8]):
                        columna = columna-1      
                        if (columna in jugadas_legales):
                            self.jugada(columna)
                            aj.llenar_nivel()
                            for hijo in aj.hijos:
                                if (hijo[1]==columna):
                                    aj = hijo[0]
                                    break
                            self.imprimir_tablero()
                        else:
                            print("Jugada ilegal")
                            self.imprimir_tablero()
                else:
                    print("\nTurno de la maquina")
                    aj, columna = self.decision_maquina(aj,algoritmo,profundidad)
                    self.jugada(columna)
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
                print("Salta el turno")
                aj.llenar_nivel()
                aj = aj.hijos[0][0]
                if (self.turno=='N'):
                    self.turno = 'B'
                else:
                    self.turno = 'N'
                self.imprimir_tablero()
            else:
                if (self.turno=='N'):
                    print(f"\nTurno de {algoritmoN} {profundidadN}")
                    aj, columna = self.decision_maquina(aj,algoritmoN,profundidadN)
                    self.jugada(columna)
                    self.imprimir_tablero() 
                else:
                    print(f"\nTurno de {algoritmoB} {profundidadB}")
                    aj, columna = self.decision_maquina(aj,algoritmoB,profundidadB)
                    self.jugada(columna)
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
                    return hijo[0], hijo[1]
        elif (algoritmo=="poda_ab"):
            alfa = -np.inf
            beta = np.inf
            aj.poda_alfa_beta(profundidad,alfa,beta,"max")
            for hijo in aj.hijos:
                if (hijo[0].evaluacion==aj.evaluacion):
                    return hijo[0], hijo[1]
        elif (algoritmo=="pvs"):
            alfa = -np.inf
            beta = np.inf
            aj.principal_variation_search(profundidad,alfa,beta,1)
            for hijo in aj.hijos:
                if (hijo[0].evaluacion==aj.evaluacion):
                    return hijo[0], hijo[1]
        elif (algoritmo=="MCTS"):
            h = aj.MCTS(profundidad)
            for hijo in aj.hijos:
                if (hijo[0]==h):
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
                    p = deepcopy(self.partida)
                    p.jugada(jugada)
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

def connect4():
    turno = int(input("Introduce tu turno (1-2): "))
    algoritmo = input("Introduce el algoritmo (minimax o poda_ab o pvs o MCTS o random): ")
    if (algoritmo!="MCTS"):
        profundidad = int(input("Introduce la profundidad: "))
    else:
        profundidad = int(input("Introduce el número de iteraciones: "))
    if ((turno==1 or turno==2) and (algoritmo=="minimax" or algoritmo=="poda_ab" or algoritmo=="pvs" or algoritmo=="MCTS" or algoritmo=="random")):
        partida = Partida()
        partida.jugar(turno,algoritmo,profundidad)
        
def connect4_maquinas(posiciones,algoritmoN,profundidadN,algoritmoB,profundidadB):
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


tiempos_poda_ab = {'poda_ab 3': 0.02862707773844401,
'poda_ab 4': 0.10944980382919312,
'poda_ab 5': 0.47460474967956545,
'poda_ab 6': 1.9352927684783936,
'poda_ab 7': 6.156408965587616}

tiempos_MCTS = {'MCTS 8': 0.024524075644356862,
'MCTS 40': 0.10873668844049628,
'MCTS 170': 0.473487483130561,
'MCTS 590': 1.9196439981460571,
'MCTS 1750': 6.1677347880143385}
    
p0 = deepcopy(Partida())
p1 = Partida([['b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'N', 'b'],['b', 'B', 'b', 'b', 'N', 'B', 'N']],'B')
p2 = Partida([['b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'N', 'b'],['b', 'B', 'b', 'b', 'b', 'N', 'b'],['b', 'B', 'b', 'N', 'N', 'B', 'b']],'B')
p3 = Partida([['b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'N'],['b', 'b', 'b', 'b', 'b', 'N', 'B'],['b', 'N', 'b', 'b', 'B', 'B', 'N']],'B')
p4 = Partida([['b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'N', 'b', 'b'],['b', 'b', 'b', 'b', 'B', 'b', 'N'],['b', 'B', 'b', 'N', 'B', 'b', 'N']],'B')
p5 = Partida([['b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'B', 'b', 'b'],['N', 'b', 'B', 'N', 'N', 'B', 'N']],'B')
p6 = Partida([['b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'N'],['N', 'N', 'B', 'b', 'B', 'N', 'B']],'B')
p7 = Partida([['b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'B', 'b', 'B', 'b', 'N'],['b', 'b', 'N', 'N', 'B', 'B', 'N']],'N')
p8 = Partida([['b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'N', 'b'],['b', 'B', 'b', 'b', 'b', 'B', 'b'],['N', 'B', 'b', 'B', 'b', 'N', 'N']],'N')
p9 = Partida([['b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'N', 'b'],['b', 'B', 'b', 'b', 'b', 'B', 'b'],['N', 'N', 'b', 'B', 'N', 'N', 'B']],'B')

posiciones_iniciales = [p0,p1,p2,p3,p4,p5,p6,p7,p8,p9]


"""resultados1AM = []
for i in [3,4,5,6,7]:
    for j in [8,40,170,590,1750]:
        posiciones = deepcopy(posiciones_iniciales)
        resultado = connect4_maquinas(posiciones,"poda_ab",i,"MCTS",j)
        resultados1AM.append(resultado)

resultados2AM = []
for i in [3,4,5,6,7]:
    for j in [8,40,170,590,1750]:
        posiciones = deepcopy(posiciones_iniciales)
        resultado = connect4_maquinas(posiciones,"MCTS",j,"poda_ab",i)
        resultados2AM.append(resultado)

resultadosAM = []
for r1 in resultados1AM:
    for r2 in resultados2AM:
        if (r1[0][0]==r2[1][0] and r1[1][0]==r2[0][0]):
            resultadosAM.append(((r1[0][0],r1[0][1]+r2[1][1]),(r2[0][0],r1[1][1]+r2[0][1])))"""
           
resultados1AM = [((('poda_ab', 3), 10), (('MCTS', 8), 0)),
((('poda_ab', 3), 9), (('MCTS', 40), 1)),
((('poda_ab', 3), 7), (('MCTS', 170), 3)),
((('poda_ab', 3), 7), (('MCTS', 590), 3)),
((('poda_ab', 3), 7), (('MCTS', 1750), 3)),
((('poda_ab', 4), 10), (('MCTS', 8), 0)),
((('poda_ab', 4), 9), (('MCTS', 40), 1)),
((('poda_ab', 4), 8), (('MCTS', 170), 2)),
((('poda_ab', 4), 7.5), (('MCTS', 590), 2.5)),
((('poda_ab', 4), 8), (('MCTS', 1750), 2)),
((('poda_ab', 5), 10), (('MCTS', 8), 0)),
((('poda_ab', 5), 10), (('MCTS', 40), 0)),
((('poda_ab', 5), 8), (('MCTS', 170), 2)),
((('poda_ab', 5), 8.5), (('MCTS', 590), 1.5)),
((('poda_ab', 5), 9), (('MCTS', 1750), 1)),
((('poda_ab', 6), 10), (('MCTS', 8), 0)),
((('poda_ab', 6), 10), (('MCTS', 40), 0)),
((('poda_ab', 6), 8), (('MCTS', 170), 2)),
((('poda_ab', 6), 8.5), (('MCTS', 590), 1.5)),
((('poda_ab', 6), 10), (('MCTS', 1750), 0)),
((('poda_ab', 7), 10), (('MCTS', 8), 0)),
((('poda_ab', 7), 9), (('MCTS', 40), 1)),
((('poda_ab', 7), 9), (('MCTS', 170), 1)),
((('poda_ab', 7), 9), (('MCTS', 590), 1)),
((('poda_ab', 7), 10), (('MCTS', 1750), 0))]

resultados2AM = [((('MCTS', 8), 1), (('poda_ab', 3), 9)),
((('MCTS', 40), 2), (('poda_ab', 3), 8)),
((('MCTS', 170), 5), (('poda_ab', 3), 5)),
((('MCTS', 590), 5), (('poda_ab', 3), 5)),
((('MCTS', 1750), 4), (('poda_ab', 3), 6)),
((('MCTS', 8), 0), (('poda_ab', 4), 10)),
((('MCTS', 40), 1), (('poda_ab', 4), 9)),
((('MCTS', 170), 2), (('poda_ab', 4), 8)),
((('MCTS', 590), 7), (('poda_ab', 4), 3)),
((('MCTS', 1750), 2), (('poda_ab', 4), 8)),
((('MCTS', 8), 0), (('poda_ab', 5), 10)),
((('MCTS', 40), 1), (('poda_ab', 5), 9)),
((('MCTS', 170), 2), (('poda_ab', 5), 8)),
((('MCTS', 590), 1), (('poda_ab', 5), 9)),
((('MCTS', 1750), 0), (('poda_ab', 5), 10)),
((('MCTS', 8), 0), (('poda_ab', 6), 10)),
((('MCTS', 40), 0), (('poda_ab', 6), 10)),
((('MCTS', 170), 3), (('poda_ab', 6), 7)),
((('MCTS', 590), 0), (('poda_ab', 6), 10)),
((('MCTS', 1750), 1), (('poda_ab', 6), 9)),
((('MCTS', 8), 0), (('poda_ab', 7), 10)),
((('MCTS', 40), 0), (('poda_ab', 7), 10)),
((('MCTS', 170), 1), (('poda_ab', 7), 9)),
((('MCTS', 590), 1), (('poda_ab', 7), 9)),
((('MCTS', 1750), 1), (('poda_ab', 7), 9))]

resultadosAM = [((('poda_ab', 3), 19), (('MCTS', 8), 1)),
((('poda_ab', 3), 17), (('MCTS', 40), 3)),
((('poda_ab', 3), 12), (('MCTS', 170), 8)),
((('poda_ab', 3), 12), (('MCTS', 590), 8)),
((('poda_ab', 3), 13), (('MCTS', 1750), 7)),
((('poda_ab', 4), 20), (('MCTS', 8), 0)),
((('poda_ab', 4), 18), (('MCTS', 40), 2)),
((('poda_ab', 4), 16), (('MCTS', 170), 4)),
((('poda_ab', 4), 10.5), (('MCTS', 590), 9.5)),
((('poda_ab', 4), 16), (('MCTS', 1750), 4)),
((('poda_ab', 5), 20), (('MCTS', 8), 0)),
((('poda_ab', 5), 19), (('MCTS', 40), 1)),
((('poda_ab', 5), 16), (('MCTS', 170), 4)),
((('poda_ab', 5), 17.5), (('MCTS', 590), 2.5)),
((('poda_ab', 5), 19), (('MCTS', 1750), 1)),
((('poda_ab', 6), 20), (('MCTS', 8), 0)),
((('poda_ab', 6), 20), (('MCTS', 40), 0)),
((('poda_ab', 6), 15), (('MCTS', 170), 5)),
((('poda_ab', 6), 18.5), (('MCTS', 590), 1.5)),
((('poda_ab', 6), 19), (('MCTS', 1750), 1)),
((('poda_ab', 7), 20), (('MCTS', 8), 0)),
((('poda_ab', 7), 19), (('MCTS', 40), 1)),
((('poda_ab', 7), 18), (('MCTS', 170), 2)),
((('poda_ab', 7), 18), (('MCTS', 590), 2)),
((('poda_ab', 7), 19), (('MCTS', 1750), 1))] #Resultados de ejecutar el código de arriba


"""resultados1AA = []
v = [3,4,5,6,7]
for i in [3,4,5,6,7]:
    v.remove(i)
    for j in v:
        posiciones = deepcopy(posiciones_iniciales)
        resultado = connect4_maquinas(posiciones,"poda_ab",i,"poda_ab",j)
        resultados1AA.append(resultado)

resultados2AA = []
v = [3,4,5,6,7]
for i in [3,4,5,6,7]:
    v.remove(i)
    for j in v:
        posiciones = deepcopy(posiciones_iniciales)
        resultado = connect4_maquinas(posiciones,"poda_ab",j,"poda_ab",i)
        resultados2AA.append(resultado)

resultadosAA = []
for r1 in resultados1AA:
    for r2 in resultados2AA:
        if (r1[0][0]==r2[1][0] and r1[1][0]==r2[0][0]):
            resultadosAA.append(((r1[0][0],r1[0][1]+r2[1][1]),(r2[0][0],r1[1][1]+r2[0][1])))"""
            
resultados1AA = [((('poda_ab', 3), 3), (('poda_ab', 4), 7)),
((('poda_ab', 3), 3), (('poda_ab', 5), 7)),
((('poda_ab', 3), 0.5), (('poda_ab', 6), 9.5)),
((('poda_ab', 3), 1.5), (('poda_ab', 7), 8.5)),
((('poda_ab', 4), 4.5), (('poda_ab', 5), 5.5)),
((('poda_ab', 4), 4), (('poda_ab', 6), 6)),
((('poda_ab', 4), 4.5), (('poda_ab', 7), 5.5)),
((('poda_ab', 5), 2), (('poda_ab', 6), 8)),
((('poda_ab', 5), 3.5), (('poda_ab', 7), 6.5)),
((('poda_ab', 6), 5.5), (('poda_ab', 7), 4.5))]

resultados2AA = [((('poda_ab', 4), 6.0), (('poda_ab', 3), 4.0)),
((('poda_ab', 5), 8), (('poda_ab', 3), 2)),
((('poda_ab', 6), 8), (('poda_ab', 3), 2)),
((('poda_ab', 7), 10), (('poda_ab', 3), 0)),
((('poda_ab', 5), 4.5), (('poda_ab', 4), 5.5)),
((('poda_ab', 6), 8), (('poda_ab', 4), 2)),
((('poda_ab', 7), 9), (('poda_ab', 4), 1)),
((('poda_ab', 6), 4.5), (('poda_ab', 5), 5.5)),
((('poda_ab', 7), 7), (('poda_ab', 5), 3)),
((('poda_ab', 7), 7.0), (('poda_ab', 6), 3.0))]

resultadosAA = [((('poda_ab', 3), 7.0), (('poda_ab', 4), 13.0)),
((('poda_ab', 3), 5), (('poda_ab', 5), 15)),
((('poda_ab', 3), 2.5), (('poda_ab', 6), 17.5)),
((('poda_ab', 3), 1.5), (('poda_ab', 7), 18.5)),
((('poda_ab', 4), 10.0), (('poda_ab', 5), 10.0)),
((('poda_ab', 4), 6), (('poda_ab', 6), 14)),
((('poda_ab', 4), 5.5), (('poda_ab', 7), 14.5)),
((('poda_ab', 5), 7.5), (('poda_ab', 6), 12.5)),
((('poda_ab', 5), 6.5), (('poda_ab', 7), 13.5)),
((('poda_ab', 6), 8.5), (('poda_ab', 7), 11.5))] #Resultados de ejecutar el código de arriba

  
"""resultados1MM = []
v = [8,40,170,590,1750]
for i in [8,40,170,590,1750]:
    v.remove(i)
    for j in v:
        posiciones = deepcopy(posiciones_iniciales)
        resultado = connect4_maquinas(posiciones,"MCTS",i,"MCTS",j)
        resultados1MM.append(resultado)

resultados2MM = []
v = [8,40,170,590,1750]
for i in [8,40,170,590,1750]:
    v.remove(i)
    for j in v:
        posiciones = deepcopy(posiciones_iniciales)
        resultado = connect4_maquinas(posiciones,"MCTS",j,"MCTS",i)
        resultados2MM.append(resultado)

resultadosMM = []
for r1 in resultados1MM:
    for r2 in resultados2MM:
        if (r1[0][0]==r2[1][0] and r1[1][0]==r2[0][0]):
            resultadosMM.append(((r1[0][0],r1[0][1]+r2[1][1]),(r2[0][0],r1[1][1]+r2[0][1])))"""
            
resultados1MM = [((('MCTS', 8), 0), (('MCTS', 40), 10)),
((('MCTS', 8), 0), (('MCTS', 170), 10)),
((('MCTS', 8), 0), (('MCTS', 590), 10)),
((('MCTS', 8), 0), (('MCTS', 1750), 10)),
((('MCTS', 40), 0), (('MCTS', 170), 10)),
((('MCTS', 40), 0), (('MCTS', 590), 10)),
((('MCTS', 40), 0), (('MCTS', 1750), 10)),
((('MCTS', 170), 1), (('MCTS', 590), 9)),
((('MCTS', 170), 0), (('MCTS', 1750), 10)),
((('MCTS', 590), 2), (('MCTS', 1750), 8))]

resultados2MM = [((('MCTS', 40), 10), (('MCTS', 8), 0)),
((('MCTS', 170), 10), (('MCTS', 8), 0)),
((('MCTS', 590), 10), (('MCTS', 8), 0)),
((('MCTS', 1750), 10), (('MCTS', 8), 0)),
((('MCTS', 170), 10), (('MCTS', 40), 0)),
((('MCTS', 590), 10), (('MCTS', 40), 0)),
((('MCTS', 1750), 10), (('MCTS', 40), 0)),
((('MCTS', 590), 9), (('MCTS', 170), 1)),
((('MCTS', 1750), 10), (('MCTS', 170), 0)),
((('MCTS', 1750), 9), (('MCTS', 590), 1))]

resultadosMM = [((('MCTS', 8), 0), (('MCTS', 40), 20)),
((('MCTS', 8), 0), (('MCTS', 170), 20)),
((('MCTS', 8), 0), (('MCTS', 590), 20)),
((('MCTS', 8), 0), (('MCTS', 1750), 20)),
((('MCTS', 40), 0), (('MCTS', 170), 20)),
((('MCTS', 40), 0), (('MCTS', 590), 20)),
((('MCTS', 40), 0), (('MCTS', 1750), 20)),
((('MCTS', 170), 2), (('MCTS', 590), 18)),
((('MCTS', 170), 0), (('MCTS', 1750), 20)),
((('MCTS', 590), 3), (('MCTS', 1750), 17))] #Resultados de ejecutar el código de arriba
        
        
"""resultados1MR = []
for i in [8,40,170,590,1750]:
    posiciones = deepcopy(posiciones_iniciales)
    resultado = connect4_maquinas(posiciones,"MCTS",i,"random",0)
    resultados1MR.append(resultado)

resultados2MR = []
for i in [8,40,170,590,1750]:
    posiciones = deepcopy(posiciones_iniciales)
    resultado = connect4_maquinas(posiciones,"random",0,"MCTS",i)
    resultados2MR.append(resultado)

resultadosMR = []
for r1 in resultados1MR:
    for r2 in resultados2MR:
        if (r1[0][0]==r2[1][0] and r1[1][0]==r2[0][0]):
            resultadosMR.append(((r1[0][0],r1[0][1]+r2[1][1]),(r2[0][0],r1[1][1]+r2[0][1])))"""
            
resultados1MR = [((('MCTS', 8), 8), (('random', 0), 2)),
((('MCTS', 40), 8), (('random', 0), 2)),
((('MCTS', 170), 10), (('random', 0), 0)),
((('MCTS', 590), 10), (('random', 0), 0)),
((('MCTS', 1750), 10), (('random', 0), 0))]

resultados2MR = [((('random', 0), 3), (('MCTS', 8), 7)),
((('random', 0), 0), (('MCTS', 40), 10)),
((('random', 0), 0), (('MCTS', 170), 10)),
((('random', 0), 0), (('MCTS', 590), 10)),
((('random', 0), 0), (('MCTS', 1750), 10))]

resultadosMR = [((('MCTS', 8), 15), (('random', 0), 5)),
((('MCTS', 40), 18), (('random', 0), 2)),
((('MCTS', 170), 20), (('random', 0), 0)),
((('MCTS', 590), 20), (('random', 0), 0)),
((('MCTS', 1750), 20), (('random', 0), 0))] #Resultados de ejecutar el código de arriba


"""resultados1AR = []
for i in [3,4,5,6,7]:
    posiciones = deepcopy(posiciones_iniciales)
    resultado = connect4_maquinas(posiciones,"poda_ab",i,"random",0)
    resultados1AR.append(resultado)

resultados2AR = []
for i in [3,4,5,6,7]:
    posiciones = deepcopy(posiciones_iniciales)
    resultado = connect4_maquinas(posiciones,"random",0,"poda_ab",i)
    resultados2AR.append(resultado)

resultadosAR = []
for r1 in resultados1AR:
    for r2 in resultados2AR:
        if (r1[0][0]==r2[1][0] and r1[1][0]==r2[0][0]):
            resultadosAR.append(((r1[0][0],r1[0][1]+r2[1][1]),(r2[0][0],r1[1][1]+r2[0][1])))"""
            
resultados1AR = [((('poda_ab', 3), 10), (('random', 0), 0)),
((('poda_ab', 4), 10), (('random', 0), 0)),
((('poda_ab', 5), 10), (('random', 0), 0)),
((('poda_ab', 6), 10), (('random', 0), 0)),
((('poda_ab', 7), 10), (('random', 0), 0))]

resultados2AR = [((('random', 0), 0), (('poda_ab', 3), 10)),
((('random', 0), 0), (('poda_ab', 4), 10)),
((('random', 0), 0), (('poda_ab', 5), 10)),
((('random', 0), 0), (('poda_ab', 6), 10)),
((('random', 0), 0), (('poda_ab', 7), 10))]

resultadosAR = [((('poda_ab', 3), 20), (('random', 0), 0)),
((('poda_ab', 4), 20), (('random', 0), 0)),
((('poda_ab', 5), 20), (('random', 0), 0)),
((('poda_ab', 6), 20), (('random', 0), 0)),
((('poda_ab', 7), 20), (('random', 0), 0))] #Resultados de ejecutar el código de arriba

