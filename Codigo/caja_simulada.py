'''
Programación 3 - 2024 - Trabajo Integrador Final
Subproblema 2 - Grupo F
Alumnos:
 - Javier Ingusci
 - Enrique Mariotti
 - Joaquín Rodríguez
'''

import json
import random

def inicializar_caja_random():
    '''
    Inicializar la caja en un estado aleatorio.
    La cantidad maxima de billetes de cada denominacion son 500.
    '''
    caja_simulada = {
        "ARS_10000":    0,
        "ARS_2000":     0,
        "ARS_1000":     0,
        "ARS_500":      0,
        "ARS_200":      0,
        "ARS_100":      0,
        "ARS_50":       0,
        "ARS_20":       0,
        "ARS_10":       0,
        "ARS_5":        0,
        "USD_100":      0,
        "USD_50":       0,
        "USD_20":       0,
        "USD_10":       0,
        "USD_5":        0,
        "USD_2":        0,
        "USD_1":        0
    }

    # Inicializar los valores de la caja
    for key, value in caja_simulada.items():
        caja_simulada[key] = random.randint(0, 500)

    # Convertir a json
    with open("caja_simulada.json", "w") as json_file: 
        json.dump(caja_simulada, json_file)

    return caja_simulada


def consultar_caja():
    '''
    Consulta a la caja simulada.
    '''
    # Abrir json
    with open('caja_simulada.json') as json_file:
        caja_simulada = json.load(json_file)

    return caja_simulada

def ingreso_caja(ingreso):
    '''
    Ingreso a caja (ARS o USD).
    '''
    # Abrir json
    with open('caja_simulada.json') as json_file:
        caja_simulada = json.load(json_file)

    # Sumar billetes segun denominaciones
    for key, value in caja_simulada.items():
        caja_simulada[key] += ingreso[key]

    # Convertir a json
    with open("caja_simulada.json", "w") as json_file: 
        json.dump(caja_simulada, json_file)

    return caja_simulada

def egreso_caja(egreso):
    '''
    Egreso a caja (ARS).
    '''
    # Abrir json
    with open('caja_simulada.json') as json_file:
        caja_simulada = json.load(json_file)

    # Sumar billetes segun denominaciones
    for key, value in caja_simulada.items():
        caja_simulada[key] -= egreso[key]
        if caja_simulada[key] < 0:
            caja_simulada[key] = 0

    # Convertir a json
    with open("caja_simulada.json", "w") as json_file: 
        json.dump(caja_simulada, json_file)

    return caja_simulada

# Ejecución del programa
if __name__ == "__main__":

    monto = {
        "ARS_10000":    0,
        "ARS_2000":     0,
        "ARS_1000":     0,
        "ARS_500":      0,
        "ARS_200":      0,
        "ARS_100":      0,
        "ARS_50":       0,
        "ARS_20":       10,
        "ARS_10":       0,
        "ARS_5":        0,
        "USD_100":      0,
        "USD_50":       0,
        "USD_20":       0,
        "USD_10":       0,
        "USD_5":        0,
        "USD_2":        0,
        "USD_1":        0
    }

    # Operaciones nominales    
    print(inicializar_caja_random())
    print('\n')
    print(consultar_caja())
    print('\n')
    print(ingreso_caja(monto))
    print('\n')
    print(egreso_caja(monto))
    print('\n')

    # Casos de error
    monto['ARS_20'] = 10* consultar_caja()['ARS_20']
    print(egreso_caja(monto))


    
