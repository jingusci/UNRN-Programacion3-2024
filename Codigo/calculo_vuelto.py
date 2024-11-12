# Importar las librerias
from pyswip import Prolog

from consultas_bd import consultar_caja_registradora

def calculo_vuelto_prolog(vuelto):
    '''
    Esta funcion recibe un monto de vuelto y devuelve una lista con todas las posibles 
    combinaciones de billetes a dar de vuelto.
    Redondea el vuelto al multiplo de 5 mas cercano.
    '''

    # Redondear el vuelto al multiplo de 5 mas cercano
    vuelto_multiplo_de_5 = round(vuelto / 5) * 5

    ### Abrir el archivo prolog
    prolog = Prolog()
    prolog.consult("billetes_v2.pl")

    # Ejecutar la consulta prolog y convertir el resultado en una lista
    # Esta lista contiene todas las posibilidades de vuelto que se pueden dar
    resultado = list(prolog.query(f"calcular_vuelto({vuelto_multiplo_de_5}, Resultado)"))

    if resultado:
        # Remover duplicados de la lista
        lista_sin_duplicados = remover_duplicados(resultado)

        # Procesar vuelto como diccionario
        vuelto_procesado = procesar_vuelto(lista_sin_duplicados)

        # Retornar la lista sin duplicados
        return vuelto_procesado
    else:
        # Si no existe un resultado, lanzar una excepcion
        raise ValueError("No se encontró un resultado.")


def remover_duplicados(lista):
    '''
    Esta funcion recibe y devuelve una lista sin elementos duplicados.
    '''
    lista_sin_duplicados = []
    for item in lista:
        if item not in lista_sin_duplicados:
            lista_sin_duplicados.append(item)
    return lista_sin_duplicados

 
def procesar_vuelto(vuelto):
    '''
    Esta funcion recibe un monto de vuelto y lo procesa para mostrarlo al usuario.
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
        
    return ordenar_por_denominacion(final)


def ordenar_por_denominacion(diccionario):
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

def encontrar_vuelto_valido(resultados_vuelto):
    '''
    Esta función recibe un diccionario con los resultados de vuelto y 
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
        
                



