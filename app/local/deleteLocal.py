import os
import shutil

def delete_local(path, name):
    path = path.replace('"', '')
    path = path.lstrip('/')
    path = path.rstrip('/')
    if name == "not coming":
        name=""
        
    archivo_proyecto = os.path.join(os.path.dirname(__file__), "../../Archivos", path, name)

    if os.path.exists(archivo_proyecto):

        if os.path.isfile(archivo_proyecto):
            os.remove(archivo_proyecto)
            return (f"Archivo {name} eliminado exitosamente.")
        
        elif os.path.isdir(archivo_proyecto):
            shutil.rmtree(archivo_proyecto)
            return (f"Carpeta eliminada exitosamente.")
        
    else:
            return (f"Error: No se encontro el archivo o carpeta en la ruta especificada.")
