import os

def add_local(path, body):
    path = path.replace('"', '')
    path = path.lstrip('/')
    path = path.rstrip('/')
    archivo_proyecto = os.path.join(os.path.dirname(__file__), "../../Archivos", path)

    if os.path.isfile(archivo_proyecto):
        with open(archivo_proyecto, "a") as archivo:
            archivo.write(body)
        return(f"Contenido agregado al archivo '{path}' exitosamente.")

    else:
        return(f"Error: No se encontro el archivo '{path}' en la ruta especificada.")
