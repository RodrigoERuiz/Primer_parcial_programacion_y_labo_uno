from equipo import Equipo
from jugador import Jugador 
from estadisticas import Estadistica
import re
import os
import json
import sqlite3

mi_equipo = Equipo() 

def exportar_csv(path: str, modo: str, contenido: str):
    """
    Exporta contenido a un archivo CSV.

    Esta función toma un contenido en forma de cadena de texto y lo exporta a un archivo CSV especificado por la ruta
    proporcionada. Los encabezados y valores se extraen de las líneas del contenido. El modo de apertura del archivo
    (escritura, anexado, etc.) se especifica mediante el parámetro 'modo'.

    Parámetros:
        path (str): Ruta del archivo CSV donde se exportará el contenido.
        modo (str): Modo de apertura del archivo ('w' para escritura, 'a' para anexado, etc.).
        contenido (str): Contenido en forma de cadena de texto que se exportará.
    """
    try:
        # Separa el contenido en líneas
        lineas = contenido.strip().split('\n')

        # Crea dos listas, una para los encabezados y otra para los valores
        encabezados = []
        valores = []

        for linea in lineas:
            # Divide cada línea en dos partes utilizando ':' como separador
            partes = linea.split(': ')
            encabezado = partes[0].strip() 
            encabezados.append(encabezado)
            valores.append(partes[1])

        with open(path, modo, encoding='utf-8') as archivo:
            # Escribe los encabezados en una fila
            archivo.write(','.join(encabezados) + '\n')

            # Escribe los valores en la siguiente fila
            archivo.write(','.join(valores) + '\n')
    except FileNotFoundError:
        print(f"Error: Archivo no encontrado - {path}")
    except PermissionError:
        print(f"Error: Permiso denegado para acceder al archivo - {path}")

def exportar_json(path: str, modo: str, contenido: dict):
    '''
        Exporta un diccionario a un archivo JSON.

    Esta función toma un diccionario 'contenido' y lo exporta a un archivo JSON especificado por la ruta 'path'.
    El modo de apertura del archivo (escritura, anexado, etc.) se especifica mediante el parámetro 'modo'.

    Parámetros:
        path (str): Ruta del archivo JSON donde se exportará el contenido.
        modo (str): Modo de apertura del archivo ('w' para escritura, 'a' para anexado, etc.).
        contenido (dict): Diccionario que se exportará como JSON.
    '''
    try:
        with open(path, modo, encoding='utf-8') as archivo:
            json.dump(contenido, archivo, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        print(f"Error: Archivo no encontrado - {path}")
    except PermissionError:
        print(f"Error: Permiso denegado para acceder al archivo - {path}")

def crear_db(path:str, nombre_tabla:str):
    '''
        Crea una base de datos SQLite y una tabla en ella.

    Esta función crea una base de datos SQLite en el archivo especificado por 'path' y luego crea una tabla
    con el nombre especificado por 'nombre_tabla'. La tabla contendrá tres columnas: 'id' (clave primaria autoincremental),
    'nombre' (texto) y 'temporadas' (entero).

    Parámetros:
        path (str): Ruta donde se creará la base de datos SQLite con la extensión '.db'.
        nombre_tabla (str): Nombre de la tabla que se creará en la base de datos.

    '''
    with sqlite3.connect(f"{path}.db") as conexion:
        try:
            sentencia = f''' create  table {nombre_tabla}
                            (
                                    id integer primary key autoincrement,
                                    nombre text,
                                    temporadas integer
                            )
                        '''
            conexion.execute(sentencia)
            print("Se creo la tabla personajes")                       
        except sqlite3.OperationalError:
            print("La tabla personajes ya existe") 
            
def insertar_filas_db(path:str, nombre_tabla:str,diccionario:dict):
    '''
        Inserta filas en una tabla de una base de datos SQLite.

    Esta función toma un diccionario donde las claves son los nombres y los valores son las temporadas, e inserta
    filas en la tabla de la base de datos especificada por 'path' y 'nombre_tabla'.

    Parámetros:
        path (str): Ruta de la base de datos SQLite con la extensión '.db'.
        nombre_tabla (str): Nombre de la tabla en la que se insertarán las filas.
        diccionario (dict): Diccionario donde las claves son nombres (str) y los valores son temporadas (int).
    ''' 
    with sqlite3.connect(f"{path}.db") as conexion:
        try:
            for nombre,temporadas in diccionario.items():
                conexion.execute(f"insert into {nombre_tabla}(nombre,temporadas) values (?,?)", (nombre,temporadas))

            conexion.commit()
        except:
            print("Error")
                       
def crear_db_posiciones(path:str, nombre_tabla:str):
    with sqlite3.connect(f"{path}.db") as conexion:
        try:
            sentencia = f''' create  table {nombre_tabla}
                            (
                                    Posiciones text
                            )
                        '''
            conexion.execute(sentencia)
            print("Se creo la tabla personajes")                       
        except sqlite3.OperationalError:
            print("La tabla personajes ya existe") 

def insertar_posisciones_db(path: str, nombre_tabla: str, lista_posisciones_unicas: list):
    with sqlite3.connect(f"{path}.db") as conexion:
        try:
            for posicion in lista_posisciones_unicas:
                conexion.execute(f'insert into {nombre_tabla}(Posiciones) values (?)', (posicion,))
            conexion.commit()
        except:
            print('Error')

def convertir_string_a_diccionario(texto:str)->dict:
    """
    Convierte una cadena de texto en un diccionario.

    Esta función toma una cadena de texto en un formato específico y la convierte en un diccionario donde las claves son
    los nombres de los jugadores y los valores son la cantidad de temporadas. El formato esperado de la cadena de texto es
    una serie de líneas donde cada línea contiene un nombre de jugador seguido de ": " y el número de temporadas.

    Args:
        texto (str): La cadena de texto que se va a convertir en un diccionario.

    Returns:
        dict: Un diccionario donde las claves son los nombres de los jugadores y los valores son la cantidad de temporadas.

    Examples:
        Ejemplo de uso:

        >>> datos_jugadores = "Nombre Jugador 1: 5\nNombre Jugador 2: 7\nNombre Jugador 3: 10"
        >>> diccionario = convertir_string_a_diccionario(datos_jugadores)
        >>> print(diccionario)
    """
    data_dict = {}
    for linea in texto.split('\n'):
        partes = linea.split(': ')
        if len(partes) == 2:
            nombre_jugador = partes[0].strip()
            temporadas = int(partes[1].split()[0])
            data_dict[nombre_jugador] = temporadas
    return data_dict
        
def limpiar_consola() -> None:
    """
    Imprime un mensaje indicando que limpiará la consola al presionar la tecla enter.
        Para que funcione hay que importar el modulo os de la siguiente manera:
        import os
    Recibe: Nada
    Devuelve: Nada
    """
    if os.name in ['ce', 'nt', 'dos']:
        os.system('cls')
    else:
        os.system('clear')
        
def verificar_continuidad_de_ejecucion(mensaje:str)->bool:
        respuesta = input(mensaje).lower()
        while respuesta != "si" and respuesta != "no":
            respuesta = input('Respuesta inválida ¿Desea realizar otra operación? (si/no) ').lower()
        if respuesta.lower() == 'si':
            return True
        return False

def quick_sort_lista_jugadores_recursivo(lista_jugadores:list[Jugador], menor_a_mayor:bool, campo:str):
    if len(lista_jugadores) <= 1:
        return lista_jugadores

    pivot = lista_jugadores[0]
    lista_iz = []
    lista_de = []

    for jugador in lista_jugadores[1:]:
        if menor_a_mayor:
            if getattr(jugador.estadistica, campo) < getattr(pivot.estadistica, campo):
                lista_iz.append(jugador)
            else:
                lista_de.append(jugador)
        else:
            if getattr(jugador.estadistica, campo) > getattr(pivot.estadistica, campo):
                lista_iz.append(jugador)
            else:
                lista_de.append(jugador)

    lista_iz = quick_sort_lista_jugadores_recursivo(lista_iz, menor_a_mayor,campo)
    lista_iz.append(pivot)
    lista_de = quick_sort_lista_jugadores_recursivo(lista_de, menor_a_mayor,campo)
    lista_iz.extend(lista_de)

    return lista_iz

def quick_sort_lista_jugadores_recursivo_dos_parametros(lista_jugadores:list[Jugador], menor_a_mayor:bool, campo_uno:str, campo_dos:str):
    if len(lista_jugadores) <= 1:
        return lista_jugadores

    pivot = lista_jugadores[0]
    lista_iz = []
    lista_de = []

    for jugador in lista_jugadores[1:]:
        if menor_a_mayor:
            if getattr(jugador.estadistica, campo_uno) + getattr(jugador.estadistica, campo_dos) <\
                getattr(pivot.estadistica, campo_uno) + getattr(pivot.estadistica, campo_dos):
                lista_iz.append(jugador)
            else:
                lista_de.append(jugador)
        else:
            if getattr(jugador.estadistica, campo_uno) + getattr(jugador.estadistica, campo_dos) >\
                getattr(pivot.estadistica, campo_uno) + getattr(pivot.estadistica, campo_dos):
                lista_iz.append(jugador)
            else:
                lista_de.append(jugador)

    lista_iz = quick_sort_lista_jugadores_recursivo_dos_parametros(lista_iz, menor_a_mayor,campo_uno,campo_dos)
    lista_iz.append(pivot)
    lista_de = quick_sort_lista_jugadores_recursivo_dos_parametros(lista_de, menor_a_mayor,campo_uno,campo_dos)
    lista_iz.extend(lista_de)

    return lista_iz

def obtener_jugadores_ordenados_por(lista_de_jugadores:list[Jugador], mayor_a_menor:str,campo:str)->str:
        string_retorno = ''
        jugadores_ordenados_por_temporada = quick_sort_lista_jugadores_recursivo(lista_de_jugadores,False,'get_temporadas')
        for jugador in jugadores_ordenados_por_temporada:
            string_retorno += f'{jugador.nombre}: {jugador.estadistica.get_temporadas} temporadas \n'
        return string_retorno

def mostrar_nombre_y_apartado_estadisticos_jugador(jugador:Jugador,apartado_uno:str,apartado_dos:str)->str:
    return f'{jugador.nombre} {apartado_uno}: {getattr(jugador.estadistica, apartado_uno)} {apartado_dos}: {getattr(jugador.estadistica, apartado_dos)}' 


def mostrar_nombre_y_apartado_estadisticos_equipo(lista_jugadores:list[Jugador],apartado_uno:str, apartado_dos:str):

    string_retorno = ''
    for jugador in lista_jugadores:
        string_retorno +=  f'{jugador.mostrar_nombre_y_apartado_estadisticos_jugador(apartado_uno,apartado_dos)}\n'
    return string_retorno

def obtener_porcentaje(valor_actual:int, valor_maximo:int):
    return (valor_actual * 100) / valor_maximo

def listar_jugadores_ordenados_con_porcentaje(lista_jugadores_ordenados, apartado_uno, apartado_dos, hay_que_listar_todos = None):
    '''
        Lista los jugadores ordenados por un par de apartados estadísticos con su porcentaje en relación al máximo.

    Esta función toma una lista de jugadores previamente ordenada según dos apartados estadísticos, y permite al usuario
    especificar cuántos de estos jugadores desea listar junto con su porcentaje en relación al máximo en esos dos
    apartados. Si las función es invocado con el parámetro hay_que_listar_todos en False, por defecto se listan todos
    los jugadores del equipo

    Parámetros:
        lista_jugadores_ordenados (list[Jugador]): La lista de jugadores previamente ordenada.
        apartado_uno (str): El nombre del primer apartado estadístico por el que se ordenarán los jugadores.
        apartado_dos (str): El nombre del segundo apartado estadístico por el que se ordenarán los jugadores.

    Retorna:
        str: Una cadena que contiene la lista de jugadores ordenados junto con su porcentaje en relación al máximo
        en los dos apartados estadísticos.
  
        Ejemplo de uso:

        >>> jugadores_ordenados = quick_sort_lista_jugadores_recursivo(equipo.lista_jugadores, True, 'get_puntos_totales', 'get_rebotes_totales')
        >>> resultado = listar_jugadores_ordenados_con_porcentaje(jugadores_ordenados, 'get_puntos_totales', 'get_rebotes_totales')
        >>> print(resultado)
    '''
    cantidad_jugadores = len(lista_jugadores_ordenados)
    
    if hay_que_listar_todos:
        cantidad_a_listar = cantidad_jugadores  # Si no se especifica una cantidad, listar todos los jugadores.
    else:
        while True:
            cantidad_a_listar = input(f'Cuantos jugadores desea listar (1-{cantidad_jugadores})? ')
            if not re.match(r'^\d+$', cantidad_a_listar):
                print("La cantidad debe ser un número entero.")
            else:
                cantidad_a_listar = int(cantidad_a_listar)
                if cantidad_a_listar < 1 or cantidad_a_listar > cantidad_jugadores:
                    print(f"La cantidad debe estar entre 1 y {cantidad_jugadores}.")
                else:
                    break

    string_retorno = ''
    maximo_en_apartado_uno = getattr(lista_jugadores_ordenados[0].estadistica, apartado_uno)
    maximo_en_apartado_dos = getattr(lista_jugadores_ordenados[0].estadistica, apartado_dos)
    valores_maximos_sumados = maximo_en_apartado_uno + maximo_en_apartado_dos

    for i, jugador in enumerate(lista_jugadores_ordenados[:cantidad_a_listar], start=1):
        apartados_sumados_jugador_actual = getattr(jugador.estadistica, apartado_uno) + getattr(jugador.estadistica, apartado_dos)
        string_retorno += f'{i}. {mostrar_nombre_y_apartado_estadisticos_jugador(jugador, apartado_uno, apartado_dos)} {round(obtener_porcentaje(apartados_sumados_jugador_actual, valores_maximos_sumados), 2)}%\n'
    
    return string_retorno
    
def imprimir_resultados(jugadores, dato_para_imprimir, apartado_estadistico=None):
    '''
    Imprime los resultados de una búsqueda de jugadores en función de un dato específico.

    Recibe:
        jugadores (list): Una lista de objetos Jugador.
        dato_a_buscar (str): El dato que se busca (por ejemplo, "rebotes totales").
        apartado_estadistico (str): El apartado estadístico específico que se debe imprimir si es necesario (por defecto, None).

    Retorna:
        None
    '''
    if apartado_estadistico:
        for jugador in jugadores:
            print(f'El jugador con más {dato_para_imprimir} es: {jugador.nombre} con {getattr(jugador.estadistica, apartado_estadistico)}')
    else:
        for jugador in jugadores:
            print(f'{jugador.nombre}: puntos: {jugador.estadistica.get_promedio_puntos_por_partido}')

menu_inicial =\
    '''
          1) Mostrar la lista de todos los jugadores del Dream Team
          2) Seleccionar un jugador por indice y mostrar sus estadísticas (OPCION EXPORTAR A CSV)
          3) Exportar estadistica a CSV
          4) Buscar jugador por nombre y mostrar sus logros
          5) Calcular y mostrar el promedio de puntos por partido de todo el equipo del Dream Team, ordenado por nombre de manera ascendente
          6) Ingresar jugador y verificar si es HoF
          7) Calcular y mostar el jugador con mayor cantidad de rebotes totales 
          8) Generar listado ordenado por temporadas y exportar archivo CSV/JSON/DB
          9) Ordenar los jugadores por el valor sumado de robos y bloqueos totales
         10) Crear base de datos de jugadores ordenados por temporadas jugadas
         11) Salir
         
        Seleccione una opcion de la lista: '''
menu_punto_8 =\
    '''
    A) guardar este listado ordenado en un archivo CSV con su apellido.csv
    B) Permitir guardar este listado ordenado en un archivo JSON y permitir al usuario ingresar el nombre del archivo a guardar (validar con regex)
    C) Guardar en Base de datos
    D) Salir del sub menu actual
    
    Seleccione una opcion de la lista: '''
menu_punto_9 =\
    '''
    A) Ordenar los jugadores por le valor sumado de rebotes totales y bloqueos totales
    B) listar todos los jugadores ordenados y mostrar el porcentaje de este valor sumado tomando como 100% el valor máximo
    C) crear un filtro que permita ingresar un valor y que solo muestre esa cantidad de jugadores ordenados por la suma de los dos campos
    D) Salir del sub menu actual
    
    Seleccione una opcion de la lista: '''

def mostrar_menu(patron_regex:str, menu:str): # Se utliza en bucle principal y sub menu del punto 8 y 9
    '''
    Muestra un menú y solicita una opción al usuario.

    Esta función muestra un menú en forma de cadena de texto y solicita al usuario que ingrese una opción. 
    Luego, verifica si la opción ingresada por el usuario coincide con un patrón de expresión regular especificado.
    Si la opción es válida, la función la devuelve en mayúsculas; de lo contrario, devuelve -1.

    Parámetros:
        patron_regex (str): Un patrón de expresión regular utilizado para validar la opción ingresada por el usuario.
        menu (str): El menú que se mostrará al usuario en forma de cadena de texto.

    Retorna:
        str: La opción ingresada por el usuario en mayúsculas si es válida
    '''  
    opcion = input(f'{menu}')
    patron = rf'{patron_regex}'
    if re.match(patron,opcion) != None:
        return opcion.upper()
    
def dream_team_app(equipo:Equipo):
    ejecutar = True
    case_2_ejecutado = None
    while ejecutar:
        opcion = mostrar_menu('^[1-9]|10|11$',menu_inicial)
        match(opcion):
            case "1":
                equipo.mostrar_jugadores()
            case "2":
                case_2_ejecutado = True
                jugador_elegido = mi_equipo.mostrar_estadistica_de_jugador_elegido_por_indice()
                print(jugador_elegido.mostrar_estadistica_jugador())
            case '3':
                if case_2_ejecutado:
                    exportar_csv('archivo_prueba.csv','w',jugador_elegido.mostrar_estadistica_jugador())
                else:
                    print('\nprimero debe seleccionar un jugador...\n')
                    jugador_elegido = mi_equipo.mostrar_estadistica_de_jugador_elegido_por_indice()
                    print(jugador_elegido.mostrar_estadistica_jugador())
                    exportar_csv('archivo_prueba.csv','w',jugador_elegido.mostrar_estadistica_jugador())
                case_2_ejecutado = None 
            case '5':
                jugadores_ordenados_por_promedio_de_puntos = quick_sort_lista_jugadores_recursivo(equipo.lista_jugadores,False,'get_promedio_puntos_por_partido')
                imprimir_resultados(jugadores_ordenados_por_promedio_de_puntos,'get_promedio_puntos_por_partido')
            case '6': 
                equipo.buscar_hall_oh_fame_por_nombre()
            case "7":
                dato_a_buscar = "rebotes totales"
                jugador_buscado = equipo.buscar_jugador_con_maximo_o_minimo_apartado_estadistico('get_rebotes_totales',True)
                imprimir_resultados(jugador_buscado,dato_a_buscar, 'get_rebotes_totales')
            case "4":
                jugador_buscado = equipo.buscar_jugador_por_nombre()
                for jugador in jugador_buscado:
                    jugador.mostrar_logros()

            case '8':
                ejecutar = True
                salir_sub_menu = None
                while ejecutar: 
                    print(obtener_jugadores_ordenados_por(equipo.lista_jugadores,False,'get_temporadas'))  
                    opcion = mostrar_menu('^[Aa|Bb|Cc|Dd]{1}$', menu_punto_8)             
                    match(opcion):
                    
                        case 'A':
                            nombre_del_archivo = input('Ingrese el nombre con el que desea guardar el archivo: ').lower()
                            exportar_csv(f'{nombre_del_archivo}.csv','w',obtener_jugadores_ordenados_por(equipo.lista_jugadores,False,'get_temporadas'))
                        
                        case 'B':
                            nombre_del_archivo = input('Ingrese el nombre con el que desea guardar el archivo: ').lower()
                            string_convertido_a_json = convertir_string_a_diccionario(obtener_jugadores_ordenados_por(equipo.lista_jugadores,False,'get_temporadas'))
                            exportar_json(f'{nombre_del_archivo}.json','w',string_convertido_a_json) 
                            
                        case 'C':
                            crear_db('db_jugadores_ordenados_por_temporadas','jugadores_ordenadados_temporadas')
                            insertar_filas_db('db_jugadores_ordenados_por_temporadas','jugadores_ordenadados_temporadas',convertir_string_a_diccionario(obtener_jugadores_ordenados_por(equipo.lista_jugadores,False,'get_temporadas')))
                            
                        case 'D':
                            salir_sub_menu = True
                        case _:
                            continue

                    if salir_sub_menu or not verificar_continuidad_de_ejecucion('Desea continuar dentro de este sub-menu? si/no: '):
                        ejecutar = False 
                    limpiar_consola()  

            case '9':
                ejecutar = True
                salir_sub_menu = None
                while ejecutar:
                    opcion = mostrar_menu('^[Aa|Bb|Cc|Dd]{1}$', menu_punto_9)
                    match(opcion):
                        case 'A':
                            jugadores_ordenados_por_apartados_estadisticos_sumados = quick_sort_lista_jugadores_recursivo_dos_parametros(equipo.lista_jugadores,False,'get_robos_totales','get_bloqueos_totales')
                            print(mostrar_nombre_y_apartado_estadisticos_equipo(jugadores_ordenados_por_apartados_estadisticos_sumados,'get_robos_totales','get_bloqueos_totales'))
                            
                        case 'B':
                            jugadores_ordenados_por_apartados_estadisticos_sumados = quick_sort_lista_jugadores_recursivo_dos_parametros(equipo.lista_jugadores,False,'get_robos_totales','get_bloqueos_totales')
                            print(listar_jugadores_ordenados_con_porcentaje(jugadores_ordenados_por_apartados_estadisticos_sumados,'get_robos_totales','get_bloqueos_totales',True))
                            
                        case 'C':
                            jugadores_ordenados_por_apartados_estadisticos_sumados = quick_sort_lista_jugadores_recursivo_dos_parametros(equipo.lista_jugadores,False,'get_robos_totales','get_bloqueos_totales')
                            print(listar_jugadores_ordenados_con_porcentaje(jugadores_ordenados_por_apartados_estadisticos_sumados,'get_robos_totales','get_bloqueos_totales',False))
                            
                        case 'D':
                            salir_sub_menu = True
                            
                        case _:
                            continue
                      
                    if salir_sub_menu or not verificar_continuidad_de_ejecucion('Desea continuar dentro de este sub-menu? si/no: '):
                        ejecutar = False    
                    limpiar_consola()
            case '10':
                lista_posiciones = equipo.generar_lista_posiciones()
                crear_db_posiciones('db_posiciones','tabla_posiciones')
                insertar_posisciones_db('db_posiciones','tabla_posiciones',lista_posiciones)
                
            case '11':
                break
            
            case _:
                print ('Opcion invalida')  
           
        ejecutar = verificar_continuidad_de_ejecucion('\n¿Desea realizar otra operación? (si/no) ')
        limpiar_consola() 
        
dream_team_app(mi_equipo)

