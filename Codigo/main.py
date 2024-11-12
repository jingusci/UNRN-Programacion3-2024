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
from consultas_bd import *
from recon_billetes import *

# Prototipos de funciones para interactuar con el usuario:

def esperar_nuevo_cliente():
    '''
    Espera hasta que el sistema se active por la llegada
    de un auto.
    '''
    pass


def entregar_vuelto(monto_ingresado, valor_estacionamiento):
    '''
    Funcion para calcular el vuelto e indicar la combinacion 
    de billetes a entregar.
    '''

    # Calculo del vuelto
    vuelto = monto_ingresado - valor_estacionamiento

    # Calculo de billetes a entregar (consulta al prolog)
    vuelto_completo = calculo_vuelto_prolog(vuelto)

    # Encontrar vuelto valido
    vuelto_valido = encontrar_vuelto_valido(vuelto_completo)

    # Resultado del vuelto -> Impresion por pantalla
    # TODO - Cambiar a un return
    print(f"Vuelto a entregar: ${vuelto}.\n")
    # print(vuelto_valido_to_string(vuelto_valido))


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


# ---  Función principal del programa  ---

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