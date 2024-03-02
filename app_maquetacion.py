from tkinter import *
from tkinter import ttk, filedialog
import sqlite3
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox

#############################################################################################
# FUNCIONES
#############################################################################################

def crear_base_datos():
    # Conectar a la base de datos (si no existe, se creará)
    conexion = sqlite3.connect('basededatos.db')
    cursor = conexion.cursor()

    # Crear tabla si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS materiales (
                        id INTEGER PRIMARY KEY,
                        material TEXT NOT NULL,
                        descripcion TEXT NOT NULL,
                        precio_venta REAL NOT NULL,
                        precio_costo REAL NOT NULL,
                        stock INTEGER NOT NULL,
                        proveedor TEXT NOT NULL)''')

    # Guardar los cambios y cerrar la conexión
    conexion.commit()
    conexion.close()

#falta definir
def imprimir_base_datos_inicio():
    # imprimo el detalle de la base de datos en un treeview()
    conexion = sqlite3.connect('basededatos.db')
    cursor  = conexion.cursor()

    # Obtengo todos los registros de la tabla materiales
    cursor.execute("SELECT * FROM materiales")
    registros = cursor.fetchall()

    #cierro la conexion  para que no quede abierta toda la vida
    conexion.close()

    # limpio los campos del treeview
    for registros in tree.get_children():
        tree.delete(registros)

    # imprimo los registros de la base en el treeview
    for row in registros:
        tree.insert('', 'end', value=row)




def exportar_base():
    #imprimo en consola a modo testing para ver si se ejecuta la funcion.
    #esta funcion exporta a txt la base dando la opcion de elegir donde guardar el archivo

    print("Exportando base...")
    # Pedir al usuario que seleccione la ubicación y el nombre del archivo
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
    
    if file_path:
        # Conectar a la base de datos
        conexion = sqlite3.connect('basededatos.db')
        cursor = conexion.cursor()

        # Obtener todos los registros de la tabla materiales
        cursor.execute("SELECT * FROM materiales")
        registros = cursor.fetchall()

        # Cerrar la conexión
        conexion.close()

        # Escribir los registros en el archivo de texto seleccionado por el usuario
        with open(file_path, 'w') as file:
            for registro in registros:
                file.write(str(registro) + '\n')
        
        print("Base de datos exportada correctamente.")
    else:
        print("Exportación cancelada.")



# Función para mostrar la ayuda
def mostrar_ayuda():
    # Mensaje de ayuda
    mensaje = """Esta es una aplicación realizada por elias  que muestra una maquetación básica de una interfaz gráfica utilizando Tkinter. 
    Puedes utilizar esta aplicación para gestionar una base de datos de materiales, donde puedes consultar, dar de alta, borrar y modificar registros.
    """
    # Mostrar el mensaje de ayuda en una ventana emergente
    messagebox.showinfo("Ayuda", mensaje)

# funcion para que no detone los botones
def accion_boton():
    pass

def alta_registro():
    # Recopilar la información ingresada por el usuario
    material = entry1.get()
    descripcion = entry2.get()
    precio_venta = float(entry3.get())
    precio_costo = float(entry4.get())
    stock = int(entry5.get())
    proveedor = entry6.get()

    # Conectar a la base de datos
    conexion = sqlite3.connect('basededatos.db')
    cursor = conexion.cursor()

    # Insertar el nuevo registro en la tabla materiales
    cursor.execute("INSERT INTO materiales (material, descripcion, precio_venta, precio_costo, stock, proveedor) VALUES (?, ?, ?, ?, ?, ?)",
                (material, descripcion, precio_venta, precio_costo, stock, proveedor))

    # Guardar los cambios y cerrar la conexión
    conexion.commit()
    conexion.close()

    # Mostrar mensaje de éxito
    messagebox.showinfo("Alta de registro", "Registro agregado correctamente.")

    # Limpiar los campos de entrada después de agregar el registro
    entry1.delete(0, END)
    entry2.delete(0, END)
    entry3.delete(0, END)
    entry4.delete(0, END)
    entry5.delete(0, END)
    entry6.delete(0, END)

def consultar_registro():
    # Obtener el texto ingresado en los campos de entrada
    material = entry1.get()
    descripcion = entry2.get()

    # Conectar a la base de datos
    conexion = sqlite3.connect('basededatos.db')
    cursor = conexion.cursor()

    # Realizar la consulta en función del texto ingresado
    if material:
        cursor.execute("SELECT * FROM materiales WHERE material LIKE ?", ('%' + material + '%',))
    elif descripcion:
        cursor.execute("SELECT * FROM materiales WHERE descripcion LIKE ?", ('%' + descripcion + '%',))
    else:
        messagebox.showwarning("Consulta", "Debe ingresar al menos un criterio de búsqueda (Material o Descripción).")
        return

    # Limpiar el treeview antes de agregar nuevos datos
    for record in tree.get_children():
        tree.delete(record)

    # Insertar los resultados de la consulta en el treeview
    for row in cursor.fetchall():
        tree.insert('', 'end', values=row)

    # Cerrar la conexión
    conexion.close()

def borrar_registro():
    # obtengo el material ingresado por el usuario
    material = entry1.get()

    # valido que se haya ingresado un material
    if not material:
        messagebox.showwarning("Borrar registro", "Debe ingresar el material del registro que desea borrar.")
        return

    # conecto la base de datos
    conexion = sqlite3.connect('basededatos.db')
    cursor = conexion.cursor()

    try:
        # intento borrar el registro con el material proporcionado
        cursor.execute("DELETE FROM materiales WHERE material = ?", (material,))
        conexion.commit()
        messagebox.showinfo("Borrar registro", f"Registro con material '{material}' eliminado correctamente.")
    except sqlite3.Error as e:
        # muestro un mensaje en caso de error
        messagebox.showerror("Error", f"No se pudo borrar el registro: {e}")
    finally:
        # cierro la conexión
        conexion.close()

    # borro los campo de entrada después de borrar el registro
    entry1.delete(0, END)

def modificar_registro():
    # Obtener el material ingresado por el usuario
    material = entry1.get()

    # Obtener los valores ingresados por el usuario para los otros campos
    descripcion = entry2.get()
    precio_venta = entry3.get()
    precio_costo = entry4.get()
    stock = entry5.get()
    proveedor = entry6.get()

    # Validar que se haya ingresado un material
    if not material:
        messagebox.showwarning("Modificar registro", "Debe ingresar el material del registro que desea modificar.")
        return

    # Conectar a la base de datos
    conexion = sqlite3.connect('basededatos.db')
    cursor = conexion.cursor()

    try:
        # Verificar si el registro con el material proporcionado existe
        cursor.execute("SELECT * FROM materiales WHERE material = ?", (material,))
        registro = cursor.fetchone()

        if registro:
            # Construir la consulta SQL para actualizar el registro
            sql = "UPDATE materiales SET"
            values = []

            # Agregar los campos que se van a modificar
            if descripcion:
                sql += " descripcion = ?,"
                values.append(descripcion)
            if precio_venta:
                sql += " precio_venta = ?,"
                values.append(float(precio_venta))
            if precio_costo:
                sql += " precio_costo = ?,"
                values.append(float(precio_costo))
            if stock:
                sql += " stock = ?,"
                values.append(float(stock))
            if proveedor:
                sql += " proveedor = ?,"
                values.append(proveedor)

            # Eliminar la última coma y cerrar la consulta
            sql = sql.rstrip(',') + " WHERE material = ?"
            values.append(material)

            # Ejecutar la consulta para actualizar el registro
            cursor.execute(sql, tuple(values))
            conexion.commit()

            messagebox.showinfo("Modificar registro", f"Registro con material '{material}' modificado correctamente.")
        else:
            messagebox.showerror("Error", f"No se encontró ningún registro para el material '{material}'.")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"No se pudo modificar el registro: {e}")
    finally:
        # Cerrar la conexión
        conexion.close()

    # Limpiar los campos de entrada después de modificar el registro
    entry1.delete(0, END)
    entry2.delete(0, END)
    entry3.delete(0, END)
    entry4.delete(0, END)
    entry5.delete(0, END)
    entry6.delete(0, END)



#############################################################################################
# MAQUETACION - arranque de la app contenedor
#############################################################################################
app = Tk()

# Incluyo dentro del loop de la app la funcion de crear base de datos
crear_base_datos()


# Titulo de la ventana
app.title("POS base de materiales")

# seteo del tamaño de la ventana
app.geometry("950x400")

#Seteo el fondo de la app
app.configure(background="white")


# maquetacion del menu

# inserto el menu
menubar = Menu(app)
filemenu = Menu(menubar, tearoff=False) # tearoff=False para que no se pueda arrastrar por fuera del menú

# Submenú de "Exportar base"
filemenu.add_command(label="Exportar base", command=exportar_base)

# Ítem "Salir"
filemenu.add_command(label="Salir", command=app.quit)

# Añadir el menú "Archivo" al menú principal
menubar.add_cascade(label="Archivo", menu=filemenu)

# Menú de ayuda
helpmenu = Menu(menubar, tearoff=False)
helpmenu.add_command(label="Ayuda", command=mostrar_ayuda)

# Añadir el menú "Ayuda" al menú principal
menubar.add_cascade(label="Ayuda", menu=helpmenu)

# Configurar la barra de menú
app.config(menu=menubar)


# maquetacion de los widget

# Crear y colocar los widgets Entry y Label uno por uno
label1 = Label(app, text="MATERIAL", background="white")
label1.place(x=260, y=20)

entry1 = Entry(app)
entry1.place(x=400, y=20)

label2 = Label(app, text="DESCRIPCION", background="white")
label2.place(x=260, y=50)

entry2 = Entry(app)
entry2.place(x=400, y=50)

label3 = Label(app, text="PRECIO DE VENTA", background="white")
label3.place(x=260, y=80)


entry3 = Entry(app, width=10)
entry3.place(x=400, y=80)
entry3.insert(0, "0.0")

label4 = Label(app, text="PRECIO DE COSTO", background="white")
label4.place(x=260, y=110)

entry4 = Entry(app, width=10)
entry4.place(x=400, y=110)
entry4.insert(0, "0.0")

label5 = Label(app, text="STOCK", background="white")
label5.place(x=260, y=140)

entry5 = Entry(app, width=10)
entry5.place(x=400, y=140)
entry5.insert(0, "0.0")

label6 = Label(app, text="PROVEEDOR", background="white")
label6.place(x=260, y=170)

entry6 = Entry(app)
entry6.place(x=400, y=170)

# Botones
# variables con las dimensiones
button_width = 10
button_height = 1

button1 = Button(app, text="Consultar",width=button_width, height=button_height , background="white",command=consultar_registro)
button1.place(x=200, y=200)

button2 = Button(app, text="Alta", width=button_width, height=button_height, background="white" ,command=alta_registro)
button2.place(x=300, y=200)

button3 = Button(app, text="Borrar", width=button_width, height=button_height, background="white" ,command=borrar_registro)
button3.place(x=400, y=200)

button4 = Button(app, text="Modificar", width=button_width, height=button_height, background="white" ,command=modificar_registro)
button4.place(x=500, y=200)

# Treeview
tree = ttk.Treeview(app)
tree["columns"] = ("#0", "1", "2", "3", "4", "5", "6")
tree.column("#0", width=10, minwidth=150)  # Ajusté el ancho de las columnas
tree.column("1", width=150, minwidth=150)
tree.column("2", width=150, minwidth=150)
tree.column("3", width=150, minwidth=150)
tree.column("4", width=150, minwidth=150)
tree.column("5", width=150, minwidth=150)
tree.column("6", width=150, minwidth=150)
tree.heading("#0", text="ID", anchor=W)  # Cambié el texto de las cabeceras
tree.heading("1", text="MATERIAL", anchor=W)
tree.heading("2", text="DESCRIPCION", anchor=W)
tree.heading("3", text="PRECIO DE VENTA", anchor=W)
tree.heading("4", text="PRECIO DE COSTO", anchor=W)
tree.heading("5", text="STOCK", anchor=W)
tree.heading("6", text="PROVEEDOR", anchor=W)
tree.place(relx=0.5, y=480, anchor=S, relwidth=1)

#imprimo la base  de datos en el treeview

imprimir_base_datos_inicio()

# Cargar imagen y agregarla a una etiqueta
image = Image.open("1.JPG")
image = image.resize((200, 150))
photo = ImageTk.PhotoImage(image)
image_label = Label(app, image=photo)
image_label.image = photo  # Esto es importante para evitar que la imagen se elimine por el recolector de basura
image_label.place(x=580, y=25)

# cargar logo en cada label
#label 1
image = Image.open("1.JPG")
image = image.resize((20, 20))
photo = ImageTk.PhotoImage(image)
image_label = Label(app, image=photo)
image_label.image = photo  # Esto es importante para evitar que la imagen se elimine por el recolector de basura
image_label.place(x=220, y=20)

# label 2
image = Image.open("1.JPG")
image = image.resize((20, 20))
photo = ImageTk.PhotoImage(image)
image_label = Label(app, image=photo)
image_label.image = photo  # Esto es importante para evitar que la imagen se elimine por el recolector de basura
image_label.place(x=220, y=50)

# label 3
image = Image.open("1.JPG")
image = image.resize((20, 20))
photo = ImageTk.PhotoImage(image)
image_label = Label(app, image=photo)
image_label.image = photo  # Esto es importante para evitar que la imagen se elimine por el recolector de basura
image_label.place(x=220, y=80)

# label 4
image = Image.open("1.JPG")
image = image.resize((20, 20))
photo = ImageTk.PhotoImage(image)
image_label = Label(app, image=photo)
image_label.image = photo  # Esto es importante para evitar que la imagen se elimine por el recolector de basura
image_label.place(x=220, y=110)

# label 5
image = Image.open("1.JPG")
image = image.resize((20, 20))
photo = ImageTk.PhotoImage(image)
image_label = Label(app, image=photo)
image_label.image = photo  # Esto es importante para evitar que la imagen se elimine por el recolector de basura
image_label.place(x=220, y=140)

# label 6
image = Image.open("1.JPG")
image = image.resize((20, 20))
photo = ImageTk.PhotoImage(image)
image_label = Label(app, image=photo)
image_label.image = photo  # Esto es importante para evitar que la imagen se elimine por el recolector de basura
image_label.place(x=220, y=170)

# cierre de la app
app.mainloop()
