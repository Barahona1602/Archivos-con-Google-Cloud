import os

def create_local(name, body, path):
        name = validate_filename(name)
        path = path.replace('"', '')
        path = path.lstrip('/')

        archivo_proyecto = os.path.join(os.path.dirname(__file__), "../../Archivos", path, name)
        if not os.path.exists(archivo_proyecto): 
            os.makedirs(os.path.dirname(archivo_proyecto), exist_ok=True)
            
            with open(archivo_proyecto, "w") as archivo:
                archivo.write(body)
            return(f"Archivo {name} creado exitosamente")

        else:
            return(f"Error: La carpeta y el archivo ya existen")


def validate_filename(name):
    if name:
        if not name.endswith(".txt"):
            name += ".txt"
    return name