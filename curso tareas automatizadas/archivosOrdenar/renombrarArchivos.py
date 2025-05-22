import os

carpeta = "C:/Users/EDINSONFLOREZ/Downloads/pruebasPY/curso tareas automatizadas/archivosOrdenar/springer ebooks"
prefijo = "Libro_Springer_"
extension = (".pdf")

archivos = []

for f in os.listdir(carpeta):
    if f.endswith(extension):
        archivos.append(f)

for i, nombre_actual in enumerate(archivos, start=1):
    extension_actual = os.path.splitext(nombre_actual)[1]
    nuevo_nombre = f"{prefijo}{i:03}{extension_actual}"

    ruta_actual = os.path.join(carpeta,nombre_actual)
    ruta_nueva = os.path.join(carpeta,nuevo_nombre)

    os.rename(ruta_actual,ruta_nueva)
