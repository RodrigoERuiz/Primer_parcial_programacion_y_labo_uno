import json
import re
from jugador import Jugador
import copy

class Equipo:
    def __init__(self) -> None:
        self.ruta = 'dream_team.json'
        self.lista_jugadores = self.crear_lista_jugadores()
    
    @property #getter
    def get_lista_jugadores(self):
        return self.__lista_jugadores
    
    def leer_archivo(self):
        try:
            with open(self.ruta, 'r', encoding='UTF-8') as archivo:
                lista_de_jugadores = json.load(archivo)
                return lista_de_jugadores
        except FileNotFoundError:
            print("Error: Archivo no encontrado")
            return None
    
    def crear_lista_jugadores(self):
        lista_jugadores = self.leer_archivo().get('jugadores')
        lista_objetos_jugador = [Jugador(jugador) for jugador in lista_jugadores]
        return lista_objetos_jugador
    
    def mostrar_jugadores(self):
        for jugador in self.lista_jugadores:
           jugador.mostrar_nombre_y_posicion()
           
    def mostrar_estadisticas_jugadores(self):
        for jugador in self.lista_jugadores:
            jugador.mostrar_estadistica_jugador()        
            
    def mostrar_logros_jugadores(self):
        for jugador in self.lista_jugadores:
            jugador.mostrar_logros()
    
    def imprimir_roster_con_indice(self):
        '''
        Recibe una instancia de la clase Equipo.
        Imprime por pantalla el nombre de cada jugador con un índice.
        '''
        for i, jugador in enumerate(self.lista_jugadores, start=1):
            print(f'{i}) {jugador.nombre}')
    
    def buscar_jugador_por_nombre(self)->list[Jugador]:
        '''
        Retorna una lista con los jugadores que hayan tenido coincidencias en el nombre
        '''
        lista_coincidencias = []
        while len(lista_coincidencias) == 0:
            nombre_buscado = input("Ingrese el nombre del jugador: ").title()
            for jugador in self.lista_jugadores:
                if re.search(nombre_buscado,jugador.nombre):
                    lista_coincidencias.append(jugador)
        return lista_coincidencias
    
    # def buscar_jugador_con_maximo_o_minimo_apartado_estadistico(self, apartado_estadistico: str, busco_mayor:bool) -> Jugador:
    #     '''
    #     Recibe:
    #             un apartado estadistico
    #             un booleano (Si es True busca por mayor sino busca por menor)
        
    #     Propósito: Retornar al jugador con el mayor o menor apartado estadístico pasado por parametro
    #     '''
    #     if not self.lista_jugadores:
    #         return None
    #     jugador_retorno = self.lista_jugadores[0]
    #     for jugador in self.lista_jugadores[1:]:
    #         if busco_mayor:
    #             if getattr(jugador_retorno.estadistica, apartado_estadistico) is None or\
    #                 getattr(jugador_retorno.estadistica, apartado_estadistico) < getattr(jugador.estadistica, apartado_estadistico):#se utiliza para acceder a un apartado_estadistico cuando éste esta parametrizado
    #                 jugador_retorno = jugador
    #         else:
    #             if getattr(jugador_retorno.estadistica, apartado_estadistico) is None or\
    #                 getattr(jugador_retorno.estadistica, apartado_estadistico) > getattr(jugador.estadistica, apartado_estadistico):
    #                  jugador_retorno = jugador
    #     return jugador_retorno
    
    
    def buscar_jugador_con_maximo_o_minimo_apartado_estadistico(self, apartado_estadistico: str, busco_mayor:bool) -> list[Jugador]:
        '''
        Recibe:
                un apartado estadistico
                un booleano (Si es True busca por mayor sino busca por menor)
        
        Propósito: Retornar al jugador con el mayor o menor apartado estadístico pasado por parametro
            '''
        if not self.lista_jugadores:
            return []

        valor_extremo = None
        jugadores_retorno = []

        for jugador in self.lista_jugadores:
            valor_actual = getattr(jugador.estadistica, apartado_estadistico)
            
            if valor_actual is not None:
                if valor_extremo is None:
                    valor_extremo = valor_actual
                    jugadores_retorno.append(jugador)
                elif (busco_mayor and valor_actual > valor_extremo) or (not busco_mayor and valor_actual < valor_extremo):
                    # Se encontró un nuevo valor máximo o mínimo, reiniciar la lista de jugadores.
                    valor_extremo = valor_actual
                    jugadores_retorno = [jugador]
                elif valor_actual == valor_extremo:
                    # El valor actual es igual al valor máximo o mínimo actual, agregar el jugador a la lista.
                    jugadores_retorno.append(jugador)

        return jugadores_retorno
    
    def buscar_hall_oh_fame_por_nombre(self)->str:
        '''
        Recibe una lista de jugadores
        le pide un nombre al usuario
        retorna un string indicando si es el jugador es miembro o no del salon de la fama
        '''
        jugadores_consultados = self.buscar_jugador_por_nombre()
        for jugador in jugadores_consultados:
            if jugador.is_hall_of_fame():
                print(f'{jugador.nombre} Es Hall of Fame')
            else:
                print(f'{jugador.nombre} No es Hall of Fame')

    def pedir_ingreso_de_dato_y_validar(self):  
        '''
        Le solicita al usuario que ingrese y un numero
        valida que este se encuentre entre el 1 y el 12
        una vez que lo obtiene lo castea a int y lo retorna
        '''
        while True:
            dato_ingresado = input("Seleccione el nro del jugador en la lista para ver sus estadisticas: ")
            if re.match(r"^(1[0-1]|[0-9])$",dato_ingresado):
                dato_ingresado = int(dato_ingresado)
                break
        return dato_ingresado

    
    def filtar_jugador_por_indice_estadisticas(self)->Jugador:
        '''
        Recibe una lista de jugadores
        le solicita al usuario que elija un jugador
        retorna una copia del jugador que ocupa el indice indicado por el usuar
        '''
        indice_buscado = self.pedir_ingreso_de_dato_y_validar()
        jugador_retorno = self.lista_jugadores[indice_buscado-1]
        print(jugador_retorno.nombre)
        return jugador_retorno 
    
    def mostrar_estadistica_de_jugador_elegido_por_indice(self):
        self.imprimir_roster_con_indice()
        jugador_selccionado = self.filtar_jugador_por_indice_estadisticas()
        return jugador_selccionado
    
    def generar_lista_posiciones(self)->list[str]:
        '''
           Genera una lista de las posiciones válidas presentes en la lista de jugadores del equipo sin posiciones repetidas.

            Retorna:
                list[str]: Una lista de cadenas que representan las posiciones válidas de los jugadores en el equipo.
        '''
        lista_posiciones_validas = [jugador.posicion for jugador in self.lista_jugadores]
        lista_posiciones_validas = list(set(lista_posiciones_validas))
        return lista_posiciones_validas
