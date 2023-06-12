import gspread
from oauth2client.service_account import ServiceAccountCredentials


class conectar_sheets():
    def __init__(self):
        #Conectar google sheets
        myscope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
        mycreds = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/sergi/Desktop/Estudio/Practicas Google Python/mimetic-pursuit-350701-5a450a994929.json', myscope)
        myclient = gspread.authorize(mycreds)
        
        #abrir el archivo
        mysheet = myclient.open('Nuke_API_Shared')
        self.worksheet = mysheet.worksheet('Elemental_shots')

    def obtener_celda(self, shot_name):
    
        #encontrar el valor de una celda
        shot_name = shot_name.upper()
        cell = self.worksheet.findall(shot_name)
        
        if len(cell) < 1:
            mensaje = 'Not found'
            estado = 'Not found'
            print('Not found in sheets')
            return {"mensaje": mensaje, "estado": estado}
        else:
            for item in cell:
                print("Found something at R%s, C%s" % (item.row, item.col))
                mensaje = self.worksheet.cell(item.row, 7).value
                estado = self.worksheet.cell(item.row, 9).value
                return {"mensaje": mensaje, "estado": estado}


