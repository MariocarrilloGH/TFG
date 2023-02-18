import random
import numpy as np
from copy import deepcopy

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
        for i in range(0,8):
            if (i!=0):
                sol = sol + '\n'
                sol = sol + "---+---+---+---+---+---+---+---\n"
            for j in range(0,8):
                if (self.tablero[i][j]=='b' and j==7):
                    sol = sol + "   " + str(i+1)
                elif (self.tablero[i][j]=='b'):
                    sol = sol + "   |"
                elif (j==7):
                    sol = sol + " " + self.tablero[i][j] + " "
                else:
                    sol = sol + " " + self.tablero[i][j] + " |"
        sol = sol + "\n a   b   c   d   e   f   g   h "
        print(sol)   

class Arbol_juego:
    def __init__(self,partida):
        self.hijos = []
        self.partida = partida

    def anadir_hijo(self,hijo,jugada):
        (self.hijos).append((hijo,jugada))

    def imprimir_hijos(self):
        if (len(self.hijos)!=0):
            for hijo in (self.hijos):
                print(hijo[1])
                (hijo[0].partida).imprimir_tablero()

    def llenar_nivel(self):
        jugadas_legales = (self.partida).jugadas_legales()
        for jugada in jugadas_legales:
            fila = jugada[0]
            columna = jugada[1]
            p = deepcopy(self.partida)
            p.jugada(fila,columna)
            aj = Arbol_juego(p)
            self.anadir_hijo(aj,jugada)
    
    def ordenar_hijos(self):
        hijos_ordenados = []
        jugador = self.turno
        if (len(self.hijos)!=0):
            hijos_ordenados.append(self.hijos[0])
            for hijo in (self.hijos[1::]):
                for hijo_ord in hijos_ordenados:
                    if ((hijo[0].partida).heuristica(jugador)>(hijo_ord[0].partida).heuristica(jugador)):
                        
    
    def minimax(self,profundidad,etiqueta):
        if (etiqueta=="max"):
            jugador = (self.partida).turno
        else:
            jugador = 'N'
            if ((self.partida).turno=='N'):
                jugador = 'B'
        if (profundidad==0 or (self.partida).es_final()):
            return (self.partida).heuristica(jugador)
        else:
            if (etiqueta=="max"):
                valor = -np.inf
                self.llenar_nivel()
                for hijo in self.hijos:
                    m = (hijo[0]).minimax(profundidad-1,"min")
                    valor = max(valor,m)
                return valor
            else:
                valor = np.inf
                self.llenar_nivel()
                for hijo in self.hijos:
                    m = (hijo[0]).minimax(profundidad-1,"max")
                    valor = min(valor,m)
                return valor
        
    def poda_alfa_beta(self,profundidad,alfa,beta,etiqueta):
        if (etiqueta=="max"):
            jugador = (self.partida).turno
        else:
            jugador = 'N'
            if ((self.partida).turno=='N'):
                jugador = 'B'
        if (profundidad==0 or (self.partida).es_final()):
            return (self.partida).heuristica(jugador)
        else:
            if (etiqueta=="max"):
                valor = -np.inf
                self.llenar_nivel()
                for hijo in self.hijos:
                    m = (hijo[0]).poda_alfa_beta(profundidad-1,alfa,beta,"min")
                    valor = max(valor,m)
                    if (valor>beta):
                        break
                    alfa = max(alfa,valor)
                return valor
            else:
                valor = np.inf
                self.llenar_nivel()
                for hijo in self.hijos:
                    m = (hijo[0]).poda_alfa_beta(profundidad-1,alfa,beta,"max")
                    valor = min(valor,m)
                    if (valor<alfa):
                        break
                    beta = min(beta,valor)
                return valor
    
    def principal_variation_search(self,profundidad,alfa,beta,lado):
        self.ordenar_hijos()
        