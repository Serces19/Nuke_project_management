import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sqlite3

#Crear la DB
conn = sqlite3.connect('C:/Users/sergi/Desktop/Estudio/Practicas Google Python/Elemental.sqlite')
cur = conn.cursor()
cur.execute('DROP TABLE shots')
cur.execute('CREATE TABLE IF NOT EXISTS shots (id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, shot_name TEXT UNIQUE, capitulo TEXT, secuencia TEXT, first_frame INTEGER, last_frame INTEGER)')




#setear variables 
ruta = 'B:/Elemental VFX'
directorio = os.walk(ruta)
extension = '.exr'
lista_shots = dict()
count = 0
lista = []

#funcion que determina cual es el frame de un shot a partir del nombre
def get_frame(frame_name):
    frame_name = frame_name.split('.')
    frame_name = frame_name[0]
    frame_name = frame_name.split('_')
    frame_name = frame_name[-1]
    return(frame_name)


#busca direccion por direccion y va entrando en las subcarpetas
for folder, subfolders, files in directorio:
    shots = list()
    # cuando encuentra files .exr en una misma direccion los guarda en una lista
    for i in files:
        if i.endswith(extension):
            shots.append(i)

    # Si la lista tiene mas de 5 files .exr
    if len(shots) > 5:
        comprobador_folder = folder
        comprobador_folder = comprobador_folder.split('\\')
        comprobador_folder = comprobador_folder[-1]

        #si el folder actual tiene el nombre correcto '3840x2160' busca el primer y ultimo .exr (ordenados por nombre)
        # y los guarda en un diccionario con el nombre del anterior folder en el arbol como key
        if comprobador_folder in ('3840x2160', '2160x3840'):
            folder = folder.split('\\')
            folder = folder[-2]
            #Si el folder tiene varios plates (A B C) quita el _A del nombre del folder
            if not folder.endswith('VFX'):
                folder = folder.split('_')
                folder = folder[:-1]
                folder = '_'.join(folder)

            #Primer elemento de la lista
            first = shots[0]
            #Ultimo elemento de la lista 
            last = shots[-1]

            #llama la funcion get_frame devuelve solo el frame
            first = get_frame(first)
            last = get_frame(last)

            #separa capitulo
            capitulo = folder.split('_')
            capitulo = capitulo[:2]
            capitulo = '_'.join(capitulo)

            #separa secuencia
            secuence = folder.split('_')
            secuence = secuence[:3]
            secuence = '_'.join(secuence)
            
            #Si el elemento no es repetido lo guarda como una nueva fila en la DB
            if folder not in lista:
                count += 1
                cur.execute('''INSERT OR IGNORE INTO shots (shot_name, capitulo, secuencia, first_frame, last_frame) 
                VALUES (?, ?, ?, ?, ?)''', (folder, capitulo, secuence, first, last))

conn.commit()
print('numero total de shots asignados:', count)



