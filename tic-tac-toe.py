import random
from copy import deepcopy
from PIL import Image
import numpy as np

class Partida:
    def __init__(self):
        self.tablero = [['b','b','b'],['b','b','b'],['b','b','b']]
        self.turno = 'X'
        
    def es_final(self):
        gana_X = (self.tablero[0][0]=='X' and self.tablero[0][1]=='X' and self.tablero[0][2]=='X') or (self.tablero[1][0]=='X' and self.tablero[1][1]=='X' and self.tablero[1][2]=='X') or (self.tablero[2][0]=='X' and self.tablero[2][1]=='X' and self.tablero[2][2]=='X') or (self.tablero[0][0]=='X' and self.tablero[1][0]=='X' and self.tablero[2][0]=='X') or (self.tablero[0][1]=='X' and self.tablero[1][1]=='X' and self.tablero[2][1]=='X') or (self.tablero[0][2]=='X' and self.tablero[1][2]=='X' and self.tablero[2][2]=='X') or (self.tablero[0][0]=='X' and self.tablero[1][1]=='X' and self.tablero[2][2]=='X') or (self.tablero[0][2]=='X' and self.tablero[1][1]=='X' and self.tablero[2][0]=='X')
        if gana_X:
            return True,'X'
        gana_O = (self.tablero[0][0]=='O' and self.tablero[0][1]=='O' and self.tablero[0][2]=='O') or (self.tablero[1][0]=='O' and self.tablero[1][1]=='O' and self.tablero[1][2]=='O') or (self.tablero[2][0]=='O' and self.tablero[2][1]=='O' and self.tablero[2][2]=='O') or (self.tablero[0][0]=='O' and self.tablero[1][0]=='O' and self.tablero[2][0]=='O') or (self.tablero[0][1]=='O' and self.tablero[1][1]=='O' and self.tablero[2][1]=='O') or (self.tablero[0][2]=='O' and self.tablero[1][2]=='O' and self.tablero[2][2]=='O') or (self.tablero[0][0]=='O' and self.tablero[1][1]=='O' and self.tablero[2][2]=='O') or (self.tablero[0][2]=='O' and self.tablero[1][1]=='O' and self.tablero[2][0]=='O')
        if gana_O:
            return True,'O'
        empate = self.tablero[0][0]!='b' and self.tablero[0][1]!='b' and self.tablero[0][2]!='b' and self.tablero[1][0]!='b' and self.tablero[1][1]!='b' and self.tablero[1][2]!='b' and self.tablero[2][0]!='b' and self.tablero[2][1]!='b' and self.tablero[2][2]!='b'
        if empate:
            return True,''
        else:
            return False,''
    
    def esta_vacia(self,fila,columna):
        return (self.tablero[fila][columna]=='b')
    
    def jugada(self,fila,columna):
        if (0<=fila<=2 and 0<=columna<=2 and self.esta_vacia(fila,columna)):
            self.tablero[fila][columna] = self.turno
            if (self.turno=='X'):
                self.turno = 'O'
            else:
                self.turno = 'X'
    
    def imprimir_tablero(self):
        sol = ""
        for i in range(0,3):
            if (i!=0):
                sol = sol + '\n'
                sol = sol + "---+---+---\n"
            for j in range(0,3):
                if (self.tablero[i][j]=='b' and j==2):
                    sol = sol + "   "
                elif (self.tablero[i][j]=='b'):
                    sol = sol + "   |"
                elif (j==2):
                    sol = sol + " " + self.tablero[i][j] + " "
                else:
                    sol = sol + " " + self.tablero[i][j] + " |"
        print(sol)   

    def imagen_tablero(self):
        tablero_vacio = Image.open("tablero_vacio_tic-tac-toe.png")
        X = Image.open("X.png")
        O = Image.open("O.png")
        for i in range(0,3):
            for j in range(0,3):
                if (self.tablero[i][j]!='b'):
                    coordenada_X = 10+(110*j)
                    coordenada_Y = 10+(110*i)
                    if (self.tablero[i][j]=='X'):
                        tablero_vacio.paste(X,(coordenada_X,coordenada_Y))
                    else:
                        tablero_vacio.paste(O,(coordenada_X,coordenada_Y))
        archivo = input("Introduce el nombre del archivo: ")
        tablero_vacio.save(archivo+".png")                  
            
    def jugar(self,turno,dificultad):
        self.imprimir_tablero()
        if (turno==1):
            jugador = 'X'
            maquina = 'O'
        else:
            jugador = 'O'
            maquina = 'X'
        sin_ocupar = [1,2,3,4,5,6,7,8,9]
        if (dificultad==2):
            aj = Arbol_juego(self)
            aj.llenar_arbol()
            aj.minimax(maquina)
        while (not self.es_final()[0]):
            if (self.turno==jugador):
                casilla = int(input("Introduzca una casilla vacia (1-9): "))
                if (casilla in sin_ocupar):
                    if (dificultad==2):
                        for hijo in aj.hijos:
                            if (hijo[1]==casilla):
                                aj = hijo[0]
                    fila = (casilla-1)//3
                    columna = (casilla-1)%3
                    self.jugada(fila,columna)
                    sin_ocupar.remove(casilla)
                    self.imprimir_tablero()
                else:
                    print("")
                    self.imprimir_tablero()
            else:
                print("\nTurno de la maquina")
                if (dificultad==1):
                    casilla = random.choice(sin_ocupar)
                else:
                    if (aj.evaluacion==-1):
                        casilla = random.choice(sin_ocupar)
                    elif (aj.evaluacion==0):
                        for hijo in aj.hijos:
                            if (hijo[0].evaluacion==0):
                                casilla = hijo[1]
                                aj = hijo[0]
                                break
                    else:
                        for hijo in aj.hijos:
                            if (hijo[0].evaluacion==1):
                                casilla = hijo[1]
                                aj = hijo[0]
                                break
                fila = (casilla-1)//3
                columna = (casilla-1)%3
                self.jugada(fila,columna)
                sin_ocupar.remove(casilla)
                self.imprimir_tablero()      
        final = self.es_final()
        if (final[1]!=''):
            if (final[1]==jugador):
                print("\nHas ganado")
            else:
                print("\nHas perdido")
        else:
            print("\nHas empatado")

class Arbol_juego:
    def __init__(self,partida):
        self.hijos = []
        self.padre = None
        self.partida = partida
        self.visitado = False
        self.evaluacion = None
        self.Q = 0
        self.N = 0

    def anadir_hijo(self,hijo,casilla):
        if (self.hijos==[]):
            self.hijos = [(hijo,casilla)]
        else:
            self.hijos = self.hijos + [(hijo,casilla)]

    def imprimir_hijos(self):
        if (self.hijos!=[]):
            for hijo in (self.hijos):
                print(hijo[1])
                (hijo[0].partida).imprimir_tablero()
                
    def imagen_hijos(self):
        if (self.hijos!=[]):
            for hijo in (self.hijos):
                (hijo[0].partida).imagen_tablero()
            
    def llenar_arbol(self):
        if (not (self.partida).es_final()[0]):
            for casilla in range(1,10):
                fila = (casilla-1)//3
                columna = (casilla-1)%3
                if ((self.partida).esta_vacia(fila,columna)):
                    p = deepcopy(self.partida)
                    p.jugada(fila,columna)
                    aj = Arbol_juego(p)
                    aj.padre = self
                    self.anadir_hijo(aj,casilla)
                    aj.llenar_arbol()
    
    def nodos(self):
        if ((self.partida).es_final()[0]):
            return 1
        else:
            nodos = 1
            for hijo in self.hijos:
                n_h = hijo[0].nodos()
                nodos += n_h
            return nodos
    
    def nodos_con_hijo(self):
        if ((self.partida).es_final()[0]):
            return 0
        else:
            nodos = 1
            for hijo in self.hijos:
                n_h = hijo[0].nodos_con_hijo()
                nodos += n_h
            return nodos
    
    def minimax(self,jugador):
        if (jugador==(self.partida).turno):
            nodo = "max"
        else:
            nodo = "min"
        if (self.hijos==[]):
            final = (self.partida).es_final()
            if (final[1]!=''):
                if (final[1]==jugador):
                    self.evaluacion = 1
                else:
                    self.evaluacion = -1
            else:
                self.evaluacion = 0
        else:
            todos_pierden = True
            alguno_pierde = False
            todos_ganan = True
            alguno_gana = False
            for hijo in (self.hijos):
                hijo[0].minimax(jugador)
                ev_hijo = hijo[0].evaluacion
                if (ev_hijo==0):
                    todos_pierden = False
                    todos_ganan = False
                elif (ev_hijo==1):
                    todos_pierden = False
                    alguno_gana = True
                else:
                    todos_ganan = False
                    alguno_pierde = True
            if (nodo=="max"):
                if alguno_gana:
                    self.evaluacion = 1
                elif todos_pierden:
                    self.evaluacion = -1
                else:
                    self.evaluacion = 0
            else:
                if todos_ganan:
                    self.evaluacion = 1
                elif alguno_pierde:
                    self.evaluacion = -1
                else:
                    self.evaluacion = 0  
        
    def poda_alfa_beta(self,profundidad,alfa,beta,etiqueta):
        if (etiqueta=="max"):
            jugador = (self.partida).turno
        else:
            jugador = 'X'
            if ((self.partida).turno=='X'):
                jugador = 'O'
        if (self.hijos==[]):
            final = (self.partida).es_final()
            if (final[1]!=''):
                if (final[1]==jugador):
                    self.evaluacion = 1
                else:
                    self.evaluacion = -1
            else:
                self.evaluacion = 0
        else:
            if (etiqueta=="max"):
                valor = -np.inf
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
        if (lado==1):
            jugador = (self.partida).turno
        else:
            jugador = 'X'
            if ((self.partida).turno=='X'):
                jugador = 'O'
        if (self.hijos==[]):
            final = (self.partida).es_final()
            if (final[1]!=''):
                if (final[1]==jugador):
                    self.evaluacion = lado*np.inf
                else:
                    self.evaluacion = lado*-np.inf
            else:
                self.evaluacion = 0
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
        if not primera:
            while (nodo.compl_expandido()):
                nodo = nodo.max_uct()
        return (nodo.sin_visitar())
    
    def rollout(self,turno):
        nodo = self
        while (not (nodo.partida).es_final()):
            nodo = nodo.rollout_policy()
        return (nodo.resultado(turno))
    
    def rollout_policy(self):
        nodo = self
        hijo = random.choice(nodo.hijos)
        return hijo[0]
    
    def resultado(self,turno):
        final = (self.partida).es_final()
        if (final[1]!=''):
            if (final[1]==turno):
                resultado = 1
            else:
                resultado = -1
        else:
            resultado = 0
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
                    
def tic_tac_toe():
    turno = int(input("Introduce tu turno (1-2): "))
    dificultad = int(input("Introduce la dificultad (1-2): "))
    if ((turno==1 or turno==2) and (dificultad==1 or dificultad==2)):
        partida = Partida()
        partida.jugar(turno,dificultad)


t = [['O', 'O', 'X'], ['X', 'b', 'O'], ['b', 'b', 'X']]

p = Partida()
p.tablero = deepcopy(t)

aj = Arbol_juego(p)
aj.llenar_arbol()

