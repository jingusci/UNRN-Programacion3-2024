'''
Programación 3 - 2024 - Trabajo Integrador Final
Subproblema 2 - Grupo F
Alumnos:
 - Javier Ingusci
 - Enrique Mariotti
 - Joaquín Rodríguez

 Archivo calculo_vuelto.py

 Objetivo: Identificar que billetes entregar como vuelto
 Metodología: 
    -   Funcion principal que recibe como input que cantidad de vuelto entregar
    -   Consulta a un archivo prolog que calcula las combinaciones de billetes 
        que son posibles para entregar
    -   Procesamiento de la salida del mensaje de prolog y conversión en diccionario
    -   Seleccion de vuelto valido segun billetes disponibles en la caja registradora

Input: Valor de vuelto (int)  
Salida: Diccionario con billetes a entregar

Funcion extra:
    string para mostrar en consola con los billetes a entregar 
 
 '''


# Importar las librerias
from pyswip import Prolog

from consultas_bd import consultar_caja_registradora

def calculo_vuelto_prolog(vuelto):
    '''
    Esta funcion recibe un monto a entregar de vuelto (Redondea el vuelto al 
    multiplo de 5 mas cercano.), calcula las con todas las posibles combinaciones 
    de billetes a dar de vuelto, consulta la BD "Caja registradora" para 
    obtener la informacion de billetes disponibles y devuelve la combinacion 
    de billetes a dar como vuelto.
    '''

    retorno = None

    # Lanzar excepción ante la llegada de un numero negativo
    if vuelto <= 0:
        raise ValueError(f"No es posible entregar ${vuelto} como vuelto")

    # Redondear el vuelto al multiplo de 5 mas cercano
    vuelto_multiplo_de_5 = round(vuelto / 5) * 5

    ### Abrir el archivo prolog
    prolog = Prolog()
    prolog.consult("billetes_v2.pl") # TODO: Eliminar la v1 si nos quedamos con esta version.

    # Ejecutar la consulta prolog y convertir el resultado en una lista
    # Esta lista contiene todas las posibilidades de vuelto que se pueden dar
    resultado = list(prolog.query(f"calcular_vuelto({vuelto_multiplo_de_5}, Resultado)"))

    # Si el resultado existe, procesas la lista obtenida. Si no, lanzar una excepción
    if resultado:
        # Remover duplicados de la lista
        lista_sin_duplicados = __remover_duplicados__(resultado)

        # Procesar vuelto como diccionario
        vuelto_procesado = __procesar_vuelto__(lista_sin_duplicados)

        # Buscar el vuelto valido segun los billetes disponibles
        vuelto_valido = __encontrar_vuelto_valido__(vuelto_procesado)

        # Retornar el Diccionario final de resultados: None o Diccionario valido
        retorno = vuelto_valido
    else:
        # Si no existe un resultado, lanzar una excepcion
        raise ValueError("No se encontró un resultado.")

    return retorno

def __remover_duplicados__(lista):
    '''
    Esta funcion recibe y devuelve una lista sin elementos duplicados.
    '''
    lista_sin_duplicados = []
    for item in lista:
        if item not in lista_sin_duplicados:
            lista_sin_duplicados.append(item)
    return lista_sin_duplicados

 
def __procesar_vuelto__(vuelto):
    '''
    Esta funcion recibe un la lista de combinaciones de billetes como vuelto 
    y lo procesa para generar un diccionario con los distintos resultados posibles.
    Devuelve el diccionario ordenado.
    '''
    final = {}
    for i, item in enumerate(vuelto, start=1):
        # Crear clave para cada resultado
        resultado_clave = f"Resultado_{i}"
        final[resultado_clave] = {}
        
        # Procesar cada billete en el resultado
        for billete in item['Resultado']:
            # Remover los caracteres innecesarios
            billete = billete.strip(",'() ")
            denominacion, cantidad = billete.split(", ")
            
            # Crear clave para cada billete y agregar al diccionario
            final[resultado_clave][f"ARS_{denominacion}"] = int(cantidad)
        
    return __ordenar_por_denominacion__(final)


def __ordenar_por_denominacion__(diccionario):
    '''
    Esta función recibe el diccionario procesado de combinaciones de billetes posibles como vuelto
    y la ordena de manera que el primer resultado sea entregar la menor cantidad de billetes de la
    mayor denominación posible.
    '''

    # Definir las denominaciones en orden descendente
    denominaciones = ['Billetes_10000','Billetes_2000','Billetes_1000','Billetes_500','Billetes_200', 'Billetes_100', 'Billetes_50', 'Billetes_20', 'Billetes_10', 'Billetes_5']

    # Función de ordenación que crea una tupla de prioridad para cada resultado
    def prioridad(entry):
        _, billetes = entry
        # Crear una tupla de cantidades de cada denominación en orden descendente
        return tuple(billetes.get(den, 0) for den in denominaciones)

    # Ordenar el diccionario usando la función de prioridad en orden descendente
    dict_ordenado =  dict(sorted(diccionario.items(), key=prioridad, reverse=True))

    nuevo_diccionario = {f'Resultado_{i+1}': valor for i, (_, valor) in enumerate(dict_ordenado.items())}
    return nuevo_diccionario


def __encontrar_vuelto_valido__(resultados_vuelto):
    '''
    Esta función recibe un diccionario con los resultados de vuelto (Salida de la funcion calculo_vuelto_prolog) y 
    determina cual es posible en base a los billetes disponibles a en la caja registradora.    
    '''

    retorno = None
    
    # Se omiten los vueltos en dolares.
    billetes_vuelto = {
        "ARS_10000": 0,
        "ARS_2000": 0,
        "ARS_1000": 0,
        "ARS_500": 0,
        "ARS_200": 0,
        "ARS_100": 0,
        "ARS_50": 0,
        "ARS_20": 0,
        "ARS_10": 0,
        "ARS_5": 0
    }

    datos_caja = consultar_caja_registradora()
    for _, billetes_necesarios in resultados_vuelto.items():
        es_valido = True
        for billete, cantidad in billetes_necesarios.items():
            # Verificar si hay suficientes billetes en la caja
            if datos_caja[billete] < cantidad:
                es_valido = False
                break
        if es_valido:
            for key, value in billetes_necesarios.items():
                billetes_vuelto[key] += value
            retorno = billetes_vuelto
            break
    return retorno

def vuelto_valido_to_string(vuelto_valido):
    '''
    Esta función recibe un diccionario con un vuelto válido y lo convierte en un string para mostrar al usuario.
    '''
    retorno = ''
    if vuelto_valido:
        resultado = f"Entregar: "
        for billete, cantidad in vuelto_valido.items():
            resultado += f"{cantidad} billetes de ${billete[4:]}, "
        resultado = resultado.rstrip(', ')
        retorno = resultado
    else:
        retorno = "No hay vuelto disponible."
    return retorno
        
if __name__ == "__main__":

    # Caja simulada para este ejemplo:
    # {"ARS_10000": 0, "ARS_2000": 0, "ARS_1000": 0, "ARS_500": 1, "ARS_200": 2, "ARS_100": 1,
    #  "ARS_50": 0, "ARS_20": 0, "ARS_10": 0, "ARS_5": 0,
    #  "USD_100": 0, "USD_50": 0, "USD_20": 0, "USD_10": 0, "USD_5": 0, "USD_2": 0, "USD_1": 0}
    vuelto_prueba = 500
    vuelto_prueba_calculado = calculo_vuelto_prolog(vuelto_prueba)
    print("Resultado: \n")
    print(vuelto_prueba_calculado)
    print(vuelto_valido_to_string(vuelto_prueba_calculado))
