import nuke
from nukescripts import panels
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtWidgets import QWidget
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtWidgets import QApplication, QMainWindow, QLabel
from PySide2.QtCore import QTimer, Qt, QTime
from Manager_panel.ui.master_ui import Manager_UI
from Manager_panel.sheets.read_sheets import conectar_sheets
from Manager_panel.db.DB_Manager import manager_db
from Manager_panel.timelog_DB import Timelog


class Manager(Manager_UI):
    def __init__(self):
        super().__init__()
        self.setupUi()

        # Agregar funciones a los botones del TAB 3
        self.remove_button.clicked.connect(self.remove_item)
        self.agregar_shot_cola.clicked.connect(self.load_to_queue)

        #Funciones para actualizar la interfaz
        self.update_viewer_queue()
        self.temporizador()

    def temporizador(self):
            # Inicia un bucle 
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_data)
            self.timer.start(15000)


    #################################################################################
                                ## Definir las funciones
    ##################################################################################

    #####################
    ## DB

    def update_viewer_queue(self):
        # Conectar con DB para cargar datos de la tabla
        manage_db = manager_db()
        records = manage_db.leer_datos()
        
        # Configura el número de filas y columnas en la tabla
        row_count = len(records)
        column_count = len(records[0]) if row_count > 0 else 0
        self.table.setRowCount(row_count)
        self.table.setColumnCount(column_count)

        # Inserta los registros en la tabla
        for row, record in enumerate(records):
            for column, value in enumerate(record):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row, column, item)
        
        # Adaptar size de la tabla segun los conteidos
        self.table.resizeColumnsToContents()
        
    def load_to_queue(self):
        # Conectar con DB
        manage_db = manager_db()
        manage_db.escribir_datos()
        self.update_viewer_queue()

    def add_item(self):
        new_item_text = "Nuevo elemento"
        self.table.addItem(new_item_text)

    def remove_item(self):
        # Obtener la fila seleccionada
        fila_seleccionada = self.table.currentRow()
        nombre_fila = self.table.item(fila_seleccionada, 0).text()

        #Crear la instancia de la clase y ejecutar el metodo borrar_fila_seleccionada
        manage_db = manager_db()
        manage_db.borrar_fila_seleccionada(nombre_fila)
        
        # Actualizar la interfaz
        self.update_viewer_queue()


    #####################
    ## Interfaz

    def update_data(self):
        self.update_viewer_queue()
        
        # Obtener data y ejecutar shot
        self.shot = nuke.tcl('regsub -all {_v[0-9]+} [file rootname [file tail [value root.name]]] ""')
        self.update_shot_name(self.shot)
        
        # Obtener data y ejecutar status
        from Manager_panel.timelog_DB import status
        self.update_status(status)
        print('el status es:', status)

        # Obtener data y ejecutar mensaje de descripcion y estado
        manage_sheets = conectar_sheets()
        resultado = manage_sheets.obtener_celda(self.shot)
        estado = resultado["estado"]
        mensaje = resultado["mensaje"]
        self.update_mensaje(mensaje)
        self.update_estado(estado)

        # Obtener data de la base de datos
        manage_db = manager_db()
        resultado = manage_db.get_data(self.shot)
        total_hoy = resultado["total_hoy"]
        total_shot = resultado["total_shot"]
        self.update_todays_work(total_hoy, total_shot)

        # Actualizar
        print('data updated')
        self.updateValue()

    def update_status(self, status):
        self.status.setText(status)
        if status == 'Idle':
            color = 'red'
        else:
            color = 'rgb(30, 120, 90)'
        self.status.setStyleSheet(f"color: {color}")

    def update_mensaje(self, mensaje):
        self.comentarios.setText(mensaje)

    def update_shot_name(self, shot_name):
        self.shot_name.setText(shot_name)

    def update_estado(self, estado):
        self.estado.setText(estado)

    def update_shot_time(self):
        pass

    def update_todays_work(self, total_hoy, total_shot):
        self.tiempo_shot.setText(f'{total_shot} hrs.')
        self.tiempo_hoy.setText(f'{total_hoy} hrs.')

    def updateValue(self):
        self.update()

###############################################################################
                    ## Implementation como panel un nuke #
###############################################################################

def addManagerPane():
    panels.registerWidgetAsPanel('nuke.Manager', 'Manager', 'com.SergioCes.Manager', True)

nuke.Manager = Manager
addManagerPane()


