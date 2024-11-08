# Importar las librerias
from pyswip import Prolog

def remover_duplicados(lista):
    '''
    Esta funcion recibe y devuelve una lista sin elementos duplicados.
    '''
    lista_sin_duplicados = []
    for item in lista:
        if item not in lista_sin_duplicados:
            lista_sin_duplicados.append(item)
    return lista_sin_duplicados

 
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
    prolog.consult("billetes.pl")

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
    
    return final