'''
Programación 3 - 2024 - Trabajo Integrador Final
Subproblema 2 - Grupo F
Alumnos:
 - Javier Ingusci
 - Enrique Mariotti
 - Joaquín Rodríguez

Éste módulo mantiene la cuenta de la cantidad de billetes de cada
denominación que hay en la caja registradora. Los datos se mantienen
en un archivo json.

Todas las funciones que reciben cantidades de dinero como argumento,
esperan un diccionario en el cual las llaves son denominaciones (las
que aparecen en la lista DENOMINACIONES son la únicas válidas) y los
valores son cantidades de billetes.
'''

import json
import random

DENOMINACIONES = ["ARS_10000", "ARS_2000", "ARS_1000", "ARS_500", "ARS_200", "ARS_100", "ARS_50", "ARS_20", "ARS_10", "ARS_5", "USD_100", "USD_50", "USD_20", "USD_10", "USD_5", "USD_2", "USD_1"]

_filename = 'caja_simulada.json'

def _escribir_datos(valores):
    '''
    Recibe un diccionario con las cantidades de cada denominación y
    lo escribe al archivo.
    '''
    with open(_filename, 'w') as json_file:
        valores = json.dump(valores, json_file)

def consultar():
    '''
    Devuelve un diccionario con los datos leídos del archivo.
    '''
    with open(_filename, 'r') as json_file:
        valores = json.load(json_file)
    
    return valores

def randomizar():
    '''
    Inicializa la caja en un estado aleatorio.
    La cantidad maxima de billetes de cada denominación es 500.
    '''
    cantidades = {denominacion: random.randint(0, 500) for denominacion in DENOMINACIONES}
    _escribir_datos(cantidades)

def ingresar(ingreso):
    '''
    Registra ingreso de billetes a la caja.
    ingreso debe ser un diccionario con denominaciones como llaves.
    '''
    cantidades = consultar()

    # Sumar billetes según denominaciones
    for denominacion, cantidad in ingreso.items():
        cantidad[denominacion] += cantidad

    _escribir_datos(cantidades)

def retirar(egreso):
    '''
    Retira dinero de la caja.
    egreso debe ser un diccionario con denominaiones como llaves.
    Se levanta una excepción si no alcanza el dinero en la caja.
    '''
    cantidades = consultar()

    # Verificar que se puede entregar la cantidad solicitada:
    for denominacion, cantidad_solicitada in egreso.items():
        if cantidades[denominacion] < cantidad_solicitada:
            raise ValueError(f'No se pueden entregar {cantidad_solicitada} billetes de {denominacion}. El máximo disponible es {cantidades[denominacion]}.')
    
    # Restar billetes retirados:
    for denominacion, cantidad in egreso.items():
        cantidad[denominacion] -= cantidad

    _escribir_datos(cantidades)

def se_puede_retirar(combinación):
    cantidades_disponibles = consultar()

    alcanza = True
    for denominación, cantidad_solicitada in combinación.items():
        if cantidad_solicitada > cantidades_disponibles[denominación]:
            alcanza = False
            break
    
    return alcanza

