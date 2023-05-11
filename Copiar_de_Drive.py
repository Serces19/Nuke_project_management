import csv
import os
import shutil
import os
from tqdm import tqdm



def copytree2(src, dst, symlinks=False, ignore=None):
    # Crear la carpeta de destino si no existe
    os.makedirs(dst, exist_ok=True)

    # Copiar archivos y directorios
    for item in tqdm(os.listdir(src), desc="Copying " + src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        # Si es un enlace simbólico, copiarlo directamente
        if os.path.islink(src_path):
            linkto = os.readlink(src_path)
            os.symlink(linkto, dst_path)

        # Si es un archivo, copiarlo
        elif os.path.isfile(src_path):
            shutil.copy2(src_path, dst_path)

        # Si es un directorio, copiarlo recursivamente
        elif os.path.isdir(src_path):
            copytree2(src_path, dst_path, symlinks, ignore)



with open('C:/Users/sergi/Desktop/Estudio/Practicas Google Python/PTRS_108_VFX_SHOTLIST - EP. 101.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        if row[41] == 'Sergio':
            shot = row[8]

            secuencia = shot.split('_')
            secuencia = secuencia[:3]
            secuencia = '_'.join(secuencia)

            capitulo = shot.split('_')
            capitulo = capitulo[:2]
            capitulo = '_'.join(capitulo)

            shot = shot.split('_')
            shot = shot[:-2]
            shot = '_'.join(shot)

            ruta_origen = f'J:/Shared drives/01_PTRS/{capitulo}/04_POST/{secuencia}/{shot}/'
            ruta_destino = f'B:/Elemental VFX/{capitulo}/{secuencia}/{shot}/'

            print(ruta_destino)
            print(ruta_origen)

            #Copiar todos los archivos de una carpeta a otra
            copytree2(ruta_origen, ruta_destino)
            print('Hecho')









