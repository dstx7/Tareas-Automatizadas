import os
import shutil
import getpass
import time
import threading

from tkinter import Tk, filedialog, Button, Label
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

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
    ".mkv":"videos",
    ".docx":"words",
    ".txt":"textos"
} 

def esperar_archivo_libre (ruta_archivo, intentos = 10, espera = 0.5):
    for i in range(intentos):
        try:
            with open(ruta_archivo, "rb"):
                return True
        except (PermissionError, OSError):
            time.sleep(espera)
    return False
        
#funcion para ordernar archivos
def ordernar_archivos(ruta):

    for archivo in os.listdir(ruta):
        
        ruta_archivo = os.path.join(ruta,archivo)

        # Ignorar el archivo de log
        if archivo == "log_movimientos.txt":
                continue
        
        if not esperar_archivo_libre(ruta_archivo):
            print(f"el archivo {ruta_archivo} esta siendo utilizado")
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

class ManejadorEventos(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"Nuevo archivo detectado: {event.src_path}")
            ordernar_archivos(ruta)

for carpeta in set(extensiones.values()):
    ruta_carpeta = os.path.join(ruta,carpeta)

    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)

ordernar_archivos(ruta)

manejador_eventos = ManejadorEventos()
observador = Observer()
observador.schedule(manejador_eventos,ruta,recursive=False)
#observador.start()
"""
try:
    while True:
        print("Siguiente vigilancia, use CTRL + C para detener")
        time.sleep(1)

except KeyboardInterrupt:
    print("Deteniendo vigilancia")
    observador.stop()
"""
def iniciar_vigilancia():
    observador.start()

def detener_vigilancia():
    observador.stop()
    observador.join()

ventana.deiconify()
ventana.title("Vigilancia de carpeta ")
ventana.geometry("1280x720")


Label(ventana, text=f"vigilando la carpeta: {ruta}", wraplength=350).pack(pady=10)
Button(ventana, text="Detener vigilancia y salir", command=detener_vigilancia).pack(pady=10)

hilo_vigilancia = threading.Thread(target = iniciar_vigilancia, daemon=True)
hilo_vigilancia.start()

ventana.mainloop()