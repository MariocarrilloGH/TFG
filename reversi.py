import random
import numpy as np
from copy import deepcopy
from PIL import Image
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
    p = deepcopy(Partida())
    num_jugada = 0
    while (num_jugada<num_jugadas):
        jugadas_legales = p.jugadas_legales()
        jugada = random.choice(list(jugadas_legales))
        p.jugada(jugada[0],jugada[1])
        num_jugada += 1
    return p
    
class Partida:
    def __init__(self,tablero=tablero_inicial(),turno='N'):
        self.tablero = tablero
        self.turno = turno
        
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
        
    def imagen_tablero(self):
        tablero_vacio = Image.open("tablero_vacio_reversi.png")
        N = Image.open("N.png")
        B = Image.open("B.png")
        for i in range(0,8):
            for j in range(0,8):
                if (self.tablero[i][j]!='b'):
                    coordenada_X = 2+2+(32*j)
                    coordenada_Y = 2+2+(32*i)
                    if (self.tablero[i][j]=='N'):
                        tablero_vacio.paste(N,(coordenada_X,coordenada_Y))
                    else:
                        tablero_vacio.paste(B,(coordenada_X,coordenada_Y))
        archivo = input("Introduce el nombre del archivo: ")
        tablero_vacio.save(archivo+".png") 
        
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
                    p = deepcopy(hijo[0].partida)
                    aj = Arbol_juego(p)
                    return aj, hijo[1][0], hijo[1][1]
        else:
            aj.llenar_nivel()
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
            
    def imagen_hijos(self):
        for hijo in (self.hijos):
            (hijo[0].partida).imagen_tablero()

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
        es_el_primero = True
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
            for hijo in self.hijos:
                if es_el_primero:
                    (hijo[0]).principal_variation_search(profundidad-1,-beta,-alfa,-lado)
                    valor = (-1)*((hijo[0]).evaluacion)
                    es_el_primero = False
                else:
                    (hijo[0]).principal_variation_search(profundidad-1,-alfa-1,-alfa,-lado)
                    valor = (-1)*((hijo[0]).evaluacion)
                    if (alfa<valor<beta):
                        (hijo[0]).principal_variation_search(profundidad-1,-beta,-valor,-lado)
                        valor = (-1)*((hijo[0]).evaluacion)
                alfa = max(alfa,valor)
                if (alfa>=beta):
                    break
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
        
def reversi_maquinas(posiciones,algoritmoN,profundidadN,algoritmoB,profundidadB):
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


tiempos_poda_ab = {'poda_ab 2': 0.030983233451843263,
'poda_ab 3': 0.17031026970256458,
'poda_ab 4': 1.1829345533924718,
'poda_ab 5': 2.423319237572806,
'poda_ab 6': 15.855559428532919}

tiempos_MCTS = {'MCTS 1': 0.0805530865987142,
'MCTS 3': 0.17514230410257975,
'MCTS 13': 1.2137874480216735,
'MCTS 26': 2.3641257593708653,
'MCTS 170': 15.709569854121055}  

p0 = deepcopy(Partida())
p1 = Partida([['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'N', 'b', 'b'],['b', 'b', 'b', 'B', 'N', 'B', 'b', 'b'],['b', 'b', 'b', 'N', 'B', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'N', 'B', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b']])
p2 = Partida([['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'B', 'b', 'b', 'b'],['b', 'b', 'N', 'B', 'N', 'N', 'b', 'b'],['b', 'b', 'B', 'B', 'B', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b']])
p3 = Partida([['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'B', 'N', 'b', 'b', 'b'],['b', 'b', 'b', 'B', 'N', 'b', 'b', 'b'],['b', 'b', 'N', 'B', 'N', 'b', 'b', 'b'],['b', 'b', 'b', 'B', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b']])
p4 = Partida([['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'N', 'b', 'b', 'b', 'b'],['b', 'b', 'B', 'B', 'B', 'B', 'b', 'b'],['b', 'b', 'b', 'N', 'N', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'N', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b']])
p5 = Partida([['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'N', 'B', 'b', 'b', 'b'],['b', 'b', 'b', 'N', 'B', 'b', 'b', 'b'],['b', 'b', 'N', 'B', 'B', 'b', 'b', 'b'],['b', 'N', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b']])
p6 = Partida([['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'B', 'b', 'b', 'b'],['b', 'b', 'N', 'B', 'N', 'N', 'b', 'b'],['b', 'b', 'B', 'B', 'B', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b']])
p7 = Partida([['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'B', 'B', 'B', 'b', 'b'],['b', 'b', 'N', 'N', 'B', 'b', 'b', 'b'],['b', 'b', 'b', 'B', 'N', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b']])
p8 = Partida([['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'N', 'b', 'b'],['b', 'b', 'b', 'b', 'N', 'b', 'b', 'b'],['b', 'b', 'N', 'N', 'B', 'b', 'b', 'b'],['b', 'b', 'b', 'B', 'B', 'b', 'b', 'b'],['b', 'b', 'B', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b']])
p9 = Partida([['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'B', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'B', 'B', 'N', 'b', 'b', 'b'],['b', 'b', 'B', 'N', 'N', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'N', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b']])

posiciones_iniciales = [p0,p1,p2,p3,p4,p5,p6,p7,p8,p9]


"""resultados1AM = []
for i in [2,3,4,5,6]:
    for j in [1,3,13,26,170]:
        posiciones = deepcopy(posiciones_iniciales)
        resultado = reversi_maquinas(posiciones,"poda_ab",i,"MCTS",j)
        resultados1AM.append(resultado)

resultados2AM = []
for i in [2,3,4,5,6]:
    for j in [1,3,13,26,170]:
        posiciones = deepcopy(posiciones_iniciales)
        resultado = reversi_maquinas(posiciones,"MCTS",j,"poda_ab",i)
        resultados2AM.append(resultado)

resultadosAM = []
for r1 in resultados1AM:
    for r2 in resultados2AM:
        if (r1[0][0]==r2[1][0] and r1[1][0]==r2[0][0]):
            resultadosAM.append(((r1[0][0],r1[0][1]+r2[1][1]),(r2[0][0],r1[1][1]+r2[0][1])))"""

resultados1AM = [((('poda_ab', 2), 8), (('MCTS', 1), 2)),
((('poda_ab', 2), 7), (('MCTS', 3), 3)),
((('poda_ab', 2), 3), (('MCTS', 13), 7)),
((('poda_ab', 2), 0), (('MCTS', 26), 10)),
((('poda_ab', 2), 2), (('MCTS', 170), 8)),
((('poda_ab', 3), 7.5), (('MCTS', 1), 2.5)),
((('poda_ab', 3), 6.5), (('MCTS', 3), 3.5)),
((('poda_ab', 3), 6.5), (('MCTS', 13), 3.5)),
((('poda_ab', 3), 4), (('MCTS', 26), 6)),
((('poda_ab', 3), 0), (('MCTS', 170), 10)),
((('poda_ab', 4), 7), (('MCTS', 1), 3)),
((('poda_ab', 4), 10), (('MCTS', 3), 0)),
((('poda_ab', 4), 6), (('MCTS', 13), 4)),
((('poda_ab', 4), 4), (('MCTS', 26), 6)),
((('poda_ab', 4), 4), (('MCTS', 170), 6)),
((('poda_ab', 5), 9), (('MCTS', 1), 1)),
((('poda_ab', 5), 8), (('MCTS', 3), 2)),
((('poda_ab', 5), 8), (('MCTS', 13), 2)),
((('poda_ab', 5), 2), (('MCTS', 26), 8)),
((('poda_ab', 5), 2), (('MCTS', 170), 8)),
((('poda_ab', 6), 10), (('MCTS', 1), 0)),
((('poda_ab', 6), 9), (('MCTS', 3), 1)),
((('poda_ab', 6), 6), (('MCTS', 13), 4)),
((('poda_ab', 6), 3), (('MCTS', 26), 7)), 
((('poda_ab', 6), 3), (('MCTS', 170), 7))]

resultados2AM = [((('MCTS', 1), 4), (('poda_ab', 2), 6)),
((('MCTS', 3), 2.5), (('poda_ab', 2), 7.5)),
((('MCTS', 13), 7), (('poda_ab', 2), 3)),
((('MCTS', 26), 10), (('poda_ab', 2), 0)),
((('MCTS', 170), 10), (('poda_ab', 2), 0)),
((('MCTS', 1), 3.5), (('poda_ab', 3), 6.5)),
((('MCTS', 3), 0), (('poda_ab', 3), 10)),
((('MCTS', 13), 4), (('poda_ab', 3), 6)),
((('MCTS', 26), 7), (('poda_ab', 3), 3)),
((('MCTS', 170), 9), (('poda_ab', 3), 1)),
((('MCTS', 1), 1), (('poda_ab', 4), 9)),
((('MCTS', 3), 2), (('poda_ab', 4), 8)),
((('MCTS', 13), 7), (('poda_ab', 4), 3)),
((('MCTS', 26), 7), (('poda_ab', 4), 3)),
((('MCTS', 170), 10), (('poda_ab', 4), 0)),
((('MCTS', 1), 0), (('poda_ab', 5), 10)),
((('MCTS', 3), 0.5), (('poda_ab', 5), 9.5)),
((('MCTS', 13), 1), (('poda_ab', 5), 9)),
((('MCTS', 26), 4.5), (('poda_ab', 5), 5.5)),
((('MCTS', 170), 8), (('poda_ab', 5), 2)),
((('MCTS', 1), 3), (('poda_ab', 6), 7)),
((('MCTS', 3), 0), (('poda_ab', 6), 10)),
((('MCTS', 13), 4), (('poda_ab', 6), 6)),
((('MCTS', 26), 3), (('poda_ab', 6), 7)),
((('MCTS', 170), 9), (('poda_ab', 6), 1))]

resultadosAM = [((('poda_ab', 2), 14), (('MCTS', 1), 6)),
((('poda_ab', 2), 14.5), (('MCTS', 3), 5.5)),
((('poda_ab', 2), 6), (('MCTS', 13), 14)),
((('poda_ab', 2), 0), (('MCTS', 26), 20)),
((('poda_ab', 2), 2), (('MCTS', 170), 18)),
((('poda_ab', 3), 14.0), (('MCTS', 1), 6.0)),
((('poda_ab', 3), 16.5), (('MCTS', 3), 3.5)),
((('poda_ab', 3), 12.5), (('MCTS', 13), 7.5)),
((('poda_ab', 3), 7), (('MCTS', 26), 13)),
((('poda_ab', 3), 1), (('MCTS', 170), 19)),
((('poda_ab', 4), 16), (('MCTS', 1), 4)),
((('poda_ab', 4), 18), (('MCTS', 3), 2)),
((('poda_ab', 4), 9), (('MCTS', 13), 11)),
((('poda_ab', 4), 7), (('MCTS', 26), 13)),
((('poda_ab', 4), 4), (('MCTS', 170), 16)),
((('poda_ab', 5), 19), (('MCTS', 1), 1)),
((('poda_ab', 5), 17.5), (('MCTS', 3), 2.5)),
((('poda_ab', 5), 17), (('MCTS', 13), 3)),
((('poda_ab', 5), 7.5), (('MCTS', 26), 12.5)),
((('poda_ab', 5), 4), (('MCTS', 170), 16)),
((('poda_ab', 6), 17), (('MCTS', 1), 3)),
((('poda_ab', 6), 19), (('MCTS', 3), 1)),
((('poda_ab', 6), 12), (('MCTS', 13), 8)),
((('poda_ab', 6), 10), (('MCTS', 26), 10)),
((('poda_ab', 6), 4), (('MCTS', 170), 16))] #Resultados de ejecutar el código de arriba


"""resultados1AA = []
v = [2,3,4,5,6]
for i in [2,3,4,5,6]:
    v.remove(i)
    for j in v:
        posiciones = deepcopy(posiciones_iniciales)
        resultado = reversi_maquinas(posiciones,"poda_ab",i,"poda_ab",j)
        resultados1AA.append(resultado)

resultados2AA = []
v = [2,3,4,5,6]
for i in [2,3,4,5,6]:
    v.remove(i)
    for j in v:
        posiciones = deepcopy(posiciones_iniciales)
        resultado = reversi_maquinas(posiciones,"poda_ab",j,"poda_ab",i)
        resultados2AA.append(resultado)

resultadosAA = []
for r1 in resultados1AA:
    for r2 in resultados2AA:
        if (r1[0][0]==r2[1][0] and r1[1][0]==r2[0][0]):
            resultadosAA.append(((r1[0][0],r1[0][1]+r2[1][1]),(r2[0][0],r1[1][1]+r2[0][1])))"""

resultados1AA = [((('poda_ab', 2), 1), (('poda_ab', 3), 9)),
((('poda_ab', 2), 3.5), (('poda_ab', 4), 6.5)),
((('poda_ab', 2), 1), (('poda_ab', 5), 9)),
((('poda_ab', 2), 2), (('poda_ab', 6), 8)),
((('poda_ab', 3), 5), (('poda_ab', 4), 5)),
((('poda_ab', 3), 1), (('poda_ab', 5), 9)),
((('poda_ab', 3), 0), (('poda_ab', 6), 10)),
((('poda_ab', 4), 3), (('poda_ab', 5), 7)),
((('poda_ab', 4), 1), (('poda_ab', 6), 9)),
((('poda_ab', 5), 4), (('poda_ab', 6), 6))]   

resultados2AA = [((('poda_ab', 3), 3), (('poda_ab', 2), 7)),
((('poda_ab', 4), 8), (('poda_ab', 2), 2)),
((('poda_ab', 5), 7), (('poda_ab', 2), 3)),
((('poda_ab', 6), 8), (('poda_ab', 2), 2)),
((('poda_ab', 4), 5), (('poda_ab', 3), 5)),
((('poda_ab', 5), 8), (('poda_ab', 3), 2)),
((('poda_ab', 6), 9), (('poda_ab', 3), 1)),
((('poda_ab', 5), 8), (('poda_ab', 4), 2)),
((('poda_ab', 6), 7), (('poda_ab', 4), 3)),
((('poda_ab', 6), 5), (('poda_ab', 5), 5))]      

resultadosAA = [((('poda_ab', 2), 8), (('poda_ab', 3), 12)),
((('poda_ab', 2), 5.5), (('poda_ab', 4), 14.5)),
((('poda_ab', 2), 4), (('poda_ab', 5), 16)),
((('poda_ab', 2), 4), (('poda_ab', 6), 16)),
((('poda_ab', 3), 10), (('poda_ab', 4), 10)),
((('poda_ab', 3), 3), (('poda_ab', 5), 17)),
((('poda_ab', 3), 1), (('poda_ab', 6), 19)),
((('poda_ab', 4), 5), (('poda_ab', 5), 15)),
((('poda_ab', 4), 4), (('poda_ab', 6), 16)),
((('poda_ab', 5), 9), (('poda_ab', 6), 11))] #Resultados de ejecutar el código de arriba

  
"""resultados1MM = []
v = [1,3,13,26,170]
for i in [1,3,13,26,170]:
    v.remove(i)
    for j in v:
        posiciones = deepcopy(posiciones_iniciales)
        resultado = reversi_maquinas(posiciones,"MCTS",i,"MCTS",j)
        resultados1MM.append(resultado)

resultados2MM = []
v = [1,3,13,26,170]
for i in [1,3,13,26,170]:
    v.remove(i)
    for j in v:
        posiciones = deepcopy(posiciones_iniciales)
        resultado = reversi_maquinas(posiciones,"MCTS",j,"MCTS",i)
        resultados2MM.append(resultado)

resultadosMM = []
for r1 in resultados1MM:
    for r2 in resultados2MM:
        if (r1[0][0]==r2[1][0] and r1[1][0]==r2[0][0]):
            resultadosMM.append(((r1[0][0],r1[0][1]+r2[1][1]),(r2[0][0],r1[1][1]+r2[0][1])))"""
            
resultados1MM = [((('MCTS', 1), 7), (('MCTS', 3), 3)),
((('MCTS', 1), 4), (('MCTS', 13), 6)),
((('MCTS', 1), 0), (('MCTS', 26), 10)),
((('MCTS', 1), 0), (('MCTS', 170), 10)),
((('MCTS', 3), 0), (('MCTS', 13), 10)), 
((('MCTS', 3), 0), (('MCTS', 26), 10)), 
((('MCTS', 3), 0), (('MCTS', 170), 10)), 
((('MCTS', 13), 2), (('MCTS', 26), 8)), 
((('MCTS', 13), 0), (('MCTS', 170), 10)), 
((('MCTS', 26), 0), (('MCTS', 170), 10))]

resultados2MM = [((('MCTS', 3), 3.5), (('MCTS', 1), 6.5)),
((('MCTS', 13), 10), (('MCTS', 1), 0)),
((('MCTS', 26), 10), (('MCTS', 1), 0)),
((('MCTS', 170), 10), (('MCTS', 1), 0)),
((('MCTS', 13), 10), (('MCTS', 3), 0)),
((('MCTS', 26), 10), (('MCTS', 3), 0)),
((('MCTS', 170), 10), (('MCTS', 3), 0)),
((('MCTS', 26), 10), (('MCTS', 13), 0)),
((('MCTS', 170), 10), (('MCTS', 13), 0)),
((('MCTS', 170), 10), (('MCTS', 26), 0))]

resultadosMM = [((('MCTS', 1), 13.5), (('MCTS', 3), 6.5)),
((('MCTS', 1), 4), (('MCTS', 13), 16)),
((('MCTS', 1), 0), (('MCTS', 26), 20)),
((('MCTS', 1), 0), (('MCTS', 170), 20)),
((('MCTS', 3), 0), (('MCTS', 13), 20)),
((('MCTS', 3), 0), (('MCTS', 26), 20)),
((('MCTS', 3), 0), (('MCTS', 170), 20)),
((('MCTS', 13), 2), (('MCTS', 26), 18)),
((('MCTS', 13), 0), (('MCTS', 170), 20)),
((('MCTS', 26), 0), (('MCTS', 170), 20))] #Resultados de ejecutar el código de arriba     
        
        
resultados1MR = []
for i in [1,3,13,26,170]:
    posiciones = deepcopy(posiciones_iniciales)
    resultado = reversi_maquinas(posiciones,"MCTS",i,"random",0)
    resultados1MR.append(resultado)

resultados2MR = []
for i in [1,3,13,26,170]:
    posiciones = deepcopy(posiciones_iniciales)
    resultado = reversi_maquinas(posiciones,"random",0,"MCTS",i)
    resultados2MR.append(resultado)

resultadosMR = []
for r1 in resultados1MR:
    for r2 in resultados2MR:
        if (r1[0][0]==r2[1][0] and r1[1][0]==r2[0][0]):
            resultadosMR.append(((r1[0][0],r1[0][1]+r2[1][1]),(r2[0][0],r1[1][1]+r2[0][1])))

"""resultados1MR = [((('MCTS', 1), 8), (('random', 0), 2)),
((('MCTS', 3), 4), (('random', 0), 6)),
((('MCTS', 13), 8), (('random', 0), 2)),
((('MCTS', 26), 8), (('random', 0), 2)),
((('MCTS', 170), 10), (('random', 0), 0))]

resultados2MR = [((('random', 0), 5), (('MCTS', 1), 5)),
((('random', 0), 6), (('MCTS', 3), 4)),
((('random', 0), 2), (('MCTS', 13), 8)),
((('random', 0), 1), (('MCTS', 26), 9)),
((('random', 0), 0), (('MCTS', 170), 10))]

resultadosMR = [((('MCTS', 1), 13), (('random', 0), 7)),
((('MCTS', 3), 8), (('random', 0), 12)),
((('MCTS', 13), 16), (('random', 0), 4)),
((('MCTS', 26), 17), (('random', 0), 3)),
((('MCTS', 170), 20), (('random', 0), 0))] #Resultados de ejecutar el código de arriba"""


"""resultados1AR = []
for i in [2,3,4,5,6]:
    posiciones = deepcopy(posiciones_iniciales)
    resultado = reversi_maquinas(posiciones,"poda_ab",i,"random",0)
    resultados1AR.append(resultado)

resultados2AR = []
for i in [2,3,4,5,6]:
    posiciones = deepcopy(posiciones_iniciales)
    resultado = reversi_maquinas(posiciones,"random",0,"poda_ab",i)
    resultados2AR.append(resultado)

resultadosAR = []
for r1 in resultados1AR:
    for r2 in resultados2AR:
        if (r1[0][0]==r2[1][0] and r1[1][0]==r2[0][0]):
            resultadosAR.append(((r1[0][0],r1[0][1]+r2[1][1]),(r2[0][0],r1[1][1]+r2[0][1])))"""
            
resultados1AR = [((('poda_ab', 2), 8), (('random', 0), 2)),
((('poda_ab', 3), 8), (('random', 0), 2)),
((('poda_ab', 4), 9), (('random', 0), 1)),
((('poda_ab', 5), 7), (('random', 0), 3)),
((('poda_ab', 6), 10), (('random', 0), 0))]

resultados2AR = [((('random', 0), 3), (('poda_ab', 2), 7)),
((('random', 0), 2), (('poda_ab', 3), 8)),
((('random', 0), 1), (('poda_ab', 4), 9)),
((('random', 0), 1), (('poda_ab', 5), 9)),
((('random', 0), 0), (('poda_ab', 6), 10))]

resultadosAR = [((('poda_ab', 2), 15), (('random', 0), 5)),
((('poda_ab', 3), 16), (('random', 0), 4)),
((('poda_ab', 4), 18), (('random', 0), 2)),
((('poda_ab', 5), 16), (('random', 0), 4)),
((('poda_ab', 6), 20), (('random', 0), 0))] #Resultados de ejecutar el código de arriba

