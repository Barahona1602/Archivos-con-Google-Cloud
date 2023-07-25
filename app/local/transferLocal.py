import os
import shutil


def transfer_local(from_path, to):
    from_path = from_path.replace('"', '')
    to = to.replace('"', '')
    from_path = from_path.lstrip('/')
    from_path = from_path.rstrip('/')
    to = to.lstrip('/')
    to = to.rstrip('/')
    from_path_full = os.path.join(os.path.dirname(__file__), "../../Archivos", from_path)
    to_full = os.path.join(os.path.dirname(__file__), "../../Archivos", to)

    if os.path.exists(from_path_full):
        if os.path.isfile(from_path_full):
            transferArchivo(from_path_full, to_full)
            return "Archivo transferido exitosamente."

        elif os.path.isdir(from_path_full):
            transferCarpeta(from_path_full, to_full)
            return "Contenido de la carpeta transferido exitosamente."

        else:
            return "Error: El origen no es una carpeta ni un archivo válido."

    else:
        return "Error: No se encontró la carpeta o archivo en la ruta especificada."


def transferCarpeta(from_path, to_path):
    if not os.path.exists(to_path):
        os.makedirs(to_path)
    folder_name = os.path.basename(from_path)

    for item in os.listdir(from_path):
        item_path = os.path.join(from_path, item)
        transferArchivo(item_path, os.path.join(to_path, item))

    return "Contenido de la carpeta transferido exitosamente."


def transferArchivo(from_path, to_path):
    to_folder = os.path.dirname(to_path)
    if not os.path.exists(to_folder):
        os.makedirs(to_folder)

    file_name = os.path.basename(from_path)
    base_name, extension = os.path.splitext(file_name)

    dest_path = to_path
    if os.path.exists(dest_path):
        counter = 1
        while os.path.exists(dest_path):
            new_file_name = f"{base_name}({counter}){extension}"
            dest_path = os.path.join(to_folder, new_file_name)
            counter += 1

    if os.path.isdir(to_path):
        dest_path = os.path.join(to_path, file_name)

    shutil.move(from_path, dest_path)
    return f"El archivo '{file_name}' se ha movido exitosamente a '{os.path.basename(dest_path)}'."
