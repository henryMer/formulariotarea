# Importa el módulo mysql.connector y el objeto Error del mismo módulo
import mysql.connector
from mysql.connector import Error

# Define la clase OrdenesDeServicio que gestionará las operaciones con la base de datos
class OrdenesDeServicio:
    # Método constructor de la clase
    def __init__(self):
        try:
            # Intenta establecer una conexión con la base de datos MySQL
            self.conn = mysql.connector.connect(
                host="localhost",     # Dirección del servidor de la base de datos
                user="root",          # Usuario de la base de datos
                password="root",      # Contraseña del usuario de la base de datos
                database="servicio_db" # Nombre de la base de datos
            )
            # Verifica si la conexión fue exitosa
            if self.conn.is_connected():
                print("Conexión exitosa a la base de datos")
            # Crea un cursor para ejecutar consultas en la base de datos
            self.cursor = self.conn.cursor()
        except Error as e:
            # Captura y muestra cualquier error que ocurra al intentar conectarse
            print(f"Error al conectar a la base de datos: {e}")

    # Método para agregar una nueva orden de servicio a la base de datos
    def agregar_orden_de_servicio(self, fecha_orden, cliente, equipo, problema, trabajo_a_realizar, tecnico_asignado, estado_orden, fecha_estimacion_fin, costo, notas_adicionales):
        try:
            # Define la consulta SQL para insertar una nueva orden de servicio
            sql = """
            INSERT INTO ordenes_servicio (
                fecha_orden, cliente, equipo, problema, trabajo_a_realizar, tecnico_asignado, estado_orden, fecha_estimacion_fin, costo, notas_adicionales
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            # Define los valores que se insertarán en la consulta
            values = (fecha_orden, cliente, equipo, problema, trabajo_a_realizar, tecnico_asignado, estado_orden, fecha_estimacion_fin, costo, notas_adicionales)
            # Ejecuta la consulta SQL con los valores proporcionados
            self.cursor.execute(sql, values)
            # Confirma la transacción
            self.conn.commit()
            print("Orden de servicio agregada exitosamente")
        except Error as e:
            # Captura y muestra cualquier error que ocurra al intentar agregar la orden de servicio
            print(f"Error al agregar la orden de servicio: {e}")

    # Método para consultar todas las órdenes de servicio de la base de datos
    def consultar_ordenes_de_servicio(self):
        try:
            # Ejecuta la consulta SQL para seleccionar todas las órdenes de servicio
            self.cursor.execute("SELECT * FROM ordenes_servicio")
            # Recupera todos los resultados de la consulta
            resultados = self.cursor.fetchall()
            return resultados
        except Error as e:
            # Captura y muestra cualquier error que ocurra al intentar consultar las órdenes de servicio
            print(f"Error al consultar las órdenes de servicio: {e}")

    # Método para eliminar una orden de servicio de la base de datos por su ID
    def eliminar_orden_de_servicio(self, id_orden):
        try:
            # Define la consulta SQL para eliminar una orden de servicio por su ID
            sql = "DELETE FROM ordenes_servicio WHERE id = %s"
            # Define el valor del ID que se usará en la consulta
            values = (id_orden,)
            # Ejecuta la consulta SQL con el ID proporcionado
            self.cursor.execute(sql, values)
            # Confirma la transacción
            self.conn.commit()
            print(f"Orden de servicio con ID {id_orden} eliminada correctamente")
        except Error as e:
            # Captura y muestra cualquier error que ocurra al intentar eliminar la orden de servicio
            print(f"Error al eliminar la orden de servicio: {e}")

    # Método para actualizar una orden de servicio existente en la base de datos
    def actualizar_orden_de_servicio(self, id_orden, fecha_orden, cliente, equipo, problema, trabajo_a_realizar, tecnico_asignado, estado_orden, fecha_estimacion_fin, costo, notas_adicionales):
        try:
            # Define la consulta SQL para actualizar una orden de servicio por su ID
            sql = """
            UPDATE ordenes_servicio
            SET fecha_orden = %s, cliente = %s, equipo = %s, problema = %s, trabajo_a_realizar = %s,
                tecnico_asignado = %s, estado_orden = %s, fecha_estimacion_fin = %s, costo = %s, notas_adicionales = %s
            WHERE id = %s
            """
            # Define los valores que se actualizarán en la consulta
            values = (fecha_orden, cliente, equipo, problema, trabajo_a_realizar, tecnico_asignado, estado_orden, fecha_estimacion_fin, costo, notas_adicionales, id_orden)
            # Ejecuta la consulta SQL con los valores proporcionados
            self.cursor.execute(sql, values)
            # Confirma la transacción
            self.conn.commit()
            print(f"Orden de servicio con ID {id_orden} actualizada correctamente")
        except Error as e:
            # Captura y muestra cualquier error que ocurra al intentar actualizar la orden de servicio
            print(f"Error al actualizar la orden de servicio: {e}")

    # Método destructor para cerrar el cursor y la conexión a la base de datos
    def __del__(self):
        # Cierra el cursor si está abierto
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        # Cierra la conexión si está abierta y conectada
        if hasattr(self, 'conn') and self.conn.is_connected():
            self.conn.close()

