import csv
import config

class Cliente:
    def __init__(self, dni, nombre, apellido):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    def __str__(self):
        return f'{self.dni} - {self.nombre} {self.apellido}'
    

class Clientes:

    lista = []
    with open(config.DATABASE_PATH, newline='\n') as fichero:
        reader = csv.reader(fichero, delimiter=';')
        for dni, nombre, apellido in reader:
            cliente = Cliente(dni, nombre, apellido)
            lista.append(cliente)

    @staticmethod
    def buscar(dni):
        for c in Clientes.lista:
            if c.dni == dni:
                return c
        return None
    
    @staticmethod
    def crear(dni, nombre, apellido):
        c = Cliente(dni, nombre, apellido)
        Clientes.lista.append(c)
        Clientes.guardar()
        return c
    
    @staticmethod
    def modificar(dni, nombre, apellido):
        c = Clientes.buscar(dni)
        if c:
            c.nombre = nombre
            c.apellido = apellido
            Clientes.guardar()
            return c
    
    @staticmethod
    def borrar(dni):
        c = Clientes.buscar(dni)
        if c:
            Clientes.lista.remove(c)
            Clientes.guardar()
            return c

    @staticmethod
    def guardar():
        with open(config.DATABASE_PATH, 'w', newline='\n') as fichero:
            writer = csv.writer(fichero, delimiter=';')
            for c in Clientes.lista:
                writer.writerow([c.dni, c.nombre, c.apellido])   
    
