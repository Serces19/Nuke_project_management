import sqlite3
from sqlite3 import Error
import getpass
import datetime
import nuke

class manager_db():
    def __init__(self):

        self.TIMER = 30
        self.DB_path = 'C:/Users/sergi/.nuke/Manager_panel/db/Manager.db'
        self.Table_name = getpass.getuser()  # Obtener nombre del usuario actual
        self.fecha_actual = datetime.date.today() # Obtener fecha actual

        # Obtener ejecutable de nuke    
        self.ruta_ejecutable = nuke.env['ExecutablePath']
        self.ruta_ejecutable = '"' + self.ruta_ejecutable + '"'
        
        # conectar con la base de datos 
        self.conn = sqlite3.connect(self.DB_path)
        self.cur = self.conn.cursor()

    ##################################################################
    ### Metodos para guardar shots y manejar el registro de us de Nuke
    def create_table(self):
        self.cur.execute(f'''CREATE TABLE IF NOT EXISTS {self.Table_name} 
                        (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
                        shot TEXT,
                        user TEXT,
                        fecha TEXT, 
                        tiempo INTEGER)
                        ''') 

    def add_time(self, shot_name):
        try:
            self.cur.execute(f'''SELECT tiempo
                            FROM {self.Table_name}
                            WHERE shot = ?
                            AND user = ?
                            AND fecha = ? ''' ,(shot_name, self.Table_name, self.fecha_actual))
            row = self.cur.fetchone()
            if row is None:
                self.cur.execute(f'''INSERT INTO {self.Table_name} (shot, user, fecha, tiempo) 
                                VALUES (?, ?, ?, ?) ''',(shot_name, self.Table_name, self.fecha_actual, self.TIMER))
            else:
                self.cur.execute(f'''UPDATE {self.Table_name} 
                                SET tiempo = tiempo + ? 
                                WHERE shot = ?
                                AND user = ?
                                AND fecha = ? ''',(self.TIMER, shot_name, self.Table_name, self.fecha_actual))
            # Gaurdar y cerrar
            self.conn.commit()
        
        finally:
            self.cur.close()
            
        print('Saving Time')


    def get_data(self, shot_name):
        self.fecha_actual =  str(self.fecha_actual)
        self.fecha_actual = '"' + self.fecha_actual + '"'
        
        try:
            # Obtener el total de todos los shots trabajados hoy
            self.cur.execute(f'''SELECT SUM (tiempo) AS suma_tiempo
                                FROM {self.Table_name}
                                WHERE fecha = {self.fecha_actual} ''')

            total_hoy = self.cur.fetchone()
            total_hoy = total_hoy[0]
            print(total_hoy)

            # Obtener el total de tiemp trabajado en el shot actual
            shot_name = '"' + shot_name + '"'
            self.cur.execute(f'''SELECT SUM (tiempo) AS suma_tiempo
                                FROM {self.Table_name}
                                WHERE shot = {shot_name} ''')
            total_shot = self.cur.fetchone()
            total_shot = total_shot[0]
            
            #convertit en formato horas, minutos y segundos
            total_hoy = self.convert_time(total_hoy)
            total_shot = self.convert_time(total_shot)


            return {"total_hoy": total_hoy, "total_shot": total_shot}
        
        finally:
            self.cur.close()


    def convert_time(self, number):
            horas = number // 3600
            minutos = (number % 3600) // 60
            segundos = number % 60
            number = "{:02d}:{:02d}:{:02d}".format(horas, minutos, segundos)
            return number
            

##############################################################
## Metodos para cargar shots al render

    def escribir_datos(self):
        # Obtener path del script actual 
        shot = nuke.tcl('value root.name')
        if shot is not None:
            pass
            # shot = '"' + shot + '"'
        else:
            print('Error no se ha cargado un shot')
            
        # # Obtener comando para renderizar
        # self.data = self.ruta_ejecutable + " -ti -V2 " + shot + " < execute_temp.py"

        # Crear tabla si no existe
        self.cur.execute('''
                         CREATE TABLE IF NOT EXISTS to_render 
                         ( comando TEXT UNIQUE NOT NULL)
        ''') 
        
        # Insertar datos en la tabla
        self.conn.execute("INSERT OR IGNORE INTO to_render (comando) VALUES (?)", (shot, ))
        self.conn.commit()
        self.conn.close()


    def leer_datos(self):
        # Crear tabla si no existe
        self.cur.execute('''
                         CREATE TABLE IF NOT EXISTS to_render 
                         ( comando TEXT UNIQUE NOT NULL)
        ''') 
        try:
            # Ejecuta una consulta para obtener todos los registros de la tabla
            self.cur.execute("SELECT * FROM to_render")
            records = self.cur.fetchall()
            return records
        
        finally:
            
            # Cierra la conexión a la base de datos
            self.conn.close()


    def borrar_fila_seleccionada(self, nombre_fila):

        # Eliminar la fila seleccionada en la tabla en SQLite
        self.cur.execute("DELETE FROM to_render WHERE comando = ?", (nombre_fila,))
        self.conn.commit()
