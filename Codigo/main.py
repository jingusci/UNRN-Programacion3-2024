'''
Programación 3 - 2024 - Trabajo Integrador Final
Subproblema 2 - Grupo F
Alumnos:
 - Javier Ingusci
 - Enrique Mariotti
 - Joaquín Rodríguez
'''
import calculo_vuelto
import consultas_bd
import recon_billetes
import caja_simulada as caja
import sys

# Funciones para interactuar con el usuario:

def entregar_vuelto(moneda, monto_ingresado, valor_estacionamiento):
    '''
    Calcular el vuelto y lo entrega al cliente.
    Si la moneda es pesos, el monto se redondea al múltiplo de 5 más cercano.
    '''
    vuelto = monto_ingresado - valor_estacionamiento
    if moneda.upper() == 'ARS':
        vuelto = round(vuelto / 5) * 5

    billetes_a_entregar = calculo_vuelto.elegir_billetes(vuelto, moneda)
    caja.retirar(billetes_a_entregar)

    print(f"Se entregó ${vuelto} {moneda} de vuelto.")


def cobrar(valor_estacionamiento):
    '''
    Recibe billetes hasta alcanzar el monto, y entrega el vuelto que corresponda.
    '''
    print(f'Ingrese billetes. \nMonto total a ingresar: ${valor_estacionamiento} ARS.')

    monto_ingresado = 0
    while monto_ingresado < valor_estacionamiento:
        print('Ingrese un billete.')
        imagen = recon_billetes.escanear_billete() # dummy, devuelve un path a una imagen
        valido, denominacion, moneda = recon_billetes.identificar_billete(imagen)

        if valido:
            print(f"Billete de ${denominacion} {moneda} aceptado.")
            caja.ingresar({f"{moneda}_{denominacion}": 1})
            if moneda == "USD":
                denominacion = consultas_bd.convertir_dolar_a_pesos(denominacion)
            monto_ingresado += denominacion
        else:
            print("Billete inválido, devuelto al cliente.")
        
        print(f'Usted ingresó ${monto_ingresado} de ${valor_estacionamiento}.')

    # Si cuando sale del bucle el costo es mayor, significa que debemos dar vuelto
    if monto_ingresado > valor_estacionamiento:
        entregar_vuelto('ARS', monto_ingresado, valor_estacionamiento)

def entregar_comprobante(monto):
    '''
    Imprime un comprobante para el usuario.
    '''
    print(f"Se imprimió un comprobante por un cobro de ${monto} ARS.")

def cobrar_estacionamiento(valor_estacionamiento):
    '''
    Funcion principal de cobro automatizado.
    '''
    cobrar(valor_estacionamiento)
    entregar_comprobante(valor_estacionamiento)
    consultas_bd.registrar_ingreso(valor_estacionamiento)

# Ejecucion del programa por consola    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python main.py <monto_a_cobrar>")
        sys.exit(1)

    try:
        monto_a_cobrar = float(sys.argv[1])
    except ValueError:
        print("Error: <monto_a_cobrar> debe ser un número válido.")
        sys.exit(1)

    if monto_a_cobrar <= 0:
        raise RuntimeError('Monto invalido.')
    
    print("Generando una caja aleatoria...")
    caja.randomizar()
    print("") ## Separador

    print("Caja Inicial: \n" + caja.caja_simulada_to_string())
    print("") ## Separador
    
    print(f"Monto a cobrar de estacionamiento: ${monto_a_cobrar}")
    cobrar_estacionamiento(monto_a_cobrar)

    print("") ## Separador
    print("Caja Final: \n" + caja.caja_simulada_to_string())
    print("") ## Separador