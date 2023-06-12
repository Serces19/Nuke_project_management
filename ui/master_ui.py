import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2 import *
from PySide2.QtGui import QColor, QPalette
from PySide2.QtCore import Qt


################################################################################
# Interfaz
################################################################################

class Manager_UI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
    
    def setupUi(self):
        #Establecer la ventana principal
        self.setWindowTitle("Nuke render")
        self.setGeometry(100, 100, 1000, 1000)  # Definir posición y tamaño de la ventana
        self.setStyleSheet(u"""
                            background-color: rgb(20, 25, 35);\n
                            font: 9pt \"Verdana\";\n
                            color: rgb(180, 180, 180);
                            border-radius: 5px; 
                            padding: 15px; 
        """)        
        self.center_window()

        #------------------------------------------Crear el lienzo-------------------------------------------
        # Crear el objeto QTabWidget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""

                            QTabWidget::pane {
                            border: none;
                            margin: -1px;
                            }

                            QTabBar::tab {
                                    background-color: rgba(255, 255, 255, 10);
                                    padding: 15px;
                                    border: 1px solid rgba(255, 255, 255, 10);
                            }

                            QTabBar::tab:selected {
                                    background-color: rgba(255, 255, 255, 50);
                            }
        """)

        self.setCentralWidget(self.tab_widget)

        # Crear las TABs
        #TAB1
        self.tab1 = QWidget()
        self.tab1.setStyleSheet(""" 
                            QWidget { 
                                    background-color: rgba(255, 255, 255, 3);
                            }
        """)

        self.tab2 = QWidget()
        self.tab2.setStyleSheet(""" 
                            QWidget { 
                                    background-color: rgba(255, 255, 255, 3);
                            }
        """)

        #TAB2
        self.tab3 = QWidget()
        self.tab3.setStyleSheet(""" 
                            QWidget { 
                                    background-color: rgba(255, 255, 255, 3);
                                    padding: 25px;
                            }
        """)

        #TAB3
        # Agregar las pestañas al QTabWidget
        self.tab_widget.addTab(self.tab1, "Overview")
        self.tab_widget.addTab(self.tab2, "Revisions")
        self.tab_widget.addTab(self.tab3, "Submit work")


        ################################################################################
        ## TAB 1
        ################################################################################

        # Crear layout del TAB 1
        layout_tab1 = QVBoxLayout()

        # Crear las divisiones principales (horizontal)
        group_box1 = QGroupBox("Status")
        group_box1.setStyleSheet("QGroupBox::title { font-style: italic; color: grey; }")
        group_box2 = QGroupBox("Description")
        group_box2.setStyleSheet("QGroupBox::title { font-style: italic; color: grey; }")

        
        # Crear la subidivisiones
        grid1_1 = QGridLayout()
        group_box2_layout = QVBoxLayout()

        #Crear las sub subdiviones
        hbox1 = QHBoxLayout()
        hbox1.setSpacing(0)

        hbox2 = QHBoxLayout()
        hbox2.setSpacing(0)

        hbox3 = QHBoxLayout()
        hbox3.setSpacing(0)

        hbox4 = QHBoxLayout()
        hbox4.setSpacing(0)

        # Crear un espacio
        spacer = QSpacerItem(0, 25, QSizePolicy.Expanding, QSizePolicy.Minimum)


        #---------------------------------------------Agregar------------------------------------------------
        # Agregar las subdivisiones del TAB 1
        group_box1.setLayout(grid1_1)
        group_box2.setLayout(group_box2_layout)
                
        # Agregar las divisiones principales al layout del TAB 1
        layout_tab1.addWidget(group_box1)
        layout_tab1.addItem(spacer)
        layout_tab1.addWidget(group_box2)

        #Establecer el layout del TAB 1
        self.tab1.setLayout(layout_tab1)

        grid1_1.addLayout(hbox1, 0, 0)
        grid1_1.addLayout(hbox2, 1, 0)
        grid1_1.addLayout(hbox3, 1, 1)
        grid1_1.addLayout(hbox4, 2, 1)

        #---------------------------------------Crear los widgets, botones, etc-------------------------------
        
        label_shot_name = QLabel("Shot name:")
        label_shot_name.setStyleSheet("QLabel { font-weight: bold; }")
        label_shot_name.setAlignment(Qt.AlignRight)
        hbox1.addWidget(label_shot_name)

        self.shot_name = QLabel()
        self.shot_name.setAlignment(Qt.AlignLeft)
        hbox1.addWidget(self.shot_name) 

        self.status = QLabel("Initializing")
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setStyleSheet("QLabel { font-style: italic; background-color: rgb(35, 40, 50)}")
        grid1_1.addWidget(self.status, 0, 1)  # Agregar el widget en la fila 0, columna 1

        label_estado = QLabel("Progress:")
        label_estado.setStyleSheet("QLabel { font-weight: bold; }")
        label_estado.setAlignment(Qt.AlignRight)
        hbox2.addWidget(label_estado)

        self.estado = QLabel()
        self.estado.setAlignment(Qt.AlignLeft)
        hbox2.addWidget(self.estado)


        label_tiempo_hoy = QLabel("Today work:")
        label_tiempo_hoy.setStyleSheet("QLabel { font-weight: bold; }")
        label_tiempo_hoy.setAlignment(Qt.AlignRight)      
        hbox3.addWidget(label_tiempo_hoy)  

        self.tiempo_hoy = QLabel()
        self.tiempo_hoy.setAlignment(Qt.AlignLeft)      
        hbox3.addWidget(self.tiempo_hoy)

        label_tiempo_shot = QLabel("Actual shot work:")
        label_tiempo_shot.setStyleSheet("QLabel { font-weight: bold; }")
        label_tiempo_shot.setAlignment(Qt.AlignRight)  
        hbox4.addWidget(label_tiempo_shot)

        self.tiempo_shot = QLabel()
        self.tiempo_shot.setAlignment(Qt.AlignLeft)
        hbox4.addWidget(self.tiempo_shot)

        # self.refresh = QPushButton("Refresh")
        # self.refresh.setStyleSheet("QPushButton:hover { background-color: rgb(40, 45, 60); }"
        #                 "QPushButton:pressed { background-color:rgb(50, 55, 70); }")
        # grid1_1.addWidget(self.refresh, 2, 1)

        self.comentarios = QTextBrowser()
        group_box2_layout.addWidget(self.comentarios)

        by = QLabel("By Sergio Cespedes")
        by.setStyleSheet("QLabel { font-style: italic; color: rgba( 120, 120, 120, 100)}")
        layout_tab1.addWidget(by)


        #################################################################################
        ### TAB 3
        #################################################################################

        # Crear los layout del TAB 3
        layout_tab3 = QVBoxLayout()

        # Crear las divisiones principales (horizontal)
        subdivision3_1 = QHBoxLayout()
        subdivision3_2 = QHBoxLayout()
        subdivision3_3 = QHBoxLayout()

        # Crear la subidivisiones
        grid3_1 = QGridLayout()

        # Crear un espacio
        spacer = QSpacerItem(0, 25, QSizePolicy.Expanding, QSizePolicy.Minimum)


        #---------------------------------------------Agregar------------------------------------------------            
        # Agregar las subdivisiones a las divisiones del TAB 3
        subdivision3_1.addLayout(grid3_1)

        # Agregar las divisiones principales al layout del TAB 3
        layout_tab3.addLayout(subdivision3_1)
        layout_tab3.addLayout(subdivision3_2)
        layout_tab3.addItem(spacer)
        layout_tab3.addLayout(subdivision3_3)

        #Establecer el layout del TAB 3
        self.tab3.setLayout(layout_tab3)

        # Label de la tabla de la cola de render
        self.informacion = QLabel("This is the render queue")
        grid3_1.addWidget(self.informacion, 1, 0)  # Agregar el widget en la fila 1, columna 0

        # Crea una tabla para visualizar la base de datos
        self.table = QTableWidget(self)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(1)
        self.table.setSelectionMode(QListWidget.SingleSelection)
        self.table.setItemDelegate(AlternatingColorDelegate())   
        subdivision3_2.addWidget(self.table)

        # Boton para agregar el script actual a la cola de render
        self.agregar_shot_cola = QPushButton("Add this script to queue")
        self.agregar_shot_cola.setStyleSheet("QPushButton { background-color: rgb(30, 120, 90); }"
                     "QPushButton:hover { background-color: rgb(40, 150, 100); }"
                     "QPushButton:pressed { background-color:rgb(10, 150, 120); }")
        subdivision3_3.addWidget(self.agregar_shot_cola)

        # Crea un botón para eliminar fila de la tabla
        self.remove_button = QPushButton("Remove seleccion ", self)
        self.remove_button.setStyleSheet("QPushButton { background-color: rgb(70, 80, 90); }"
                                        "QPushButton:hover { background-color: rgb(100, 60, 60); }"
                                        "QPushButton:pressed { background-color:rgb(120, 60, 60); }")
        subdivision3_3.addWidget(self.remove_button)



        ################################################################################
        ## FUNCIONES
        ################################################################################

    def center_window(self):
        # Obtener el tamaño de la pantalla y el tamaño de la ventana
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        window_geometry = self.frameGeometry()

        # Calcular la posición central de la ventana
        center_x = screen_geometry.center().x() - window_geometry.width() / 2
        center_y = screen_geometry.center().y() - window_geometry.height() / 2

        # Establecer la posición de la ventana
        self.move(center_x, center_y)


#############################################################################
class AlternatingColorDelegate(QStyledItemDelegate):

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        if index.row() % 2 == 0:
            option.backgroundBrush = QColor(20, 30, 40)  # Color para filas pares
        else:
            option.backgroundBrush = QColor(25, 35, 45)  # Color para filas impares


################################################################################
                                # ejecutar
################################################################################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Manager_UI()
    window.show()
    sys.exit(app.exec_())






