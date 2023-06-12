import os
import datetime
import nuke
import time
import threading
from Manager_panel.db.DB_Manager import manager_db

tiempo_inicial = time.time()
status = 'Starting'
##########################################################################
                            ## Iniciar Clase principal
##########################################################################

class Timelog():
    def __init__(self):
        self.TIMER = 30
        self.IDLE_TIME = 160
        self.rendering = False
        nuke.addUpdateUI(self.reiniciar_timer)
        nuke.addRenderProgress(self.comprobar_render)
        global tiempo_inicial
        tiempo_inicial = time.time()

    def start_thread(self):
        Timelog.thread = threading.Timer(self.TIMER, self.validate_path)
        Timelog.thread.setDaemon(True)
        Timelog.thread.start()

    def comprobar_render(self):
        self.rendering = True
     
    def validate_path(self):
        self.shot = nuke.tcl('regsub -all {_v[0-9]+} [file rootname [file tail [value root.name]]] ""')
        self.script_path = nuke.root()['name'].value()
        self.rendering = False
        nuke.renderProgress()

        # Si el script no es valido, se interrumpe el ciclo
        if os.path.exists(self.script_path):
            print('Valid script')
            # Se comprueba que no se este renderizando

            if self.rendering is False:
                # Se ejecuta el metodo WriteDB que guarda el tiempo en la DB
                self.write_DB()

            else:
                print('Render in progress')
                self.start_thread() 
                return 

        # Si el script valido, se comprueba que no se este renderizando
        # Y se ejecuta el metodo WriteDB que guarda el tiempo en la DB
        else:
            print('Invalid script')
            return  

    def write_DB(self):
        global status 
        self.fecha_actual = datetime.date.today()
        if self.contador() > self.IDLE_TIME:
            status = 'Idle'
            self.start_thread() 
            return 
        
        else:
            status = 'Working on'

        manage_db = manager_db()
        manage_db.create_table()
        manage_db.add_time(self.shot)
        self.start_thread() 

    def contador(self):
        global tiempo_inicial
        global status
        tiempo_actual = time.time()
        tiempo_lapso = tiempo_actual - tiempo_inicial
        print("Inactivity time:", tiempo_lapso, status)
        return(tiempo_lapso)

    def reiniciar_timer(self):
        global tiempo_inicial
        tiempo_inicial = time.time()
