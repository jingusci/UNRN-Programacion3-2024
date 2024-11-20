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

# Prototipos de funciones para conectar con el trabajo de los otros equipos:

def convertir_dolar_a_pesos(monto):
    '''
    Consulta el valor actual del dolar online para convertir el monto dado a pesos argentinos.
    Valor del dolar oficial.
    '''
    content = requests.get(f"https://www.x-rates.com/table/?from=USD&amount={monto}").content
    soup = bs(content, "html.parser")

    return int(soup.find(attrs={'href':'https://www.x-rates.com/graph/?from=USD&to=ARS'}).text.split(".")[0])

def registrar_ingreso(monto):
    '''
    Registra los datos de un ingreso al estacionamiento en
    las bases de datos que corresponda.
    '''
    print(f'Se registró un ingreso de AR$ {monto}.')