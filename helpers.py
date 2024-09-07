import os
import platform
import re

def limpiar_pantalla():
    os.system("cls") if platform.system() == "Windows" else os.system("clear")


def leer_texto(longitud_min=0, longitud_max=100, mensaje=None):
    print(mensaje) if mensaje else None
    while True:
        texto = input(">: ")
        if longitud_min <= len(texto) <= longitud_max:
            return texto
        print(f"El texto debe tener entre {longitud_min} y {longitud_max} caracteres")


def dni_valido(dni, lista):
    if not re.match('[0-9]{2}[A-Z]$', dni):
        print("DNI incorrecto, debe tener 2 dígitos y una letra")
        return False
    for cliente in lista:
        if cliente.dni == dni:
            print("Ya existe un cliente con ese DNI")
            return False
    return True