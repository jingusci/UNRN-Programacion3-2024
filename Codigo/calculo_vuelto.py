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

    # Lanzar excepción ante la llegada de un numero negativo
    if vuelto <= 0:
        raise ValueError(f"No es posible entregar ${vuelto} como vuelto")

    # Redondear el vuelto al multiplo de 5 mas cercano
    vuelto_multiplo_de_5 = round(vuelto / 5) * 5

    ### Abrir el archivo prolog
    prolog = Prolog()
    prolog.consult("billetes_v2.pl")

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

        # Retornar el Diccionario final de resultados
        return vuelto_valido
    else:
        # Si no existe un resultado, lanzar una excepcion
        raise ValueError("No se encontró un resultado.")


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
            final[resultado_clave][f"Billetes_{denominacion}"] = int(cantidad)
        
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

    billetes_vuelto = {
        "Billetes_10000": 0,
        "Billetes_2000": 0,
        "Billetes_1000": 0,
        "Billetes_500": 0,
        "Billetes_200": 0,
        "Billetes_100": 0,
        "Billetes_50": 0,
        "Billetes_20": 0,
        "Billetes_10": 0,
        "Billetes_5": 0
    }

    datos_caja = consultar_caja_registradora()
    for clave, billetes_necesarios in resultados_vuelto.items():
        es_valido = True
        for billete, cantidad in billetes_necesarios.items():
            # Verificar si hay suficientes billetes en la caja
            if datos_caja.get(billete, 0) < cantidad:
                es_valido = False
                break
        if es_valido:
            # return {clave: billetes_necesarios}
            for key, value in billetes_necesarios.items():
                billetes_vuelto[key] += value
    return billetes_vuelto  # Retornar None si no se encuentra un resultado válido



def vuelto_valido_to_string(vuelto_valido):
    '''
    Esta función recibe un diccionario con un vuelto válido y lo convierte en un string para mostrar al usuario.
    '''
    if vuelto_valido:
        for clave, billetes in vuelto_valido.items():
            resultado = f"Entregar: "
            for billete, cantidad in billetes.items():
                resultado += f"{cantidad} billetes de ${billete[9:]}, "
            resultado = resultado.rstrip(', ')
            return resultado
    else:
        return "No hay vuelto disponible."
        
                



#### Funcion para validar que el archivo funciona correctamente

vuelto_prueba = 500
vuelto_prueba_calculado = calculo_vuelto_prolog(vuelto_prueba)
# vuelto_prueba_calculado_2 = vuelto_valido_to_string(vuelto_prueba_calculado)

print("Resultado: \n")
print(vuelto_prueba_calculado)