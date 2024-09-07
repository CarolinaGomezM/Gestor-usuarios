import os
import helpers
import database as db

def iniciar():
    print("Iniciando el programa")
    while True:
        helpers.limpiar_pantalla()

        print("=====================================")
        print("Bienvenido al Gestor")
        print("=====================================")
        print("[1]. Listar los clientes")
        print("[2]. Buscar un cliente")
        print("[3]. Agregar un cliente")
        print("[4]. Modificar un cliente")
        print("[5]. Eliminar un cliente")
        print("[6]. Salir")
        print("=====================================")

        opcion = input("Seleccione una opción: ")
        helpers.limpiar_pantalla()

        if opcion == '1':
            print("Listando los clientes... \n ")
            for cliente in db.Clientes.lista:
                print(f"{cliente.dni} - {cliente.nombre} {cliente.apellido}")

        elif opcion == '2':
            print("Buscando los clientes... \n ")
            dni = helpers.leer_texto(3,3, "DNI (2 int y 1 char): ").upper()
            cliente = db.Clientes.buscar(dni)
            print(cliente) if cliente else print("Cliente no encontrado")

        elif opcion == '3':
            print("Añadiendo los clientes... \n ")
            dni = None
            while True:
                dni = helpers.leer_texto(3,3, "DNI (2 int y 1 char): ").upper()
                if helpers.dni_valido(dni, db.Clientes.lista):
                    break

            nombre = helpers.leer_texto(2,30, "Nombre (2 a 30 chars): ").capitalize()
            apellido = helpers.leer_texto(2,30, "Apellido (2 a 30 chars): ").capitalize()
            db.Clientes.crear(dni, nombre, apellido)
            print("Cliente añadido correctamente")

        elif opcion == '4':
            print("Modificando los clientes... \n ")
            dni = helpers.leer_texto(3,3, "DNI (2 int y 1 char): ").upper()
            cliente = db.Clientes.buscar(dni)

            if cliente:
                nombre = helpers.leer_texto(2,30, f"Nombre (2 a 30 chars): [{cliente.nombre}] ").capitalize()
                apellido = helpers.leer_texto(2,30, f"Apellido (2 a 30 chars):  [{cliente.apellido}]").capitalize()
                db.Clientes.modificar(dni, nombre, apellido)
                print("Cliente modificado correctamente")
            else:
                print("Cliente no encontrado")
            
        elif opcion == '5':
            print("Eliminando los clientes... \n ")
            dni = helpers.leer_texto(3,3, "DNI (2 int y 1 char): ").upper()
            cliente = db.Clientes.buscar(dni)
            if cliente:
                db.Clientes.borrar(dni)
                print("Cliente eliminado correctamente")
            else:
                print("Cliente no encontrado")
        elif opcion == '6':
            print("Saliendo... \n ")
            break

        input("\nPresione Enter para continuar...")
            
