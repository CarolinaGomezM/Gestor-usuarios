import unittest
import database as db
import copy
import helpers
import config
import csv

class TestDatabase(unittest.TestCase):
    def setUp(self) -> None:
        db.Clientes.lista = [
            db.Cliente('15J', 'Marta', 'Pérez'),
            db.Cliente('16K', 'Juan', 'Gómez'),
            db.Cliente('17L', 'Luis', 'García'),
        ]

    def test_buscar_cliente(self):
        cliente_existente = db.Clientes.buscar('16K')
        cliente_inexistente = db.Clientes.buscar('20K')
        self.assertIsNotNone(cliente_existente)
        self.assertIsNone(cliente_inexistente)

    def test_crear_cliente(self):
        nuevo_cliente = db.Clientes.crear('20K', 'Ana', 'Martínez')
        self.assertIn(nuevo_cliente, db.Clientes.lista)

    def test_modificar_cliente(self):
        cliente_modificado = db.Clientes.modificar('16K', 'Juan', 'Gómez Pérez')
        self.assertEqual(cliente_modificado.apellido, 'Gómez Pérez')

    def test_borrar_cliente(self):
        cliente_borrado = db.Clientes.borrar('17L')
        self.assertNotIn(cliente_borrado, db.Clientes.lista)

    def test_dni_valido(self):
        self.assertTrue(helpers.dni_valido('00A', db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('23423424S', db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('F35', db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('16K', db.Clientes.lista))

    def test_escritura_csv(self):
        db.Clientes.borrar('15J')
        db.Clientes.borrar('16K')
        db.Clientes.modificar('17L', 'Luis', 'García Pérez')

        dni, nombre, apellido = None, None, None

        with open(config.DATABASE_PATH, newline='\n') as fichero:
            reader = csv.reader(fichero, delimiter=';')
            dni, nombre, apellido = next(reader)

        self.assertEqual(dni, '17L')
        self.assertEqual(nombre, 'Luis')
        self.assertEqual(apellido, 'García Pérez')