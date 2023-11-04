from estadisticas import Estadistica
import copy

class Jugador:
    def __init__(self,jugador:dict) -> None:
        self.lista_logros = jugador.get('logros')
        self.nombre = jugador.get('nombre')
        self.posicion =jugador.get('posicion')
        self.estadistica = Estadistica(jugador['estadisticas'])
        
    def mostrar_nombre_y_posicion(self):
        print(f'Nombre: {self.nombre} posicion: {self.posicion}')

    def mostrar_logros(self):
        print(self.nombre)
        for logro in self.lista_logros:
            print(logro)
    
    def mostrar_nombre_y_apartado_estadisticos_jugador(self, apartado_uno: str, apartado_dos: str) -> str:
        return f'{self.nombre} {apartado_uno}: {getattr(self.estadistica, apartado_uno)} {apartado_dos}: {getattr(self.estadistica, apartado_dos)}'
    
                
    def mostrar_estadistica_jugador(self):
        return f'''
            Nombre: {self.nombre}
            Asistencias totales: {self.estadistica.get_asistencias_totales}
            Bloqueos totales: {self.estadistica.get_bloqueos_totales}
            Porcentaje de tiros de campo: {self.estadistica.get_porcentaje_tiros_de_campo}
            Porcentaje de tiros libres: {self.estadistica.get_porcentaje_tiros_libres}
            Porcentaje de triples: {self.estadistica.get_porcentaje_tiros_triples}
            Porcentaje de Asistencias por partido: {self.estadistica.get_promedio_asistencias_por_partido}
            Promedio de puntos por partido: {self.estadistica.get_promedio_puntos_por_partido}
            Promedio de rebotes por partido: {self.estadistica.get_promedio_rebotes_por_partido}
            Puntos totales: {self.estadistica.get_puntos_totales}
            Rebotes totales: {self.estadistica.get_rebotes_totales}
            Robos Totales: {self.estadistica.get_robos_totales}
            Temporadas: {self.estadistica.get_temporadas}
            '''

    def is_hall_of_fame(self)->bool:
        '''
        recibe un jugador y retorna True si ser hall of fame está entre sos logros
        Retorno False en caso contrario
        '''
        mensaje = "Miembro del Salon de la Fama del Baloncesto"
        return mensaje in self.lista_logros
        
