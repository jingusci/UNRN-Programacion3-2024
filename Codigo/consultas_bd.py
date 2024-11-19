'''
Programación 3 - 2024 - Trabajo Integrador Final
Subproblema 2 - Grupo F
Alumnos:
 - Javier Ingusci
 - Enrique Mariotti
 - Joaquín Rodríguez

 Este módulo hace consultas a las distintas bases de datos.
'''
import requests
from bs4 import BeautifulSoup as bs
from dateutil.parser import parse

# Prototipos de funciones para conectar con el trabajo de los otros equipos:

def consultar_tipo_estacionamiento():
    tipo = "General" #ejemplo
    return tipo

def consultar_precio_estacionamiento(tipo_estacionamiento):
    '''
    Consulta el precio en la Base de Datos de otro grupo que tiene
    los precios actualizados.
    '''
    # Esta funcion tiene que ir a consultar una BD de otro grupo.
    # TODO - Implementar la consulta a la BD de precios
    # TODO - Importar las librerías necesarias para la conexión a la BD

    if tipo_estacionamiento == "General":
        valor_estacionamiento = 100  # Ejemplo de precio para tipo "General"
    else:
        valor_estacionamiento = 150  # Ejemplo para otros tipos
    return valor_estacionamiento

def convertir_dolar_a_pesos(monto):
    '''
    Consulta el valor actual del dolar online para convertir el monto dado a pesos argentinos.
    Valor del dolar oficial! xD
    '''
    content = requests.get(f"https://www.x-rates.com/table/?from=USD&amount={monto}").content
    soup = bs(content, "html.parser")

    return int(soup.find(attrs={'href':'https://www.x-rates.com/graph/?from=USD&to=ARS'}).text.split(".")[0])

def registrar_ingreso(tipo_estacionamiento, monto):
    '''
    Registra los datos de un ingreso al estacionamiento en
    las bases de datos que corresponda.
    '''
    print(f'Se registró un ingreso de tipo {tipo_estacionamiento}, se cobró {monto}.')

def consultar_caja_registradora():
    '''
    Consulta el monto actual en la caja registradora.
    '''

    return consultar_caja()
