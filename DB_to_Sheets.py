import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sqlite3
import time
count = 0

#Conectar DB
conn = sqlite3.connect('C:/Users/sergi/Desktop/Estudio/Practicas Google Python/Elemental.sqlite')
cur = conn.cursor()

#Conectar google sheets
myscope = ['https://spreadsheets.google.com/feeds',
           'https://www.googleapis.com/auth/drive']

mycreds = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/sergi/Desktop/Estudio/Practicas Google Python/mimetic-pursuit-350701-5a450a994929.json', myscope)
myclient = gspread.authorize(mycreds)

#abrir el archivo
mysheet = myclient.open('Nuke_API_Shared')
worksheet = mysheet.worksheet('Elemental_shots')



#agregar los datos a la hoja

cur.execute('SELECT capitulo FROM shots')
capitulo = cur.fetchall()

cur.execute('SELECT secuencia FROM shots')
secuence = cur.fetchall()

cur.execute('SELECT shot_name FROM shots')
shot_name = cur.fetchall()

cur.execute('SELECT first_frame FROM shots')
first = cur.fetchall()

cur.execute('SELECT last_frame FROM shots')
last = cur.fetchall()

cur.execute('SELECT id FROM shots')
id = cur.fetchall()

for a, b, c, d, e, f in zip(id, shot_name, capitulo, secuence, first, last):
  worksheet.append_row([a[0], b[0], c[0], d[0], e[0], f[0]])
  time.sleep(1)
