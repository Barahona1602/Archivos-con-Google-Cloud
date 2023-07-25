import os
import shutil


def copy_local(from_path, to):
    from_path = from_path.replace('"', '')
    to = to.replace('"', '')
    from_path = from_path.lstrip('/')
    from_path = from_path.rstrip('/')
    to = to.lstrip('/')
    to = to.rstrip('/')
    from_path_full = os.path.join(os.path.dirname(__file__), "../../Archivos", from_path)
    to_full = os.path.join(os.path.dirname(__file__), "../../Archivos", to)

    if os.path.exists(from_path_full):

        if os.path.isdir(from_path_full):
            
            if os.path.isdir(to_full) and os.path.basename(from_path_full) == os.path.basename(to_full):
                return (f"Error: Ya existe una carpeta con el nombre '{os.path.basename(from_path_full)}' en la ubicación de destino.")

            else:
                copyCarpeta(from_path_full, to_full)
                return (f"Contenido de la carpeta '{os.path.basename(from_path_full)}' copiado exitosamente a '{to}'.")

        elif os.path.isfile(from_path_full):
            file_name = os.path.basename(from_path_full)

            if os.path.exists(os.path.join(to_full, file_name)):
                return(f"Error: Ya existe un archivo con el nombre '{file_name}' en la ubicación de destino.")

            else:
                copyArchivo(from_path_full, os.path.join(to_full, file_name))
                return(f"Archivo '{file_name}' copiado exitosamente a '{to}'.")

    else:
        return (f"Error: No se encontró la carpeta o archivo '{from_path}' en la ruta especificada.")



def copyCarpeta(from_folder, to_folder):
    os.makedirs(to_folder, exist_ok=True)
    for item in os.listdir(from_folder):
        item_path = os.path.join(from_folder, item)
        if os.path.isfile(item_path):
            copyArchivo(item_path, os.path.join(to_folder, item))
        elif os.path.isdir(item_path):
            copyCarpeta(item_path, os.path.join(to_folder, item))


def copyArchivo(src, dst):
    shutil.copy2(src, dst)  