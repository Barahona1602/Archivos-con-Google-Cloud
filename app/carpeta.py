import time
from tkinter import messagebox
from local.bitacora import bitacora
from cloud.addStorage import add_cloud
from cloud.deleteStorage import delete_cloud
from cloud.modifyStorage import modify_cloud
from cloud.renameStorage import rename_cloud
from cloud.copyStorage import copy_cloud
from cloud.transferStorage import transfer_cloud
from cloud.createStorage import create_cloud
from cloud.backupStorage import backup_cloud
from local.createLocal import create_local
from local.deleteLocal import delete_local
from local.copyLocal import copy_local
from local.transferLocal import transfer_local
from local.renameLocal import rename_local
from local.modifyLocal import modify_local
from local.addLocal import add_local
from local.backupLocal import backup_local
from local.bitacora import tiempoLocal
from local.bitacora import tiempoCloud
from local.bitacora import procesadosLocales
from local.bitacora import procesadosCloud


global bitacoraConfigure
bitacoraConfigure = "false"
global tipo
tipo = ""
global contadorLocal
contadorLocal = 0
global contadorCloud
contadorCloud = 0


def configure(type, log, read, llave):
    comando="Configure"
    if type == None or log == None or read == None:
        tmp = "Error: No se ha configurado el tipo de almacenamiento"
        bitacora("Output", comando, tmp, "", "")
    else:
        global tipo
        tipo = type
        global bitacoraConfigure
        bitacoraConfigure = log
        global archivoConfigure
        archivoConfigure = read
        global llaveConfigure
        llaveConfigure = llave

        tmp = "Archivo configurado exitosamente"
        bitacora("Output", comando, tmp, bitacoraConfigure, llaveConfigure)



def create(name, body, path):
    comando="Create"
    if tipo == "local":
        inicio = time.time()
        tmp = create_local(name, body, path)
        tiempo_transcurrido = round((time.time() - inicio) * 1000)
        tiempoLocal(tiempo_transcurrido)
        procesadosLocales(1)
        bitacora("Output", comando, tmp, bitacoraConfigure, llaveConfigure)
    
    elif tipo == "cloud":
        procesadosCloud(1)
        inicio = time.time()
        tmp = create_cloud(body, path, name)
        tiempo_transcurrido = round((time.time() - inicio) * 1000)
        tiempoCloud(tiempo_transcurrido)
        
        bitacora("Output", comando, tmp, bitacoraConfigure, llaveConfigure)
       
    else:
        tmp = "Error: No se ha configurado el tipo de almacenamiento"
        bitacora("Output", comando, tmp, bitacoraConfigure, llaveConfigure)






def delete(path, name):
    print(path)
    print(name)
    path=path.replace(' -name','')
    comando="Delete"
    answer = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de que deseas eliminar?")
    if answer:
        if tipo == "local":
            inicio = time.time()
            tmp = delete_local(path, name)
            tiempo_transcurrido = round((time.time() - inicio) * 1000)
            tiempoLocal(tiempo_transcurrido)
            procesadosLocales(1)
            bitacora("Output", comando, tmp, bitacoraConfigure, llaveConfigure)
        
        elif tipo == "cloud":
            procesadosCloud(1)
            inicio = time.time()
            tmp = delete_cloud(path, name)
            tiempo_transcurrido = round((time.time() - inicio) * 1000)
            tiempoCloud(tiempo_transcurrido)
            
            bitacora("Output", comando, tmp, bitacoraConfigure, llaveConfigure)
        
        else:
            tmp = "Error: No se ha configurado el tipo de almacenamiento"
            bitacora("Output", comando, tmp, bitacoraConfigure, llaveConfigure)



def copy(from_path, to):
    comando="Copy"
    if tipo == "local":
        inicio = time.time()
        tmp = copy_local(from_path, to)
        tiempo_transcurrido = round((time.time() - inicio) * 1000)
        tiempoLocal(tiempo_transcurrido)
        procesadosLocales(1)
        bitacora("Output", comando, tmp, bitacoraConfigure, llaveConfigure)
   
    elif tipo == "cloud":
        procesadosCloud(1)
        inicio = time.time()
        tmp = copy_cloud(from_path, to)
        tiempo_transcurrido = round((time.time() - inicio) * 1000)
        tiempoCloud(tiempo_transcurrido)
       
        bitacora("Output", comando, tmp, bitacoraConfigure, llaveConfigure)
    
    else:
        tmp = "Error: No se ha configurado el tipo de almacenamiento"
        bitacora("Output", comando, tmp, bitacoraConfigure, llaveConfigure)



def transfer(from_path, to, mode):
    comando="Transfer"
    if tipo == "local":
        if mode =="local":
            inicio = time.time()
            tmp = transfer_local(from_path, to)
            tiempo_transcurrido = round((time.time() - inicio) * 1000)
            tiempoLocal(tiempo_transcurrido)
            procesadosLocales(1)
            bitacora("Output", comando, tmp, bitacoraConfigure, llaveConfigure)
        else:
            procesadosCloud(1)
            inicio = time.time()
            tmp = "Error: Modo no soportado"
            bitacora("Output", comando, tmp, bitacoraConfigure, llaveConfigure)
            tiempo_transcurrido = round((time.time() - inicio) * 1000)
            tiempoLocal(tiempo_transcurrido)
            

    elif tipo == "cloud":

        if mode == "local":
            # ESCRIBIR ACÁ EL CÓDIGO PARA EL CLOUD A LOCAL
            inicio = time.time()
            tmp = "Error: Modo no soportado"
            bitacora("Output", comando, tmp, bitacoraConfigure, llaveConfigure)
            tiempo_transcurrido = round((time.time() - inicio) * 1000)
            tiempoCloud(tiempo_transcurrido)
            procesadosCloud(1)

        else:
            procesadosCloud(1)
            inicio = time.time()
            tmp = transfer_cloud(from_path, to)
            tiempo_transcurrido = round((time.time() - inicio) * 1000)
            tiempoCloud(tiempo_transcurrido)
            
            bitacora("Output", comando, tmp, bitacoraConfigure, llaveConfigure)
    
    else:
        tmp = "Error: No se ha configurado el tipo de almacenamiento"
        bitacora("Output", comando, tmp, bitacoraConfigure, llaveConfigure)
        


def rename(path, name):
    comando="Rename"
    if tipo == "local":
        inicio = time.time()
        tmp = rename_local(path, name)
        tiempo_transcurrido = round((time.time() - inicio) * 1000)
        tiempoLocal(tiempo_transcurrido)
        procesadosLocales(1)
        bitacora("Output", comando, tmp, bitacoraConfigure, llaveConfigure)
    
    elif tipo == "cloud":
        procesadosCloud(1)
        inicio = time.time()
        tmp = rename_cloud(path, name)
        tiempo_transcurrido = round((time.time() - inicio) * 1000)
        tiempoCloud(tiempo_transcurrido)
        
        bitacora("Output", comando, tmp, bitacoraConfigure, llaveConfigure)
      
    else:
        tmp = "Error: No se ha configurado el tipo de almacenamiento"
        bitacora("Output", comando, tmp, bitacoraConfigure, llaveConfigure)



def modify(path, body):
    comando="Modify"
    if tipo == "local":
        inicio = time.time()
        tmp = modify_local(path, body)
        tiempo_transcurrido = round((time.time() - inicio) * 1000)
        tiempoLocal(tiempo_transcurrido)
        procesadosLocales(1)
        bitacora("Output", comando, tmp, bitacoraConfigure, llaveConfigure)
    
    elif tipo == "cloud":
        procesadosCloud(1)
        inicio = time.time()
        tmp = modify_cloud(path, body)
        tiempo_transcurrido = round((time.time() - inicio) * 1000)
        tiempoCloud(tiempo_transcurrido)
        
        bitacora("Output", comando, tmp, bitacoraConfigure, llaveConfigure)
    
    else:
        tmp = "Error: No se ha configurado el tipo de almacenamiento"
        bitacora("Output", comando, tmp, bitacoraConfigure, llaveConfigure)



def add(path, body):
    comando="Add"
    if tipo == "local":
        inicio = time.time()
        tmp = add_local(path, body)
        tiempo_transcurrido = round((time.time() - inicio) * 1000)
        tiempoLocal(tiempo_transcurrido)
        procesadosLocales(1)
        bitacora("Output", comando, tmp, bitacoraConfigure, llaveConfigure)
    
    elif tipo == "cloud":
        procesadosCloud(1)
        inicio = time.time()
        tmp = add_cloud(path, body)
        tiempo_transcurrido = round((time.time() - inicio) * 1000)
        tiempoCloud(tiempo_transcurrido)
        bitacora("Output", comando, tmp, bitacoraConfigure, llaveConfigure)
    
    else:
        tmp = "Error: No se ha configurado el tipo de almacenamiento"
        bitacora("Output", comando, tmp, bitacoraConfigure, llaveConfigure)



def backup():
    comando="Backup"
    if tipo == "local":
        inicio = time.time()
        print("Backup LOCAL -- - - - - - - ")
        tmp = backup_local()
        tiempo_transcurrido = round((time.time() - inicio) * 1000)
        tiempoLocal(tiempo_transcurrido)
        bitacora("Output", comando, tmp, bitacoraConfigure, llaveConfigure)
    elif tipo == "cloud":
        inicio = time.time()
        print("Backup CLOUD -- - - - - - - ")
        tmp = backup_cloud()
        tiempo_transcurrido = round((time.time() - inicio) * 1000)
        tiempoCloud(tiempo_transcurrido)
        bitacora("Output", comando, tmp, bitacoraConfigure, llaveConfigure)
    else:
        tmp = "Error: No se ha configurado el tipo de almacenamiento"
        bitacora("Output", comando, tmp, bitacoraConfigure, llaveConfigure)