import os
import shutil

def rename_local(path, name):
    path = path.replace('"', '')
    path = path.lstrip('/')
    path = path.rstrip('/')
    archivo_proyecto = os.path.join(os.path.dirname(__file__), "../../Archivos", path)

    if os.path.exists(archivo_proyecto):

        if os.path.isfile(archivo_proyecto):
            new_path = os.path.join(os.path.dirname(archivo_proyecto), name)

            if os.path.exists(new_path):
                return(f"Error: Ya existe un archivo con el nombre {name}.")

            else:
                os.rename(archivo_proyecto, new_path)
                return(f"El archivo '{path}' ha sido renombrado a {name}.")

        elif os.path.isdir(archivo_proyecto):
            parent_dir = os.path.dirname(archivo_proyecto)
            new_path = os.path.join(parent_dir, name)

            if not os.path.exists(new_path):
                shutil.move(archivo_proyecto, new_path)
                return(f"La carpeta '{path}' ha sido renombrado a {name}.")

            else:
                return(f"Error: Ya existe una carpeta con el nombre {name}.")

    else:
        return(f"Error: No se encontro el archivo o carpeta '{path}' en la ruta especificada.")