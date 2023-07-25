from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageTk
from encriptado import decrypt
import encriptado as enc
import carpeta as carp
import threading
import time
from scanner.tokens import extract_commands
import scanner.scanner as scan
from local.bitacora import bitacora
from local.bitacora import procesadosTotales
from local.bitacora import reiniciarVariables
#--- CONTRASEÑAS ---
#Pablo42
#Alvaro123



# Función para realizar el login
def login():
    file_path = "app/log/miausuarios.txt"
    user_credentials = []
    global username
    with open(file_path, "r") as file:
        lines = file.readlines()

        for i in range(0, len(lines), 2):
            username = lines[i].strip()
            password = lines[i + 1].strip()
            user_credentials.append((username, password))

    entered_username = username_entry.get()
    entered_password = enc.encrypt(password_entry.get(),"miaproyecto12345")

    for username, password in user_credentials:
        if entered_username == username and entered_password == password.lower():
            bitacora("Input", "Sesion", f"Inicio de sesion de {username}", "", "")
            messagebox.showinfo(title="Login", message="Bienvenido " + username)
            username_entry.delete(0, END)
            password_entry.delete(0, END)
            # Ocultar la ventana de inicio de sesión
            root.withdraw()
            # Abrir la ventana principal
            open_main_window()
            break
    else:
        messagebox.showerror(title="Error", message="Acceso denegado")



# Función para mostrar la ventana de inicio de sesión
def open_main_window():
    # Crear la ventana principal
    main_window = tk.Toplevel()
    main_window.title("Ventana Principal")
    main_window.resizable(False, False)
    main_window.geometry("840x640")
    main_window.protocol("WM_DELETE_WINDOW", show_login)  # Volver al login al cerrar

    def close_main_window():
        main_window.withdraw()
        show_login()
        bitacora("Output", "Sesion", f"Se cerro sesion {username}", "", "")
        


    # Ventana configure
    def configure():
        configure_window = tk.Toplevel()
        configure_window.title("configure")
        configure_window.resizable(False, False)
        configure_window.geometry("640x440")

        def aceptar():
            type = selected_option1.get()
            encrypt_log = selected_option2.get()
            encrypt_read = selected_option3.get()
            llave = text_entry.get()
            if (type !="" and encrypt_log !="" and encrypt_read !=""):
                

                if encrypt_log == "True" or encrypt_read == "True":
                    if len(llave) != 16:
                        messagebox.showerror(title="Error", message="La llave debe tener 16 caracteres")
                    else:
                        carp.configure(type, encrypt_log, encrypt_read, llave)
                        configure_window.withdraw()
                        bitacora("Output", "Configure", f"Se configuro el programa con los siguientes datos: Tipo: {type}, Encrypt Log: {encrypt_log}, Encrypt Read: {encrypt_read}, Llave: {llave}", "", "")

                else:
                    
                    carp.configure(type, encrypt_log, encrypt_read, llave)
                    configure_window.withdraw()
                    bitacora("Output", "Configure", f"Se configuro el programa con los siguientes datos: Tipo: {type}, Encrypt Log: {encrypt_log}, Encrypt Read: {encrypt_read}, Llave: {llave}", "", "")
            else:
                messagebox.showerror(title="Error", message="Existen campos vacíos")

        # Cargando la imagen de fondo de la ventana configure
        img_path2 = os.path.join(os.path.dirname(__file__), "images/configure.png")
        bg_img2 = Image.open(img_path2)
        image2 = ImageTk.PhotoImage(bg_img2)

        
        canvas2 = Canvas(configure_window, width=640, height=440)
        canvas2.pack()

        
        canvas2.create_image(0, 0, image=image2, anchor=NW)
        canvas2.image = image2  

        # widgets de la ventana configure
        optionsTYPE = ["local", "cloud"]
        optionsTF = ["true", "false"]
        selected_option1 = tk.StringVar()
        selected_option2 = tk.StringVar()
        selected_option3 = tk.StringVar()
        text_entry = tk.StringVar()

        combo1 = ttk.Combobox(configure_window, width=40, font=("Arial", 12), values=optionsTYPE, state="readonly", textvariable=selected_option1)
        combo1.place(x=200, y=95)
        combo2 = ttk.Combobox(configure_window, width=40, font=("Arial", 12), values=optionsTF, state="readonly", textvariable=selected_option2)
        combo2.place(x=200, y=160)
        combo3 = ttk.Combobox(configure_window, width=40, font=("Arial", 12), values=optionsTF, state="readonly", textvariable=selected_option3)
        combo3.place(x=200, y=225)
        entry = Entry(configure_window, font=("Arial", 12), width=40, textvariable=text_entry)
        entry.place(x=200, y=290)
        aceptar_button = Button(configure_window, text="Aceptar", font=("Arial", 12), bg="#49B8A9", fg="#FFFFFF", width=10, command=aceptar)
        aceptar_button.place(x=250, y=370)



    # Ventana create
    def create():
        create_window = tk.Toplevel()
        create_window.title("create")
        create_window.resizable(False, False)
        create_window.geometry("640x440")

        def aceptar():
            name = text_entry1.get()
            body = text_entry2.get()
            path = text_entry3.get()
            if (path != "" and body != "" and name != ""):
                bitacora("Input", "Create", f"Crear {name}.txt en la ruta {path}", "", "")
                carp.create(name, body, path)
                create_window.withdraw()
            else:
                messagebox.showerror(title="Error", message="Existen campos vacíos")

        # Cargando la imagen de fondo de la ventana create
        img_path2 = os.path.join(os.path.dirname(__file__), "images/create.png")
        bg_img2 = Image.open(img_path2)
        image2 = ImageTk.PhotoImage(bg_img2)

        
        canvas2 = Canvas(create_window, width=640, height=440)
        canvas2.pack()

        
        canvas2.create_image(0, 0, image=image2, anchor=NW)
        canvas2.image = image2  

        # widgets de la ventana create
        text_entry1 = tk.StringVar()
        text_entry2 = tk.StringVar()
        text_entry3 = tk.StringVar()

        entry1 = Entry(create_window, font=("Arial", 12), width=40, textvariable=text_entry1)
        entry1.place(x=200, y=95)
        entry2 = Entry(create_window, font=("Arial", 12), width=40, textvariable=text_entry2)        
        entry2.place(x=200, y=160)
        entry3 = Entry(create_window, font=("Arial", 12), width=40, textvariable=text_entry3)
        entry3.place(x=200, y=225)
        aceptar_button = Button(create_window, text="Aceptar", font=("Arial", 12), bg="#49B8A9", fg="#FFFFFF", width=10, command=aceptar)
        aceptar_button.place(x=250, y=370)



    #ventana delete
    def delete():
        delete_window = tk.Toplevel()
        delete_window.title("delete")
        delete_window.resizable(False, False)
        delete_window.geometry("640x440")

        def aceptar():
            path = text_entry1.get()
            name = text_entry2.get()
            if (path != ""):
                bitacora("Input", "Delete", f"Eliminar {name} de la ruta {path}", "", "")

                carp.delete(path, name)
                delete_window.withdraw()
            else:
                messagebox.showerror("Error", "Existen campos vacíos")

        # Cargando la imagen de fondo de la ventana delete
        img_path2 = os.path.join(os.path.dirname(__file__), "images/delete.png")
        bg_img2 = Image.open(img_path2)
        image2 = ImageTk.PhotoImage(bg_img2)

        
        canvas2 = Canvas(delete_window, width=640, height=440)
        canvas2.pack()

        
        canvas2.create_image(0, 0, image=image2, anchor=NW)
        canvas2.image = image2  

        # widgets de la ventana delete
        text_entry1 = tk.StringVar()
        text_entry2 = tk.StringVar()

        entry1 = Entry(delete_window, font=("Arial", 12), width=40, textvariable=text_entry1)
        entry1.place(x=200, y=95)
        entry2 = Entry(delete_window, font=("Arial", 12), width=40, textvariable=text_entry2)        
        entry2.place(x=200, y=160)
        aceptar_button = Button(delete_window, text="Aceptar", font=("Arial", 12), bg="#49B8A9", fg="#FFFFFF", width=10, command=aceptar)
        aceptar_button.place(x=250, y=370)



    #Ventana copy
    def copy():
        copy_window = tk.Toplevel()
        copy_window.title("copy")
        copy_window.resizable(False, False)
        copy_window.geometry("640x440")

        def aceptar():
            from_ = text_entry1.get()
            to = text_entry2.get()
            if (from_ != "" and to !=""):
                bitacora("Input", "Copy", f"Copiar el contenido de {from_} a {to}", "", "")

                carp.copy(from_, to)
                copy_window.withdraw()
            else:
                messagebox.showerror("Error", "Existen campos vacíos")

        # Cargando la imagen de fondo de la ventana copy
        img_path2 = os.path.join(os.path.dirname(__file__), "images/copy.png")
        bg_img2 = Image.open(img_path2)
        image2 = ImageTk.PhotoImage(bg_img2)

        
        canvas2 = Canvas(copy_window, width=640, height=440)
        canvas2.pack()

        
        canvas2.create_image(0, 0, image=image2, anchor=NW)
        canvas2.image = image2  

        # widgets de la ventana copy
        text_entry1 = tk.StringVar()
        text_entry2 = tk.StringVar()

        entry1 = Entry(copy_window, font=("Arial", 12), width=40, textvariable=text_entry1)
        entry1.place(x=200, y=95)
        entry2 = Entry(copy_window, font=("Arial", 12), width=40, textvariable=text_entry2)        
        entry2.place(x=200, y=160)
        aceptar_button = Button(copy_window, text="Aceptar", font=("Arial", 12), bg="#49B8A9", fg="#FFFFFF", width=10, command=aceptar)
        aceptar_button.place(x=250, y=370)



    #Ventana transfer
    def transfer():
        transfer_window = tk.Toplevel()
        transfer_window.title("transfer")
        transfer_window.resizable(False, False)
        transfer_window.geometry("640x440")

        def aceptar():
            from_ = text_entry1.get()
            to = text_entry2.get()
            mode = selected_option1.get()
            if (from_ != "" and to !="" and mode != ""):
                bitacora("Input", "Transfer", f"Transferir el contenido de {from_} a {to} en {mode}", "", "")

                carp.transfer(from_, to, mode)
                transfer_window.withdraw()
            else:
                messagebox.showerror("Error", "Existen campos vacíos")

        # Cargando la imagen de fondo de la ventana transfer
        img_path2 = os.path.join(os.path.dirname(__file__), "images/transfer.png")
        bg_img2 = Image.open(img_path2)
        image2 = ImageTk.PhotoImage(bg_img2)

        
        canvas2 = Canvas(transfer_window, width=640, height=440)
        canvas2.pack()

        
        canvas2.create_image(0, 0, image=image2, anchor=NW)
        canvas2.image = image2  

        # widgets de la ventana transfer
        optionsTYPE = ["local", "cloud"]
        text_entry1 = tk.StringVar()
        text_entry2 = tk.StringVar()
        selected_option1 = tk.StringVar()

        entry1 = Entry(transfer_window, font=("Arial", 12), width=40, textvariable=text_entry1)
        entry1.place(x=200, y=95)
        entry2 = Entry(transfer_window, font=("Arial", 12), width=40, textvariable=text_entry2)        
        entry2.place(x=200, y=160)
        combo1 = ttk.Combobox(transfer_window, width=40, font=("Arial", 12), values=optionsTYPE, state="readonly", textvariable=selected_option1)
        combo1.place(x=200, y=225)
        aceptar_button = Button(transfer_window, text="Aceptar", font=("Arial", 12), bg="#49B8A9", fg="#FFFFFF", width=10, command=aceptar)
        aceptar_button.place(x=250, y=370)



    #Ventana rename
    def rename():
        rename_window = tk.Toplevel()
        rename_window.title("rename")
        rename_window.resizable(False, False)
        rename_window.geometry("640x440")

        def aceptar():
            path = text_entry1.get()
            name = text_entry2.get()
            if (path != "" and name !=""):
                bitacoraReturn = carp.bitacora("Input", "Rename", f"Cambiar el nombre en {path} a {name}", "", "")

                carp.rename(path, name)
                rename_window.withdraw()
            else:
                messagebox.showerror("Error", "Existen campos vacíos")

        # Cargando la imagen de fondo de la ventana rename
        img_path2 = os.path.join(os.path.dirname(__file__), "images/rename.png")
        bg_img2 = Image.open(img_path2)
        image2 = ImageTk.PhotoImage(bg_img2)

        
        canvas2 = Canvas(rename_window, width=640, height=440)
        canvas2.pack()

        
        canvas2.create_image(0, 0, image=image2, anchor=NW)
        canvas2.image = image2  

        # widgets de la ventana rename
        text_entry1 = tk.StringVar()
        text_entry2 = tk.StringVar()

        entry1 = Entry(rename_window, font=("Arial", 12), width=40, textvariable=text_entry1)
        entry1.place(x=200, y=95)
        entry2 = Entry(rename_window, font=("Arial", 12), width=40, textvariable=text_entry2)        
        entry2.place(x=200, y=160)
        aceptar_button = Button(rename_window, text="Aceptar", font=("Arial", 12), bg="#49B8A9", fg="#FFFFFF", width=10, command=aceptar)
        aceptar_button.place(x=250, y=370)



    #Ventana modify
    def modify():
        modify_window = tk.Toplevel()
        modify_window.title("modify")
        modify_window.resizable(False, False)
        modify_window.geometry("640x440")

        def aceptar():
            path = text_entry1.get()
            body = text_entry2.get()
            if (path != "" and body !=""):
                bitacora("Input", "Modify", f"Modificar el contenido de {path} a {body}", "", "")

                carp.modify(path, body)
                modify_window.withdraw()
            else:
                messagebox.showerror("Error", "Existen campos vacíos")

        # Cargando la imagen de fondo de la ventana modify
        img_path2 = os.path.join(os.path.dirname(__file__), "images/modify.png")
        bg_img2 = Image.open(img_path2)
        image2 = ImageTk.PhotoImage(bg_img2)

        
        canvas2 = Canvas(modify_window, width=640, height=440)
        canvas2.pack()

        
        canvas2.create_image(0, 0, image=image2, anchor=NW)
        canvas2.image = image2  

        # widgets de la ventana modify
        text_entry1 = tk.StringVar()
        text_entry2 = tk.StringVar()

        entry1 = Entry(modify_window, font=("Arial", 12), width=40, textvariable=text_entry1)
        entry1.place(x=200, y=95)
        entry2 = Entry(modify_window, font=("Arial", 12), width=40, textvariable=text_entry2)        
        entry2.place(x=200, y=160)
        aceptar_button = Button(modify_window, text="Aceptar", font=("Arial", 12), bg="#49B8A9", fg="#FFFFFF", width=10, command=aceptar)
        aceptar_button.place(x=250, y=370)



    #Ventana add
    def add():
        add_window = tk.Toplevel()
        add_window.title("add")
        add_window.resizable(False, False)
        add_window.geometry("640x440")

        def aceptar():
            path = text_entry1.get()
            body = text_entry2.get()
            if (path != "" and body !=""):
                bitacora("Input", "Add", f"Agregar {body} a {path}", "", "")

                carp.add(path, body)
                add_window.withdraw()
            else: 
                messagebox.showerror("Error", "Existen campos vacíos")

        # Cargando la imagen de fondo de la ventana add
        img_path2 = os.path.join(os.path.dirname(__file__), "images/add.png")
        bg_img2 = Image.open(img_path2)
        image2 = ImageTk.PhotoImage(bg_img2)

        
        canvas2 = Canvas(add_window, width=640, height=440)
        canvas2.pack()

        
        canvas2.create_image(0, 0, image=image2, anchor=NW)
        canvas2.image = image2  

        # widgets de la ventana add
        text_entry1 = tk.StringVar()
        text_entry2 = tk.StringVar()

        entry1 = Entry(add_window, font=("Arial", 12), width=40, textvariable=text_entry1)
        entry1.place(x=200, y=95)
        entry2 = Entry(add_window, font=("Arial", 12), width=40, textvariable=text_entry2)        
        entry2.place(x=200, y=160)
        aceptar_button = Button(add_window, text="Aceptar", font=("Arial", 12), bg="#49B8A9", fg="#FFFFFF", width=10, command=aceptar)
        aceptar_button.place(x=250, y=370)



    #Backup método
    def backup():
        bitacora("Input", "Backup", "Iniciar un backup", "", "")
        carp.backup()



    #Ventana execu
    def execu():
        execu_window = tk.Toplevel()
        execu_window.title("execu")
        execu_window.resizable(False, False)
        execu_window.geometry("640x440")

        def aceptar():
            path = text_entry1.get()
            if path != "":
                bitacora("Input", "Exec", f"Ejecutar {path}", "", "")
                exec_aux(path)
                execu_window.withdraw()
            else:
                messagebox.showerror("Error", "Existen campos vacíos")

        # Cargando la imagen de fondo de la ventana execu
        img_path2 = os.path.join(os.path.dirname(__file__), "images/exec.png")
        bg_img2 = Image.open(img_path2)
        image2 = ImageTk.PhotoImage(bg_img2)

        
        canvas2 = Canvas(execu_window, width=640, height=440)
        canvas2.pack()

        
        canvas2.create_image(0, 0, image=image2, anchor=NW)
        canvas2.image = image2  

        # widgets de la ventana execu
        text_entry1 = tk.StringVar()

        entry1 = Entry(execu_window, font=("Arial", 12), width=40, textvariable=text_entry1)
        entry1.place(x=200, y=95)
        aceptar_button = Button(execu_window, text="Aceptar", font=("Arial", 12), bg="#49B8A9", fg="#FFFFFF", width=10, command=aceptar)
        aceptar_button.place(x=250, y=370)

    def enter():
        eliminarConsola()
        reiniciarVariables()
        content = console_txt2.get("1.0", tk.END)
        # evaluate if the console recieves the encrypted data with the configure command
        command = extract_commands(content)
        # first case 
        if command[0] != None and command[1] == "":
            print("Viene configure y no viene encriptado")
            configure, type, encrypt_log, encrypt_read, llave = scan.scan_command_line_configure(command[0])
            carp.configure(type, encrypt_log, encrypt_read, llave)
            reiniciarVariables()
            return
        # second case
        elif command[0] != None and command[1] != None :
            print("Viene configure y encriptado")
            configure, type, encrypt_log, encrypt_read, llave = scan.scan_command_line_configure(command[0])
            carp.configure(type, encrypt_log, encrypt_read, llave)
            message_decrypted = decrypt(command[1], llave)
            comandos = extract_commands(message_decrypted)
            for token in comandos[0]:      
                    if(token.get("create")):
                        create, name, path, body = scan.scan_command_line_create(token.get("create"))
                        name = name.rstrip()
                        path = path.rstrip()
                        carp.create(name, body, path)
                    elif(token.get("delete")):
                        delete, path, name = scan.scan_command_line_delete(token.get("delete"))
                        path = path.rstrip()
                        name = name.rstrip()
                        carp.delete(path, name)
                    elif(token.get("copy")):
                        copy, from_, to = scan.scan_command_line_copy(token.get("copy"))
                        from_ = from_.rstrip()
                        to = to.rstrip()
                        carp.copy(from_, to)
                    elif(token.get("transfer")):
                        transfer, from_, to, mode = scan.scan_command_line_transfer(token.get("transfer"))
                        from_ = from_.rstrip()
                        to = to.rstrip()
                        mode = mode.rstrip()
                        carp.transfer(from_, to, mode)
                    elif(token.get("rename")):
                        rename, path, name = scan.scan_command_line_rename(token.get("rename"))
                        path = path.rstrip()
                        name = name.rstrip()
                        carp.rename(path, name)
                    elif(token.get("modify")):
                        modify, path, body = scan.scan_command_line_modify(token.get("modify"))
                        path = path.rstrip()
                        carp.modify(path, body)
                    elif(token.get("add")):
                        add, path, body = scan.scan_command_line_add(token.get("add"))
                        path = path.rstrip()
                        carp.add(path, body)
                    elif(token.get("backup")):
                        carp.backup()
            reiniciarVariables()
            return
        # third case
        elif command[0] == None and command[1] != None:
            print("Viene encriptado y no viene configure")
            message_decrypted = decrypt(command[1], llave)
            comandos = extract_commands(message_decrypted)
            for token in comandos[0]:
                if(token.get("configure")):
                    configure, type, encrypt_log, encrypt_read, llave = scan.scan_command_line_configure(token.get("configure"))
                    carp.configure(type, encrypt_log, encrypt_read, llave)
                elif(token.get("create")):
                    create, name, path, body = scan.scan_command_line_create(token.get("create"))
                    name = name.rstrip()
                    path = path.rstrip()
                    carp.create(name, body, path)
                elif(token.get("delete")):
                    delete, path, name = scan.scan_command_line_delete(token.get("delete"))
                    path = path.rstrip()
                    name = name.rstrip()
                    carp.delete(path, name)
                elif(token.get("copy")):
                    copy, from_, to = scan.scan_command_line_copy(token.get("copy"))
                    from_ = from_.rstrip()
                    to = to.rstrip()
                    carp.copy(from_, to)
                elif(token.get("transfer")):
                    transfer, from_, to, mode = scan.scan_command_line_transfer(token.get("transfer"))
                    from_ = from_.rstrip()
                    to = to.rstrip()
                    mode = mode.rstrip()
                    carp.transfer(from_, to, mode)
                elif(token.get("rename")):
                    rename, path, name = scan.scan_command_line_rename(token.get("rename"))
                    path = path.rstrip()
                    name = name.rstrip()
                    carp.rename(path, name)
                elif(token.get("modify")):
                    modify, path, body = scan.scan_command_line_modify(token.get("modify"))
                    path = path.rstrip()
                    carp.modify(path, body)
                elif(token.get("add")):
                    add, path, body = scan.scan_command_line_add(token.get("add"))
                    path = path.rstrip()
                    carp.add(path, body)
                elif(token.get("backup")):
                    carp.backup()
            reiniciarVariables()
            return
        # if the console recieves commands without the configure command and without encryption
        command = extract_commands(content)
        if command[0][0].get("exec"):

            exec, path = scan.scan_command_line_exec(command[0][0].get("exec"))
            directorio_actual = os.getcwd()
            ruta_archivo = os.path.join(directorio_actual, "Archivos", path)
            with open(ruta_archivo, "r") as archivo:
                content = archivo.read()
            configure_command, message_crypted = extract_commands(content)
            if message_crypted != None :
                # print(configure_command,message_crypted)
                # return
                configure, type, encrypt_log, encrypt_read, llave = scan.scan_command_line_configure(configure_command)
                carp.configure(type, encrypt_log, encrypt_read, llave)
                message_decrypted = decrypt(message_crypted, llave)
                comandos = extract_commands(message_decrypted)
                for token in comandos[0]:      
                    if(token.get("create")):
                        create, name, path, body = scan.scan_command_line_create(token.get("create"))
                        name = name.rstrip()
                        path = path.rstrip()
                        carp.create(name, body, path)
                    elif(token.get("delete")):
                        delete, path, name = scan.scan_command_line_delete(token.get("delete"))
                        path = path.rstrip()
                        name = name.rstrip()
                        carp.delete(path, name)
                    elif(token.get("copy")):
                        copy, from_, to = scan.scan_command_line_copy(token.get("copy"))
                        from_ = from_.rstrip()
                        to = to.rstrip()
                        carp.copy(from_, to)
                    elif(token.get("transfer")):
                        transfer, from_, to, mode = scan.scan_command_line_transfer(token.get("transfer"))
                        from_ = from_.rstrip()
                        to = to.rstrip()
                        mode = mode.rstrip()
                        carp.transfer(from_, to, mode)
                    elif(token.get("rename")):
                        rename, path, name = scan.scan_command_line_rename(token.get("rename"))
                        path = path.rstrip()
                        name = name.rstrip()
                        carp.rename(path, name)
                    elif(token.get("modify")):
                        modify, path, body = scan.scan_command_line_modify(token.get("modify"))
                        path = path.rstrip()
                        carp.modify(path, body)
                    elif(token.get("add")):
                        add, path, body = scan.scan_command_line_add(token.get("add"))
                        path = path.rstrip()
                        carp.add(path, body)
                    elif(token.get("backup")):
                        carp.backup()
                procesadosTotales()
            else:
                comandos = extract_commands(content)
                print(comandos[0])
                # return 
                for token in comandos[0]:
                    if(token.get("configure")):
                        configure, type, encrypt_log, encrypt_read, llave = scan.scan_command_line_configure(token.get("configure"))
                        carp.configure(type, encrypt_log, encrypt_read, llave)
                    elif(token.get("create")):
                        create, name, path, body = scan.scan_command_line_create(token.get("create"))
                        name = name.rstrip()
                        path = path.rstrip()
                        carp.create(name, body, path)
                    elif(token.get("delete")):
                        delete, path, name = scan.scan_command_line_delete(token.get("delete"))
                        path = path.rstrip()
                        name = name.rstrip()
                        carp.delete(path, name)
                    elif(token.get("copy")):
                        copy, from_, to = scan.scan_command_line_copy(token.get("copy"))
                        from_ = from_.rstrip()
                        to = to.rstrip()
                        carp.copy(from_, to)
                    elif(token.get("transfer")):
                        transfer, from_, to, mode = scan.scan_command_line_transfer(token.get("transfer"))
                        carp.transfer(from_, to, mode)
                    elif(token.get("rename")):
                        rename, path, name = scan.scan_command_line_rename(token.get("rename"))
                        path = path.rstrip()
                        name = name.rstrip()
                        carp.rename(path, name)
                    elif(token.get("modify")):
                        modify, path, body = scan.scan_command_line_modify(token.get("modify"))
                        path = path.rstrip()
                        carp.modify(path, body)
                    elif(token.get("add")):
                        add, path, body = scan.scan_command_line_add(token.get("add"))
                        path = path.rstrip()
                        carp.add(path, body)
                    elif(token.get("backup")):
                        carp.backup()
                procesadosTotales()
                
        else:
            for token in command[0]:
                if(token.get("configure")):
                    configure, type, encrypt_log, encrypt_read, llave = scan.scan_command_line_configure(token.get("configure"))
                    carp.configure(type, encrypt_log, encrypt_read, llave)
                    
                elif(token.get("create")):
                    create, name, path, body = scan.scan_command_line_create(token.get("create"))
                    name = name.rstrip()
                    path = path.rstrip()
                    carp.create(name, body, path)
                elif(token.get("delete")):
                    delete, path, name = scan.scan_command_line_delete(token.get("delete"))
                    path = path.rstrip()
                    name = name.rstrip()
                    carp.delete(path, name)
                elif(token.get("copy")):
                    copy, from_, to = scan.scan_command_line_copy(token.get("copy"))
                    from_ = from_.rstrip()
                    to = to.rstrip()
                    carp.copy(from_, to)
                elif(token.get("transfer")):
                    transfer, from_, to, mode = scan.scan_command_line_transfer(token.get("transfer"))
                    carp.transfer(from_, to, mode)
                elif(token.get("rename")):
                    rename, path, name = scan.scan_command_line_rename(token.get("rename"))
                    path = path.rstrip()
                    name = name.rstrip()
                    carp.rename(path, name)
                elif(token.get("modify")):
                    modify, path, body = scan.scan_command_line_modify(token.get("modify"))
                    path = path.rstrip()
                    carp.modify(path, body)
                elif(token.get("add")):
                    add, path, body = scan.scan_command_line_add(token.get("add"))
                    path = path.rstrip()
                    carp.add(path, body)
                elif(token.get("backup")):
                    carp.backup()
    
    def exec_aux(path):
        eliminarConsola()
        reiniciarVariables()
        directorio_actual = os.getcwd()
        ruta_archivo = os.path.join(directorio_actual, "Archivos", path)
        with open(ruta_archivo, "r") as archivo:
            content = archivo.read()
        
        configure_command, message_crypted = extract_commands(content)
        if message_crypted != None:
            configure, type, encrypt_log, encrypt_read, llave = scan.scan_command_line_configure(configure_command)
            carp.configure(type, encrypt_log, encrypt_read, llave)
            message_decrypted = decrypt(message_crypted, llave)
            comandos = extract_commands(message_decrypted)
            for token in comandos[0]:      
                if(token.get("create")):
                    create, name, path, body = scan.scan_command_line_create(token.get("create"))
                    name = name.rstrip()
                    path = path.rstrip()
                    carp.create(name, body, path)
                elif(token.get("delete")):
                    delete, path, name = scan.scan_command_line_delete(token.get("delete"))
                    path = path.rstrip()
                    name = name.rstrip()
                    carp.delete(path, name)
                elif(token.get("copy")):
                    copy, from_, to = scan.scan_command_line_copy(token.get("copy"))
                    from_ = from_.rstrip()
                    to = to.rstrip()
                    carp.copy(from_, to)
                elif(token.get("transfer")):
                    transfer, from_, to, mode = scan.scan_command_line_transfer(token.get("transfer"))
                    from_ = from_.rstrip()
                    to = to.rstrip()
                    mode = mode.rstrip()
                    carp.transfer(from_, to, mode)
                elif(token.get("rename")):
                    rename, path, name = scan.scan_command_line_rename(token.get("rename"))
                    path = path.rstrip()
                    name = name.rstrip()
                    carp.rename(path, name)
                elif(token.get("modify")):
                    modify, path, body = scan.scan_command_line_modify(token.get("modify"))
                    path = path.rstrip()
                    carp.modify(path, body)
                elif(token.get("add")):
                    add, path, body = scan.scan_command_line_add(token.get("add"))
                    path = path.rstrip()
                    carp.add(path, body)
                elif(token.get("backup")):
                    carp.backup()
            procesadosTotales()
            
        else:
            comandos = extract_commands(content)
            for token in comandos[0]:
                if(token.get("configure")):
                    configure, type, encrypt_log, encrypt_read, llave = scan.scan_command_line_configure(token.get("configure"))
                    carp.configure(type, encrypt_log, encrypt_read, llave)
                    
                elif(token.get("create")):
                    create, name, path, body = scan.scan_command_line_create(token.get("create"))
                    name = name.rstrip()
                    path = path.rstrip()
                    carp.create(name, body, path)
                elif(token.get("delete")):
                    delete, path, name = scan.scan_command_line_delete(token.get("delete"))
                    path = path.rstrip()
                    name = name.rstrip()
                    carp.delete(path, name)
                elif(token.get("copy")):
                    copy, from_, to = scan.scan_command_line_copy(token.get("copy"))
                    from_ = from_.rstrip()
                    to = to.rstrip()
                    carp.copy(from_, to)
                elif(token.get("transfer")):
                    transfer, from_, to, mode = scan.scan_command_line_transfer(token.get("transfer"))
                    from_ = from_.rstrip()
                    to = to.rstrip()
                    mode = mode.rstrip()
                    carp.transfer(from_, to, mode)
                elif(token.get("rename")):
                    rename, path, name = scan.scan_command_line_rename(token.get("rename"))
                    path = path.rstrip()
                    name = name.rstrip()
                    carp.rename(path, name)
                elif(token.get("modify")):
                    modify, path, body = scan.scan_command_line_modify(token.get("modify"))
                    path = path.rstrip()
                    carp.modify(path, body)
                elif(token.get("add")):
                    add, path, body = scan.scan_command_line_add(token.get("add"))
                    path = path.rstrip()
                    carp.add(path, body)
                elif(token.get("backup")):
                    carp.backup()
            procesadosTotales()
        

    


    main_window.protocol("WM_DELETE_WINDOW", close_main_window)

    # Cargando la imagen de fondo de la ventana principal
    img_path = os.path.join(os.path.dirname(__file__), "images/ventanaprincipal.png")
    bg_img = Image.open(img_path)
    image = ImageTk.PhotoImage(bg_img)

    
    canvas = Canvas(main_window, width=840, height=640)
    canvas.pack()

    
    canvas.create_image(0, 0, image=image, anchor=NW)
    canvas.image = image  


    espaciado=35
    # Contenido de la ventana principal
    configure_b = Button(main_window, text="configure", font=("Arial", 12), bg="#49B8A9", fg="#FFFFFF", width=12, command=configure)
    configure_b.place(x=500, y=90)

    #Boton transfer
    transfer_b= Button(main_window, text="transfer", font=("Arial", 12), bg="#49B8A9", fg="#FFFFFF", width=12, command=transfer)
    transfer_b.place(x=650, y=90)

    #Boton create
    create_b = Button(main_window, text="create", font=("Arial", 12), bg="#49B8A9", fg="#FFFFFF", width=12, command=create)
    create_b.place(x=500, y=110+espaciado)

    #Boton rename
    rename_b= Button(main_window, text="rename", font=("Arial", 12), bg="#49B8A9", fg="#FFFFFF", width=12, command=rename)
    rename_b.place(x=650, y=110+espaciado)

    #Boton delete
    delete_b= Button(main_window, text="delete", font=("Arial", 12), bg="#49B8A9", fg="#FFFFFF", width=12, command=delete)
    delete_b.place(x=500, y=130+espaciado*2)

    #Boton modify
    modify_b= Button(main_window, text="modify", font=("Arial", 12), bg="#49B8A9", fg="#FFFFFF", width=12, command=modify)
    modify_b.place(x=650, y=130+espaciado*2)

    #Boton copy
    copy_b= Button(main_window, text="copy", font=("Arial", 12), bg="#49B8A9", fg="#FFFFFF", width=12, command=copy)
    copy_b.place(x=500, y=150+ espaciado*3)

    #Boton add
    add_b = Button(main_window, text="add", font=("Arial", 12), bg="#49B8A9", fg="#FFFFFF", width=12, command=add)
    add_b.place(x=650, y=150+espaciado*3)

    #Boton backup
    backup_b= Button(main_window, text="backup", font=("Arial", 12), bg="#49B8A9", fg="#FFFFFF", width=12, command=backup)
    backup_b.place(x=500, y=170+espaciado*4)

    #Boton execu
    execu_b= Button(main_window, text="exec", font=("Arial", 12), bg="#49B8A9", fg="#FFFFFF", width=12, command=execu)
    execu_b.place(x=650, y=170+espaciado*4)

    #Boton cerrar sesion
    cerrars_b= Button(main_window, text="Cerrar Sesión", font=("Arial", 12), bg="#49B8A9", fg="#FFFFFF", width=12, command=close_main_window)
    cerrars_b.place(x=500, y=190+espaciado*5)

    enter_b= Button(main_window, text="enter", font=("Arial", 12), bg="#49B8A9", fg="#FFFFFF", width=12, command=enter)
    enter_b.place(x=650, y=190+espaciado*5)


    file_lock = threading.Lock()

    def read_file(filename):
        with file_lock:
            with open(filename, 'r') as file:
                content = file.read()
        return content

    def update_console_text(console_text, content):
        console_text.delete('1.0', tk.END)
        console_text.insert(tk.END, content)

    def check_file_changes():
        last_modified = None

        while True:
            current_modified = time.ctime(os.path.getmtime('app/log/consola.txt'))
            if current_modified != last_modified:
                content = read_file('app/log/consola.txt')
                update_console_text(console_txt, content)
                last_modified = current_modified
            time.sleep(1.5)

    def start_file_observer():
        file_observer = threading.Thread(target=check_file_changes)
        file_observer.daemon = True
        file_observer.start()

    def clear_console_file():
        with file_lock:
            with open('app/log/consola.txt', 'w') as file:
                file.write('')

    clear_console_file()

    console_txt2 = Text(main_window, width=70, height=22, font=("Arial", 8))
    console_txt2.place(x=40, y=90)

    console_txt = Text(main_window, width=120, height=12, font=("Arial", 8))
    console_txt.place(x=40, y=440)


    filename = 'app/log/consola.txt'  
    content = read_file(filename)

    start_file_observer()


    def eliminarConsola():
        archivo = 'app/log/Consola.txt'     
        try:
            with open(archivo, 'w') as archivo_consola:
                archivo_consola.write('')
                      
        except FileNotFoundError:
            print(f'El archivo {archivo} no existe.')

    

def show_login():
    # Mostrar la ventana de inicio de sesión
    root.deiconify()


root = Tk()
root.geometry("540x440")
root.resizable(False, False)
root.title("Login")

# Cargando la imagen de fondo de la ventana de inicio de sesión
img_path = os.path.join(os.path.dirname(__file__), "images/login.png")
bg_img = Image.open(img_path)
image = ImageTk.PhotoImage(bg_img)


canvas = Canvas(root, width=540, height=440, bg="#FFFFFF")
canvas.pack()


canvas.create_image(0, 0, image=image, anchor=NW)
canvas.image = image  

# Creando los widgets
username_entry = Entry(root, font=("Arial", 12), bg="#FFFFFF", width=20)
username_entry.place(x=190, y=150)

password_entry = Entry(root, show="*", font=("Arial", 12), bg="#FFFFFF", width=20)
password_entry.place(x=190, y=185)

login_button = Button(root, text="Ingresar", font=("Arial", 14), bg="#49B8A9", fg="#FFFFFF", width=10, command=login)
login_button.place(x=200, y=270)

# Cerrar la ventana principal al hacer clic en la "X"
root.protocol("WM_DELETE_WINDOW", root.quit)

root.mainloop()