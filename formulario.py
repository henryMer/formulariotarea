# Importa el módulo tkinter y sus submódulos ttk y messagebox
import tkinter as tk
from tkinter import ttk, messagebox
# Importa la clase OrdenesDeServicio desde el archivo conexion_bd
from conexion_bd import OrdenesDeServicio

# Define la clase FormularioOrdenServicio para gestionar el formulario de órdenes de servicio
class FormularioOrdenServicio:
    # Método constructor de la clase
    def __init__(self, root):
        # Define la raíz del formulario y establece el título de la ventana
        self.root = root
        self.root.title("Gestión de Órdenes de Servicio")

        # Crea un frame con padding dentro de la ventana principal
        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack(pady=20, padx=20)

        # Define las etiquetas para los campos del formulario
        self.labels = [
            "Fecha de la orden (YYYY-MM-DD)", "Cliente", "Equipo", "Problema", "Trabajo a realizar",
            "Técnico asignado", "Estado de la orden", "Fecha estimada de fin", "Costo", "Notas adicionales"
        ]
        # Lista para almacenar las entradas de texto
        self.entries = []

        # Crea las etiquetas y entradas de texto para cada campo
        for i, label in enumerate(self.labels):
            lbl = tk.Label(self.frame, text=label)
            lbl.grid(row=i, column=0, sticky="e", padx=10, pady=5)

            # Ajusta el tamaño de las entradas de texto según el campo
            if label == "Fecha de la orden (YYYY-MM-DD)" or label == "Fecha estimada de fin":
                entry = tk.Entry(self.frame, width=30)
            elif label == "Costo":
                entry = tk.Entry(self.frame, width=10)
            else:
                entry = tk.Entry(self.frame, width=50)
            
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            self.entries.append(entry)

        # Crea un frame para los botones
        btn_frame = tk.Frame(self.frame)
        btn_frame.grid(row=len(self.labels), column=0, columnspan=2, pady=10, padx=5)

        # Botón para agregar una orden de servicio
        btn_agregar = tk.Button(btn_frame, text="Agregar", command=self.agregar_orden)
        btn_agregar.pack(side="left", padx=5)

        # Botón para eliminar una orden de servicio seleccionada
        btn_eliminar = tk.Button(btn_frame, text="Eliminar seleccionado", command=self.eliminar_orden)
        btn_eliminar.pack(side="left", padx=5)

        # Botón para modificar una orden de servicio seleccionada
        btn_modificar = tk.Button(btn_frame, text="Modificar seleccionado", command=self.modificar_orden)
        btn_modificar.pack(side="left", padx=5)

        # Crea una tabla para mostrar las órdenes de servicio
        self.tabla = ttk.Treeview(self.frame, columns=("ID", "Fecha Orden", "Cliente", "Equipo", "Problema", "Trabajo Realizar", "Técnico", "Estado", "Fecha Estimada", "Costo", "Notas"), show="headings")
        self.tabla.grid(row=len(self.labels)+1, column=0, columnspan=2, pady=10)

        # Definir encabezados y anchos de columnas
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Fecha Orden", text="Fecha Orden")
        self.tabla.heading("Cliente", text="Cliente")
        self.tabla.heading("Equipo", text="Equipo")
        self.tabla.heading("Problema", text="Problema")
        self.tabla.heading("Trabajo Realizar", text="Trabajo a Realizar")
        self.tabla.heading("Técnico", text="Técnico")
        self.tabla.heading("Estado", text="Estado")
        self.tabla.heading("Fecha Estimada", text="Fecha Estimada")
        self.tabla.heading("Costo", text="Costo")
        self.tabla.heading("Notas", text="Notas")

        # Configurar anchos de columnas
        self.tabla.column("ID", width=50)
        self.tabla.column("Fecha Orden", width=100)
        self.tabla.column("Cliente", width=100)
        self.tabla.column("Equipo", width=100)
        self.tabla.column("Problema", width=150)
        self.tabla.column("Trabajo Realizar", width=150)
        self.tabla.column("Técnico", width=100)
        self.tabla.column("Estado", width=100)
        self.tabla.column("Fecha Estimada", width=100)
        self.tabla.column("Costo", width=100)
        self.tabla.column("Notas", width=150)

        # Instancia la clase OrdenesDeServicio para interactuar con la base de datos
        self.db = OrdenesDeServicio()
        # Carga las órdenes de servicio en la tabla
        self.cargar_ordenes()
        # Vincula el evento de doble clic en la tabla a la función seleccionar_orden
        self.tabla.bind("<Double-1>", self.seleccionar_orden)

    # Método para agregar una orden de servicio a la base de datos
    def agregar_orden(self):
        # Obtiene los datos de las entradas de texto
        datos = [entry.get() for entry in self.entries]

        # Verifica que los campos obligatorios estén llenos
        if any(not dato for dato in datos[:5]):
            messagebox.showerror("Error", "Por favor complete todos los campos obligatorios")
            return

        try:
            # Llama al método para agregar la orden de servicio en la base de datos
            self.db.agregar_orden_de_servicio(*datos)
            messagebox.showinfo("Éxito", "Orden de servicio agregada correctamente")
            # Limpia las entradas de texto y recarga las órdenes de servicio en la tabla
            self.limpiar_campos()
            self.cargar_ordenes()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar la orden de servicio: {e}")

    # Método para cargar las órdenes de servicio en la tabla
    def cargar_ordenes(self):
        # Elimina todos los registros actuales en la tabla
        records = self.tabla.get_children()
        for element in records:
            self.tabla.delete(element)

        try:
            # Consulta las órdenes de servicio en la base de datos
            ordenes = self.db.consultar_ordenes_de_servicio()
            # Inserta cada orden de servicio en la tabla
            for orden in ordenes:
                self.tabla.insert('', 'end', values=(orden[0], orden[1], orden[2], orden[3], orden[4], orden[5], orden[6], orden[7], orden[8], orden[9], orden[10]))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar órdenes de servicio: {e}")

    # Método para seleccionar una orden de servicio de la tabla
    def seleccionar_orden(self, event=None):
        # Obtiene el elemento seleccionado en la tabla
        item = self.tabla.selection()
        if item:
            datos_orden = self.tabla.item(item[0], "values")

            # Rellena las entradas de texto con los datos de la orden seleccionada, saltando el ID
            for i, entry in enumerate(self.entries):
                entry.delete(0, tk.END)
                entry.insert(0, datos_orden[i+1] if datos_orden[i+1] else "")

    # Método para eliminar una orden de servicio de la base de datos
    def eliminar_orden(self):
        # Obtiene el elemento seleccionado en la tabla
        item = self.tabla.selection()
        if item:
            id_orden = self.tabla.item(item[0], "values")[0]

            # Muestra un cuadro de confirmación
            respuesta = messagebox.askyesno("Confirmar Eliminación", "¿Estás seguro de querer eliminar esta orden de servicio?")

            if respuesta:
                try:
                    # Llama al método para eliminar la orden de servicio en la base de datos
                    self.db.eliminar_orden_de_servicio(id_orden)
                    messagebox.showinfo("Éxito", "Orden de servicio eliminada correctamente")
                    self.cargar_ordenes()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo eliminar la orden de servicio: {e}")

    # Método para modificar una orden de servicio en la base de datos
    def modificar_orden(self):
        # Obtiene el elemento seleccionado en la tabla
        item = self.tabla.selection()
        if item:
            id_orden = self.tabla.item(item[0], "values")[0]
            # Obtiene los nuevos datos de las entradas de texto
            nuevos_datos = [entry.get() for entry in self.entries]

            # Verifica que los campos obligatorios estén llenos
            if any(not dato for dato in nuevos_datos[:5]):
                messagebox.showerror("Error", "Por favor complete todos los campos obligatorios")
                return

            try:
                # Llama al método para actualizar la orden de servicio en la base de datos
                self.db.actualizar_orden_de_servicio(id_orden, *nuevos_datos)
                messagebox.showinfo("Éxito", "Orden de servicio modificada correctamente")
                self.cargar_ordenes()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo modificar la orden de servicio: {e}")

    # Método para limpiar todas las entradas de texto
    def limpiar_campos(self):
        for entry in self.entries:
            entry.delete(0, tk.END)

    # Método para iniciar la aplicación tkinter
    def iniciar_aplicacion(self):
        self.root.mainloop()

# Bloque principal para ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()  # Crea la ventana principal
    app = FormularioOrdenServicio(root)  # Instancia la clase FormularioOrdenServicio
    app.iniciar_aplicacion()  # Inicia el loop principal de tkinter

