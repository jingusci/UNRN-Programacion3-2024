'''
Programación 3 - 2024 - Trabajo Integrador Final
Subproblema 2 - Grupo F
Alumnos:
 - Javier Ingusci
 - Enrique Mariotti
 - Joaquín Rodríguez

Este módulo calcula la combinación de billetes que hay que
usar para entregar el vuelto.
Para esto se usa la base de conocimiento de prolog y la
caja registradora simulada.
'''

from pyswip import Prolog
import caja_simulada as caja

prolog = Prolog()
prolog.consult("billetes.pl")

def combinaciones_que_suman(monto, moneda):
    '''
    Un generador para iterar por todas las combinaciones que suman el monto dado.
    Al iterar, cada item es un diccionario con denominaciones como llaves y
    cantidad de billetes como valores.

    Las combinaciones están ordenadas de manera que las primeras usan la mayor
    cantidad posible de los billetes más grandes. Esto ayuda a dar el vuelto
    con la menor cantidad posible de billetes.
    '''
    combinaciones = prolog.query(f'billetes_suman({moneda.lower()}, {monto}, X)')

    for combinación in combinaciones:
        # Convertir el formato de prolog al formato de la caja registradora:
        combinación_dict = {}
        for billete in combinación['X']:
            denominación, cantidad = billete.strip(',()').split(', ')
            denominación = f'{moneda.upper()}_{denominación}'
            combinación_dict[denominación] = int(cantidad)
        
        yield combinación_dict

def elegir_billetes(monto, moneda):
    '''
    Calcula qué billetes devolver.

    Recibe un monto y una moneda, y usa consultas a prolog y a la caja
    registradora para determinar qué billetes devolver. Si la moneda son
    pesos, el monto se redondea al múltiplo de 5 más cercano.

    La consulta a prolog genera una lista de todas las combinaciones posibles,
    y de esa lista se elije la primera combinación para la cual hay suficientes
    billetes en la caja.
    '''
    if moneda.upper() == 'ARS':
        monto = round(monto / 5) * 5

    for combinación in combinaciones_que_suman(monto, moneda):
        if caja.se_puede_retirar(combinación):
            return combinación
    
    raise RuntimeError(f'No hay billetes en la caja para entregar ${monto} {moneda}.')
 

def billetes_a_string(combinación):
    '''
    Recibe un diccionario con una combinación de billetes y lo convierte a string.
    '''
    return ', '.join(
        f'{cantidad} billetes de {denominación}'
        for denominación, cantidad in combinación.items()
    )
