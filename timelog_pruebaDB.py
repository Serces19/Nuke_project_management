import os
import threading
import getpass
import datetime
import nuke
import time
import sqlite3


TIMER = 30
IDLE_TIME = 160
tiempo_inicial = time.time()
DB_name = "Nuke_Logs.db"
DB_path = 'C:/Users/sergi/Desktop/logs/Nuke_Logs.db'
Table_name = getpass.getuser()  # Obtener nombre del usuario actual
fecha_actual = datetime.date.today()
rendering = False


class Timelog():

    def __init__(self):
        nuke.addUpdateUI(self.reiniciar_timer)
        nuke.addRenderProgress(self.comprobar_render)
        

    def comprobar_render(self):
        global rendering
        rendering = True


    def start_thread(self):

        Timelog.thread = threading.Timer(TIMER, self.validate_path)
        Timelog.thread.setDaemon(True)
        Timelog.thread.start()


    def validate_path(self):
        self.script_path = nuke.root()['name'].value()
        global rendering
        rendering = False
        nuke.renderProgress()
        if not os.path.exists(self.script_path):
            print('Invalid path. Abort!')
            return # termina todo hasta que se abra otro script      
        else:
            print('Script valido')
            if rendering is True:
                print('renderizando')
                self.start_thread()
                return
            else:
                self.write_DB()


    def write_DB(self): 
        global fecha_actual
        fecha_actual = datetime.date.today()
        self.shot = nuke.tcl('regsub -all {_v[0-9]+} [file rootname [file tail [value root.name]]] ""')
        if self.contador() > IDLE_TIME: 
            print('Fuera de tiempo')
            self.start_thread()
            return  # Aqui se detiene el metodo y no se guarda nada en la DB
        else:
            print('Sigue trabajando')
            try:
                # Setear el DB y crear la tabla si no existe
                conn = sqlite3.connect(DB_path)
                cur = conn.cursor()
                cur.execute(f'''CREATE TABLE IF NOT EXISTS {Table_name} 
                            (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
                            shot TEXT,
                            user TEXT,
                            fecha TEXT, 
                            tiempo INTEGER)
                            ''') 


                #Seleccionar el row tiempo del script actual e iniciar el tiempo o aumentarlo si ya existe
                cur.execute(f'''SELECT tiempo
                                FROM {Table_name}
                                WHERE shot = ?
                                AND user = ?
                                AND fecha = ? ''' ,(self.shot, Table_name, fecha_actual))
                row = cur.fetchone()
                if row is None:
                    cur.execute(f'''INSERT INTO {Table_name} (shot, user, fecha, tiempo) 
                                    VALUES (?, ?, ?, ?)''',(self.shot, Table_name, fecha_actual, TIMER))
                else:
                    cur.execute(f'''UPDATE {Table_name} 
                                    SET tiempo = tiempo + ? 
                                    WHERE shot = ?
                                    AND user = ?
                                    AND fecha = ?''',(TIMER, self.shot, Table_name, fecha_actual))
                # Gaurdar y cerrar
                conn.commit()
                cur.close()
                self.start_thread()
                print('guardando tiempo')
                
            finally:
                cur.close()



    def contador(self):
        global tiempo_inicial #usar global para que la variable sea la misma en todas las funciones
        tiempo_actual = time.time()
        tiempo_lapso = tiempo_actual - tiempo_inicial
        print("Tiempo de inactividad:", tiempo_lapso)
        return(tiempo_lapso)

        

    def reiniciar_timer(self):
        global tiempo_inicial #usar global para que la variable sea la misma en todas las funciones
        tiempo_inicial = time.time()

        
#nuke.addAfterRender(function)
#nuke.addBeforeRender(function)

            