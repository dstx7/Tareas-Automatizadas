import os
import shutil
import getpass
from tkinter import Tk, filedialog
from datetime import datetime

usuario = getpass.getuser()

# Ruta de los archivos a ordenar 

ventana = Tk()
ventana.withdraw()

ruta = filedialog.askdirectory(title = "Seleccione la carpetiña")

# carpetas creadas

# tipo = ["Imagenes", "PDF" , "Video", "Word", "texto"]

extensiones = {
    ".jpg":"Imagenes",
    ".png":"Imagenes",
    ".pdf":"pdefes",
    ".mp4":"videos",
    ".docx":"words",
    ".txt":"textos"
} 


for carpeta in set(extensiones.values()):
    ruta_carpeta = os.path.join(ruta,carpeta)

    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)
        
for archivo in os.listdir(ruta):
    
   ruta_archivo = os.path.join(ruta,archivo)

   # Ignorar el archivo de log
   if archivo == "log_movimientos.txt":
        continue
   
   if os.path.isfile(ruta_archivo):
       nombre,ext = os.path.splitext(archivo)
       ext = ext.lower()

       if ext in extensiones:
           # destino = os.path.join(ruta,extensiones[ext],archivo)

           #get the date from the last update
           
           fecha_mod = datetime.fromtimestamp(os.path.getmtime(ruta_archivo))
           subcarpeta_fecha = fecha_mod.strftime("%Y-%m") #formatea año mes

           #create a subfolder if it doesn't exist.

           carpeta_tipo = os.path.join(ruta,extensiones[ext])
           carpeta_fecha = os.path.join(carpeta_tipo, subcarpeta_fecha)

           if not os.path.exists(carpeta_fecha):
               os.makedirs(carpeta_fecha)

           destino = os.path.join(carpeta_fecha,archivo)

           shutil.move(ruta_archivo, destino)

           with open(os.path.join(ruta,"log_movimientos.txt"),"a",encoding="utf-8") as log:
               log.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Movido : {archivo} -> {destino} - Usuario : {usuario}\n" )

