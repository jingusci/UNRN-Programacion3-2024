'''
Programación 3 - 2024 - Trabajo Integrador Final
Subproblema 2 - Grupo F
Alumnos:
 - Javier Ingusci
 - Enrique Mariotti
 - Joaquín Rodríguez
'''

import re

palabras_claves = {
        "ARS_10000":    ['10000','argentina'],
        "ARS_2000":     ['2000','argentina'],
        "ARS_1000":     ['1000','argentina'],
        "ARS_500":      ['500','argentina'],
        "ARS_200":      ['200','argentina'],
        "ARS_100":      ['100','argentina'],
        "ARS_50":       ['50','argentina'],
        "ARS_20":       ['20','argentina'],
        "ARS_10":       ['10','argentina'],
        "ARS_5":        ['5','argentina'],
        "USD_100":      ['100','united', 'states', 'america'],
        "USD_50":       ['50','united', 'states', 'america'],
        "USD_20":       ['20','united', 'states', 'america'],
        "USD_10":       ['10','united', 'states', 'america'],
        "USD_5":        ['5','united', 'states', 'america'],
        "USD_2":        ['2','united', 'states', 'america'],
        "USD_1":        ['1','united', 'states', 'america']
    }

# TODO: Esta tiene que llamar a todas las sub-funciones. 
# def identificar_billete():
#     '''
#     Interactúa con la máquina lectora de billetes (¿y posiblemente con una
#     base de conocimiento en prolog? eso no nos quedó claro), devuelve los
#     datos del billete ingresado.
#     '''
#     valido = True  # Simulación de billete válido
#     denominacion = 500  # Ejemplo de denominación en ARS
#     moneda = "ARS"  # Puede ser "ARS" o "USD"
#     return valido, denominacion, moneda

def reconocer_texto(texto):
    '''
    Reconocimiento del texto de la red neuronal que describe la imagen. 
    '''

    # Filtrar (A-Z, a-z, 0-9)
    texto_filt = re.sub(r'[^a-zA-Z0-9\s]', '', texto)

    # Lista filtrada
    palabras = [palabra.lower() for palabra in texto_filt.split()] 

    # Eliminar palabras repetidas 
    palabras_unicas = []  
    for palabra in palabras: 
        if palabra not in palabras_unicas:
            palabras_unicas.append(palabra)
    
    # Diccionario de palabras claves
    dict_coincidencias = {key: None for key in palabras_claves}

    # Verificar coincidencias con las palabras claves
    for key, value in palabras_claves.items():
        coincidencia = set(value).issubset(palabras_unicas)
        if coincidencia:
            dict_coincidencias[key] = True

    # La validez se da si solo existe una coincidencia.             
    keys_coincidencias = [key for key, value in dict_coincidencias.items() if value]
    valido = len(keys_coincidencias) == 1

    if valido:
        moneda = keys_coincidencias[0].split('_')[0]
        denominacion = keys_coincidencias[0].split('_')[1]
    else:
        denominacion = None
        moneda = None
    
    return valido, denominacion, moneda

# Ejecución del programa
if __name__ == "__main__":
    pass