from scanner.scanner import scan_command_line_create, scan_command_line_backup, scan_command_line_configure,scan_command_line_delete,scan_command_line_copy, scan_command_line_transfer, scan_command_line_rename, scan_command_line_modify, scan_command_line_add, scan_command_line_exec
from scanner.tokens import extract_commands
from cloud.createStorage import create_cloud
from cloud.deleteStorage import delete_cloud
from cloud.copyStorage import copy_cloud
from cloud.transferStorage import transfer_cloud
from cloud.renameStorage import rename_cloud
from cloud.modifyStorage import modify_cloud
from cloud.addStorage import add_cloud
from encriptado import decrypt
def main():
  # Define a command line string
  command_string = '''
configure -type->local -encrypt_log->false -encrypt_read->false
create -name->prueba1.txt  -path->/carpeta1/ -body->"Este es el contenido del archivo1"
create -name->prueba2.txt  -path->/carpeta1/ -body->"Este es el contenido del archivo2"
create -name->prueba1.txt  -path->/"Carpeta Ejemplo"/ -body->"Un sistema de archivos es una estructura de directorios completa, que incluye un directorio raíz y cualquier subdirectorio y archivos por debajo suyo"
create -name->prueba2.txt  -path->/"Carpeta Ejemplo"/ -body->"hola"
create -name->prueba3.txt  -path->/"Carpeta Ejemplo"/ -body->"Se trata de habilitar uno o varios discos duros en una red local, de forma que los datos que allí se almacenen permanezcan accesibles a todos los dispositivos que quieran utilizarlos"
rename -path->/carpeta1/prueba1.txt -name->nuevo_nombre1.txt
rename -path->/carpeta1/prueba1.txt -name->nuevo_nombre2.txt
rename -path->/carpeta1/prueba2.txt -name->nuevo_nombre2.txt
copy -from->/carpeta1/nuevo_nombre1.txt -to->/"Carpeta Ejemplo"/
transfer -from->/carpeta1/ -to->/"Carpeta Ejemplo"/ -mode->"local"
transfer -from->/carpeta1/nuevo_nombre2.txt -to->/"Carpeta Ejemplo"/ -mode->"local"
delete -path->/carpeta1/prueba2.txt
delete -path->/"Carpeta Ejemplo"/prueba3.txt
modify -path->/"Carpeta Ejemplo"/nuevo_nombre1.txt -body->"Se trata de habilitar uno o varios discos duros en una red local, de forma que los datos que allí se almacenen permanezcan accesibles a todos los dispositivos que quieran utilizarlos"
backup
add -path->/"Carpeta Ejemplo"/nuevo_nombre1.txt  -body->"De esa forma, el usuario no solo tiene acceso al propio almacenamiento del dispositivo que está usando, sino que también dispone de un almacenamiento común que comparte con otros dispositivos conectados a esa misma red."
create -name->prueba4.txt  -path->/carpeta1/ejemplo/ -body->"Este es el contenido del archivo4"
create -name->prueba5.txt  -path->/carpeta1/ejemplo/ -body->"Este es el contenido del archivo5"
  '''
  # configure -type->local -encrypt_log->true -encrypt_read->true -llave->miaproyecto12345
  # configure -type->local -encrypt_log->falsE -encrypt_read->false -llave->"hola123" 
  commad_crypted = '''
  configure -type->local -encrypt_log->true -encrypt_read->true -llave->miaproyecto12345
  405AF6813A5E62DC3875DC69AE4D3EC89C9B9E111D79CDFB4647EA4A2E5984A645641D4339D7668D9D6BC81BAAE1D658A8F38B1216878F0F13CF9C1E17356DAF408A68E3B4C61E2938863D0F7CCD5A5C1DBF166FDB03E2EF2DF4817600DF989FBB0405DDF131757DF46363A912151D21B211B3D439B98963B0DE7FC369D199F9E7E19538049B2323AF1F99A1172218A1A8F38B1216878F0F13CF9C1E17356DAF408A68E3B4C61E2938863D0F7CCD5A5C83E217A53FFC6244BF53183FEE3E67AAE584F64EFE64ED2483578CDCDB600D44DCB93A1CD90671068A22BFCFB2DAD3CA02944CA4B2668B9501E80DDAB09F598B02677B5D30BA63F5472BFF9DA73132FB394B018AC139C49E51C275043CD7B21485DEAB471E33279ECEF67B322F5A4F9FE1FCFD63B4878CE6342E0EAA2945C4FF2D1C0959FEC97373CC234C4B2DEFE2DE51E1B5791621EDE9F8127F7ECC9FCFA7AA4BBF35DA824770052873F61A77FF1D2835FC7EADB8004563AD7D8FC76F2081F943EA27CF2630793C4DAC59E1FDF2F344D0961883B334A26B91DA41162FB2107B9920185E542F2D40863DDC56093BEB90271BA1B08A45D22EB2554CF99D5226F754B5C6A71945F89EDC68520B61AC50C3CD56DFB04C94BC84CD7FA96D1D29FFCD292FECFCC7D96D991F55B9F726A7D6F753064C0FBAA3E073FA47517600FE35C71F8A5E16505573CBF76A425B9FCAA4E5B97E6AA901ED9C040A77A2F847CA325B38529AE74BEA89856BBDC0E13E6E30243DA23C2A5E8987ACF2DA98A02107DD35580924DCCAB2E80DBC57272703C8A9CC61E5B0C8BBB7CC4E696CC79106C66863C75FBF0CE7FD82486D398AFE2B99E8F2C27F924A0EC20B1407F358D9B0A6A83C86FC49F97D63EF714133EC5682B9620DD7667C91C0F94B9F8F9BADE4349621EBA743CCBB38A87C5D3A0249150165AD21AB56BE9DA7BA4717E49C8E250AE725EC6FC0D2E17E086866EA9903902577824ADA0505592334064E6FDFE68338C38AB1301B35D41CB7880962D48F64B0269039771FF9EF859E36D145A3E2A3D80954BF6F28EDCB0EEF906F453000B864ABDC045C5CD67A467154BFC255D412878615F47CCEC007A241815744B002223515C1AB9260046A08978EF672585F8B65BAB4731FFAAEEC601C6229908F5F996E280BC1B9DD63E01A28143268E6A1278D379B649F0E94AE8988735001AB431A3A2FDBE69DAB88150661F6F2B364A51CFBCC67A50A5093E69911D99BA99B4882AB72EEA587C547AFA3F605E411F37B34B3AC3FE188B2FDE176C97C549B883D582983FA256F4FF731F13E880EE6F9D5D4BCE2FD
  '''
  command = extract_commands(commad_crypted)
  print(command)
  if command[0] != None and command[1] == ""  :
    print("Viene configure y no viene encriptado")
  elif command[0] != None and command[1] != None :
    print("Viene configure y encriptado")
    configure, type, encrypt_log, encrypt_read, key = scan_command_line_configure(command[0])
    print(f"Command Configure:")
    print(f"Configure: {configure}")
    print(f"Type: {type}")
    print(f"Encrypt Log: {encrypt_log}")
    print(f"Encrypt Read: {encrypt_read}")
    print(f"Key: {key}\n")
  
  elif command[0] == None and command[1] != None:
    print("Viene encriptado y no viene configure")

  return

  # return 
  # message_decrypted = decrypt(message_crypted, "miaproyecto12345")
  # print(result_crypted, message_crypted)
  # print(message_decrypted)
  # list_commands = extract_commands(message_decrypted)
  # for l in list_commands:
  #   print(l)

  # return







  # commond 
  result = extract_commands(command_string)
  for token in result[0]:
    print(token)
    if(token.get("configure")):
      configure, type, encrypt_log, encrypt_read, key = scan_command_line_configure(token.get("configure"))
      print(f"Command Configure:")
      print(f"Configure: {configure}")
      print(f"Type: {type}")
      print(f"Encrypt Log: {encrypt_log}")
      print(f"Encrypt Read: {encrypt_read}")
      print(f"Key: {key}\n")
    elif(token.get("create")):
      create, name, path, body = scan_command_line_create(token.get("create"))
      print(f"Command Line Create:")
      print(f"Create: {create}")
      print(f"Name: {name}")
      print(f"Path: {path}")
      print(f"Body: {body}\n")
      # create the file in the cloud
      #delete the last character of the path 
      # create_cloud(file_data=body, destination_blob_name=path, name=name) 

    elif(token.get("delete")):
      delete, path, name = scan_command_line_delete(token.get("delete"))
      print(f"Command Delete:")
      print(f"Delete: {delete}")
      print(f"Path: {path}")
      print(f"Name: {name}\n")
      # delete_cloud(blob_name=path, name=name)
    elif(token.get("copy")):
      copy, from_path, to_path = scan_command_line_copy(token.get("copy"))
      print(f"Command Copy:")
      print(f"Copy: {copy}")
      print(f"From: {from_path}")
      print(f"To: {to_path}\n")
      # copy_cloud(blob_name=from_path, destination_blob_name=to_path)
    elif(token.get("transfer")):
      transfer, from_path, to_path, mode = scan_command_line_transfer(token.get("transfer"))
      print(f"Command Transfer:")
      print(f"Transfer: {transfer}")
      print(f"From: {from_path}")
      print(f"ARCHIVOS{from_path}")
      print(f"To: {to_path}")
      print(f"ARCHIVOS{to_path}")
      print(f"Mode: {mode}\n")
      # transfer_cloud(from_path,to_path)

    elif(token.get("rename")):
      rename, path, name = scan_command_line_rename(token.get("rename"))
      print(f"Command Rename:")
      print(f"Rename: {rename}")
      print(f"Path: {path}")
      print(f"Name: {name}\n")
      # rename_cloud(blob_name=path, new_name=name)
    elif(token.get("modify")):
      modify, path, body = scan_command_line_modify(token.get("modify"))
      print(f"Command Modify:")
      print(f"Modify: {modify}")
      print(f"Path: {path}")
      print(f"Body: {body}\n")
      # modify_cloud(blob_name=path, new_content=body)
    elif(token.get("add")):
      add, path, body = scan_command_line_add(token.get("add"))
      print(f"Command Add:")
      print(f"Add: {add}")
      print(f"Path: {path}")
      print(f"Body: {body}\n")
      # add_cloud(blob_name=path, additional_content=body)

    elif(token.get("exec")):
      exec, path = scan_command_line_exec(token.get("exec"))
      print(f"Command Exec:")
      print(f"Exec: {exec}")
      print(f"Path: {path}\n")

    elif(token.get("backup")):
      backup = scan_command_line_backup(token.get("backup"))
      print(f"Command Backup:")
      print(f"Backup: {backup}")
      
    

  command_configure = 'Configure -type->local -encrypt_log->false -encrypt_read->false'
  command_line_create1 = 'create -name->prueba1.txt -path->/carpeta1/ -body->"Este es el contenido del archivo 1"'
  command_line_create2 = 'create -namE->"prueba 2.txt" -path->/"carpeta 2"/ -boDy->"Este es el contenido del archivo 2"'
  command_line_delete1 = 'delete -path->/carpeta1/ -name->prueba1.txt'
  command_line_delete2 = 'delete -path->/"carpeta 2"/ '
  command_line_copy1 = 'Copy -from->/carpeta1/prueba1.txt -to->/"carpeta 2"/'
  command_line_copy2 = 'Copy -from->/"carpeta 2"/ -to->/carpeta1/'
  command_line_transfer1 = 'transfer -from->/carpeta1/prueba1.txt -to->/"carpeta 2"/ -mode->"local"'
  command_line_transfer2 = 'transfer -from->/"carpeta 2"/ -to->/carpeta1/ -mode->"cloud"'
  command_line_rename1 = 'renaMe -paTh->/"carpeta 2"/exampleSub1.txt -name->b1.txt'
  command_line_modify = 'modify -path->/"carpeta 2"/exampleSub1.txt -body->"este es el nuevo contenido del archivo"'
  command_line_add = 'add -path->/carpeta1/prueba1.txt -body->"este es el nuevo contenido del archivo"'
  command_line_exec = 'exec -path->/home/Desktop/miaejecutable.mia '
  # Scan the command line string
  # configure, type, encrypt_log, encrypt_read = scan_command_line_configure(command_configure)
  # create, name, path, body = scan_command_line_create(command_line_create1)
  # delete, path, name = scan_command_line_delete(command_line_delete1)
  # copy, from_path, to_path = scan_command_line_copy(command_line_copy2)
  # transfer, from_path, to_path, mode = scan_command_line_transfer(command_line_transfer2)
  # rename, path, name = scan_command_line_rename(command_line_rename1)
  # modify, path, body = scan_command_line_modify(command_line_modify)
  # add, path, body = scan_command_line_add(command_line_add)
  # exec, path = scan_command_line_exec(command_line_exec)
  # Print the extracted values

  # print(f"Command Exec:")
  # print(f"Exec: {exec}")
  # print(f"Path: {path}\n")


  # print(f"Command Add:")
  # print(f"Add: {add}")
  # print(f"Path: {path}")
  # print(f"Body: {body}\n")

  # print(f"Command Modify:")
  # print(f"Modify: {modify}")
  # print(f"Path: {path}")
  # print(f"Body: {body}\n")

  # print(f"Command Rename:")
  # print(f"Rename: {rename}")
  # print(f"Path: {path}")
  # print(f"Name: {name}\n")
  

  # print(f"Command Transfer:")
  # print(f"Transfer: {transfer}")
  # print(f"From: {from_path}")
  # print(f"To: {to_path}")
  # print(f"Mode: {mode}\n")

  # print(f"Command Copy:")
  # print(f"Copy: {copy}")
  # print(f"From: {from_path}")
  # print(f"To: {to_path}\n")

  # print(f"Command Delete:")
  # print(f"Delete: {delete}")
  # print(f"Path: {path}")
  # print(f"Name: {name}\n")

  # Print the extracted values
  # print(f"Command Configure:")
  # print(f"Configure: {configure}")
  # print(f"Type: {type}")
  # print(f"Encrypt Log: {encrypt_log}")
  # print(f"Encrypt Read: {encrypt_read} \n")

  # print(f"Command Line Create:")
  # print(f"Create: {create}")
  # print(f"Name: {name}")
  # print(f"Path: {path}")
  # print(f"Body: {body}\n")


  # print(f"\nCommand Line 2:")
  # print(f"Name: {name2}")
  # print(f"Path: {path2}")
  # print(f"Body: {body2}")

#   lexer.input(command_line1)
#   while True:
#       token = lexer.token()
#       if not token:
#           break
#       print(token)

#   lexer.input(command_line2)
#   while True:
#       token = lexer.token()
#       if not token:
#           break
#       print(token)


if __name__ == '__main__':
  main()
