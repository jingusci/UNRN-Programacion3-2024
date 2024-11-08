'''
Programación 3 - 2024 - Trabajo Integrador Final
Subproblema 2 - Grupo F
Alumnos:
 - Javier Ingusci
 - Enrique Mariotti
 - Joaquín Rodríguez
'''

# Librerias
from calculo_vuelto import *


# Prototipos de funciones para conectar con el trabajo de los otros equipos:

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
    Consulta el valor actual del dolar en una base de datos antes
    de realizar la conversión.
    '''

    # Esta funcion tiene que ir a consultar una BD de otro grupo.
    # TODO - Implementar la consulta a la BD de precios
    # TODO - Importar las librerías necesarias para la conexión a la BD
    # TODO - Borrar linea de ejemplo

    valor_dolar = 1200 #ejemplo
    return monto * valor_dolar

def registrar_ingreso(tipo_estacionamiento, monto):
    '''
    Registra los datos de un ingreso al estacionamiento en
    las bases de datos que corresponda.
    '''
    print(f'Se registró un ingreso de tipo {tipo_estacionamiento}, se cobró {monto}.')

######################################################################    

# Prototipos de funciones para interactuar con el usuario:

def esperar_nuevo_cliente():
    '''
    Espera hasta que el sistema se active por la llegada
    de un auto.
    '''
    pass

def consultar_tipo_estacionamiento():
    tipo = "General" #ejemplo
    return tipo

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

def entregar_vuelto(monto_ingresado, valor_estacionamiento):
    '''
    Funcion para calcular el vuelto e indicar la combinacion 
    de billetes a entregar.
    '''

    # Calculo del vuelto
    vuelto = monto_ingresado - valor_estacionamiento

    # Calculo de billetes a entregar (consulta al prolog)
    vuelto_completo = calculo_vuelto_prolog(vuelto) 
    
    # Resultado del vuelto -> Impresion por pantalla
    # TODO - Cambiar a un return
    # TODO - Estoy solo entregando la opcion 1.
    print(f"Vuelto a entregar: ${vuelto}.\n")
    print(f"Billetes a entregar: \n{(vuelto_completo['Resultado_1'])}")

def recibir_billetes(valor_estacionamiento):
    '''
    Recibe billetes hasta alcanzar el monto, y entrega el vuelto que corresponda.
    '''
    print(f'Monto a ingresar: ${valor_estacionamiento}.')

    monto_ingresado = 0
    while monto_ingresado < valor_estacionamiento:
        print('Ingrese un billete.')
        valido, denominacion, moneda = identificar_billete()

        if valido:
            if moneda == "USD":
                denominacion = convertir_dolar_a_pesos(denominacion)
            monto_ingresado += denominacion
            print(f"Billete de ${denominacion} {moneda} aceptado.")
        else:
            print("Billete inválido, devuelto al cliente.")
        
        print(f'Usted ingresó ${monto_ingresado} de ${valor_estacionamiento}.')

    # Si cuando sale del bucle el costo es mayor, significa que debemos dar vuelto
    if monto_ingresado > valor_estacionamiento:
        entregar_vuelto(monto_ingresado, valor_estacionamiento)

def entregar_comprobante(monto):
    '''
    Imprime un comprobante para el usuario.
    '''
    print(f"Se imprimió un comprobante por un cobro de ${monto}.")

# Lógica de funcionamiento:

def cobrar_estacionamiento():
    tipo_estacionamiento = consultar_tipo_estacionamiento()
    valor_estacionamiento = consultar_precio_estacionamiento(tipo_estacionamiento)
    recibir_billetes(valor_estacionamiento)
    entregar_comprobante(valor_estacionamiento)
    registrar_ingreso(tipo_estacionamiento, valor_estacionamiento)



def main():
    '''
    Función principal del programa.    
    '''
    while True:
        esperar_nuevo_cliente()
        cobrar_estacionamiento()
        if input("Cobrar de nuevo [s - n]:  ").lower() != 's': break



# Ejecución del programa
if __name__ == "__main__":
    main()