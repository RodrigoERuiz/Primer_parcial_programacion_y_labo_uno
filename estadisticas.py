'''

      "estadisticas": {
        "temporadas": 15,
        "puntos_totales": 32292,
        "promedio_puntos_por_partido": 30.1,
        "rebotes_totales": 6672,
        "promedio_rebotes_por_partido": 6.2,
        "asistencias_totales": 5633,
        "promedio_asistencias_por_partido": 5.3,
        "robos_totales": 2514,
        "bloqueos_totales": 893,
        "porcentaje_tiros_de_campo": 49.7,
        "porcentaje_tiros_libres": 83.5,
        "porcentaje_tiros_triples": 32.7
      }

'''


class Estadistica:
    def __init__(self, diccionario) -> None:
        self.__temporadas = diccionario.get('temporadas')
        self.__puntos_totales = diccionario.get('puntos_totales')
        self.__promedio_puntos_por_partido = diccionario.get('promedio_puntos_por_partido')
        self.__rebotes_totales = diccionario.get('rebotes_totales')
        self.__promedio_rebotes_por_partido = diccionario.get('promedio_rebotes_por_partido')
        self.__asistencias_totales = diccionario.get('asistencias_totales')
        self.__promedio_asistencias_por_partido = diccionario.get('promedio_asistencias_por_partido')
        self.__robos_totales = diccionario.get('robos_totales')
        self.__bloqueos_totales = diccionario.get('bloqueos_totales')
        self.__porcentaje_tiros_de_campo = diccionario.get('porcentaje_tiros_de_campo')
        self.__porcentaje_tiros_libres = diccionario.get('porcentaje_tiros_libres')
        self.__porcentaje_tiros_triples  = diccionario.get('porcentaje_tiros_triples')
        
    @property #getter
    def get_temporadas(self):
        return self.__temporadas
    @property
    def get_puntos_totales(self):
        return self.__puntos_totales
    @property
    def get_promedio_puntos_por_partido(self):
        return self.__promedio_puntos_por_partido
    @property
    def get_rebotes_totales(self):
        return self.__rebotes_totales
    @property
    def get_promedio_rebotes_por_partido(self):
        return self.__promedio_rebotes_por_partido
    @property
    def get_asistencias_totales(self):
        return self.__asistencias_totales
    @property
    def get_promedio_asistencias_por_partido(self):
        return self.__promedio_asistencias_por_partido
    @property
    def get_robos_totales(self):
        return self.__robos_totales
    @property
    def get_bloqueos_totales(self):
        return self.__bloqueos_totales
    @property
    def get_porcentaje_tiros_de_campo(self):
        return self.__porcentaje_tiros_de_campo
    @property
    def get_porcentaje_tiros_libres(self):
        return self.__porcentaje_tiros_libres
    @property
    def get_porcentaje_tiros_triples(self):
        return self.__porcentaje_tiros_triples
    
        
