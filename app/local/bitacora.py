from datetime import datetime
import os
import local.encriptado as enc

def bitacora(type, comand, instruction, bitacoraConfigure, llaveConfigure):
    fecha=""
    fecha = fechaYhora()
    if bitacoraConfigure=="true":
        instruccion = (enc.encrypt(f"{fecha} - {type} - {comand} - {instruction}", llaveConfigure)+"\n")
        output = f"{fecha} - {type} - {comand} - {instruction}\n"         
        bitacoraLog(instruccion)
        ejecucion = f"{comand} ejecutando..."
        write(ejecucion)
        write(output)
    else:
        instruccion = f"{fecha} - {type} - {comand} - {instruction}\n"        
        bitacoraLog(instruccion)
        ejecucion = f"{comand} ejecutando..."
        write(ejecucion)
        write(instruccion)


def fechaYhora():
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_datetime


def bitacoraLog(texto):
    fecha_actual = datetime.now()
    dia_actual = fecha_actual.day
    mes_actual = fecha_actual.month
    año_actual = fecha_actual.year

    ruta_log_archivos = os.path.join(os.path.dirname(__file__), "../../Archivos/log", str(año_actual), str(mes_actual), str(dia_actual))
    os.makedirs(ruta_log_archivos, exist_ok=True) 

    nombre_archivo = "log_archivos.txt"
    ruta_completa = os.path.join(ruta_log_archivos, nombre_archivo)

    with open(ruta_completa, "a") as archivo:
        archivo.write(texto)


def write(content):
    with open('app/log/consola.txt', 'a') as file:
        file.write(content)
        file.write('\n')  


totalLocal = 0
def tiempoLocal(numero):
        global totalLocal
        totalLocal += numero
        return totalLocal


totalCloud = 0
def tiempoCloud(numero):
        global totalCloud
        totalCloud += numero
        return totalCloud


totalProcesadosLocales = 0
def procesadosLocales(numero):
        global totalProcesadosLocales
        totalProcesadosLocales += numero
        return totalProcesadosLocales


totalProcesadosCloud = 0
def procesadosCloud(numero):
        global totalProcesadosCloud
        totalProcesadosCloud += numero
        return totalProcesadosCloud

def procesadosTotales():
    tiempo_local = tiempoLocal(0)
    tiempo_cloud = tiempoCloud(0)
    procesados_locales = procesadosLocales(0)
    procesados_cloud = procesadosCloud(0)
    fecha_y_hora = fechaYhora()
    total = f'{fecha_y_hora} - Output - Exec - Archivos procesados localmente: {procesados_locales} - Tiempo procesamiento local: {tiempo_local}ms - Archivos procesados en cloud: {procesados_cloud} -  Tiempo procesamiento cloud: {tiempo_cloud}ms'
    write(total)
    bitacoraLog(total)

def reiniciarVariables():
    global totalLocal, totalCloud, totalProcesadosLocales, totalProcesadosCloud
    totalLocal = 0
    totalCloud = 0
    totalProcesadosLocales = 0
    totalProcesadosCloud = 0