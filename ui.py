from tkinter import *
from tkinter import ttk
import database as db
from tkinter.messagebox import askokcancel, WARNING
import helpers

class CenterWidgetMixin:
     def center(self):
        self.update()
        self.geometry(f'+{self.winfo_screenwidth()//2 - self.winfo_width()//2}+{self.winfo_screenheight()//2 - self.winfo_height()//2}')


class CreateClientWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Agregar cliente')
        self.build()
        self.center()
        self.transient(parent) # Este junto con grab_set() hace que la ventana sea modal (no se puede interactuar con la ventana padre)
        self.grab_set()

    def build(self):
        frame = Frame(self)
        frame.pack(padx=20, pady=10)

        Label(frame, text='DNI: 2 ints y 1 upper char').grid(row=0, column=0)
        Label(frame, text='Nombre: 2-30 chars').grid(row=0, column=1)
        Label(frame, text='Apellido: 2-30 chars').grid(row=0, column=2)

        dni = Entry(frame)
        dni.grid(row=1, column=0)
        dni.bind('<KeyRelease>', lambda event: self.validate(event, 0))

        nombre = Entry(frame)
        nombre.grid(row=1, column=1)
        nombre.bind('<KeyRelease>', lambda event: self.validate(event, 1))

        apellido = Entry(frame)
        apellido.grid(row=1, column=2)
        apellido.bind('<KeyRelease>', lambda event: self.validate(event, 2))

        frame = Frame(self)
        frame.pack(pady=10)

        crear = Button(frame, text='Crear', command=self.create_client)
        crear.configure(state=DISABLED)
        crear.grid(row=0, column=0)
        Button(frame, text='Cancelar', command=self.close).grid(row=0, column=1)

        self.validaciones = [0,0,0]
        self.crear = crear
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    def create_client(self):
        self.master.treeview.insert(
                parent='',
                index='end',
                iid=self.dni.get(),
                values=(self.dni.get(), self.nombre.get(), self.apellido.get())
            )
        db.Clientes.crear(self.dni.get(), self.nombre.get(), self.apellido.get())
        self.close()

    def close(self):
        self.destroy()
        self.update()

    def validate(self, event, index):
        valor = event.widget.get()
        # if index == 0:
        #     valido = helpers.dni_valido(valor, db.Clientes.lista)
        #     if valido:
        #         event.widget.configure({"bg": "green"})
        #     else:
        #         event.widget.configure({"bg": "red"})

        # if index == 1:
        #     valido = valor.isalpha() and 2 <= len(valor) <= 30
        #     if valido:
        #         event.widget.configure({"bg": "green"})
        #     else:
        #         event.widget.configure({"bg": "red"})

        # if index == 2:
        #     valido = valor.isalpha() and 2 <= len(valor) <= 30
        #     if valido:
        #         event.widget.configure({"bg": "green"})
        #     else:
        #         event.widget.configure({"bg": "red"})

        valido = helpers.dni_valido(valor, db.Clientes.lista) if index == 0 else valor.isalpha() and 2 <= len(valor) <= 30
        event.widget.configure({"bg": "green"} if valido else {"bg": "red"})

        #Cambiar el estado del botón en base a las validaciones
        self.validaciones[index] = valido
        self.crear.config(state=NORMAL if self.validaciones == [1,1,1] else DISABLED)


class EditClientWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Actualizar cliente')
        self.build()
        self.center()
        self.transient(parent) # Este junto con grab_set() hace que la ventana sea modal (no se puede interactuar con la ventana padre)
        self.grab_set()

    def build(self):
        frame = Frame(self)
        frame.pack(padx=20, pady=10)

        Label(frame, text='DNI: (No editable)').grid(row=0, column=0)
        Label(frame, text='Nombre: 2-30 chars').grid(row=0, column=1)
        Label(frame, text='Apellido: 2-30 chars').grid(row=0, column=2)

        dni = Entry(frame)
        dni.grid(row=1, column=0)

        nombre = Entry(frame)
        nombre.grid(row=1, column=1)
        nombre.bind('<KeyRelease>', lambda event: self.validate(event, 0))

        apellido = Entry(frame)
        apellido.grid(row=1, column=2)
        apellido.bind('<KeyRelease>', lambda event: self.validate(event, 1))

        client = self.master.treeview.focus() # Códigos para obtener un cliente seleccionado
        campos = self.master.treeview.item(client, "values")
        dni.insert(0, campos[0])
        dni.configure(state=DISABLED)
        nombre.insert(0, campos[1])
        apellido.insert(0, campos[2])

        frame = Frame(self)
        frame.pack(pady=10)

        actualizar = Button(frame, text='Actualizar', command=self.update_client)
        actualizar.grid(row=0, column=0)
        Button(frame, text='Cancelar', command=self.close).grid(row=0, column=1)

        self.validaciones = [1,1]
        self.actualizar = actualizar
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    def update_client(self):
        cliente = self.master.treeview.focus()
        self.master.treeview.item(cliente, values=(self.dni.get(), self.nombre.get(), self.apellido.get()))
        db.Clientes.modificar(self.dni.get(), self.nombre.get(), self.apellido.get())
        self.close()

    def close(self):
        self.destroy()
        self.update()

    def validate(self, event, index):
        valor = event.widget.get()

        valido = (valor.isalpha() and 2 <= len(valor) <= 30)
        event.widget.configure({"bg": "green"} if valido else {"bg": "red"})

        #Cambiar el estado del botón en base a las validaciones
        self.validaciones[index] = valido
        self.actualizar.config(state=NORMAL if self.validaciones == [1,1] else DISABLED)


class MainWindow(Tk, CenterWidgetMixin):
    def __init__(self):
        super().__init__()
        self.title('Gestión de clientes')
        self.build()
        self.center()
    
    def build(self):
        frame = Frame(self)
        frame.pack()

        treeview = ttk.Treeview(frame)
        treeview['columns'] = ('DNI', 'Nombre', 'Apellido')

        treeview.column("#0", width=0, stretch=NO)
        treeview.column("DNI", anchor=CENTER)
        treeview.column("Nombre", anchor=CENTER)
        treeview.column("Apellido", anchor=CENTER)

        treeview.heading("DNI", text="DNI", anchor=CENTER)
        treeview.heading("Nombre", text="Nombre", anchor=CENTER)
        treeview.heading("Apellido", text="Apellido", anchor=CENTER)


        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        treeview['yscrollcommand'] = scrollbar.set

        for cliente in db.Clientes.lista:
            treeview.insert(
                parent='',
                index='end',
                iid=cliente.dni,
                values=(cliente.dni, cliente.nombre, cliente.apellido)
            )


        treeview.pack()

        frame = Frame(self)
        frame.pack(pady=20)

        Button(frame, text='Agregar', command=self.create).grid(row=0, column=0)
        Button(frame, text='Modificar', command=self.edit).grid(row=0, column=1)
        Button(frame, text='Borrar', command=self.delete).grid(row=0, column=2)

        self.treeview = treeview

    def delete(self):
        cliente = self.treeview.focus()
        if cliente:
            campos = self.treeview.item(cliente, "values")
            confirmar = askokcancel('Confirmar', f'¿Está seguro de eliminar a {campos[1]} {campos[2]}?', icon=WARNING)
            if confirmar:
                self.treeview.delete(cliente)
                db.Clientes.borrar(campos[0])

    
    def create(self):
        CreateClientWindow(self)

    def edit(self):
        if self.treeview.focus():
            EditClientWindow(self)


if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()