'''
Programación 3 - 2024 - Trabajo Integrador Final
Subproblema 2 - Grupo F
Alumnos:
 - Javier Ingusci
 - Enrique Mariotti
 - Joaquín Rodríguez
'''


def identificar_billete():
    '''
    Interactúa con la máquina lectora de billetes (¿y posiblemente con una
    base de conocimiento en prolog? eso no nos quedó claro), devuelve los
    datos del billete ingresado.
    '''
    valido = True  # Simulación de billete válido
    denominacion = 500  # Ejemplo de denominación en ARS
    moneda = "ARS"  # Puede ser "ARS" o "USD"
    return valido, denominacion, moneda