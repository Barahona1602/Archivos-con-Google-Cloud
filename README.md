# AIM_Proyecto1


# Crear y correr un entorno virtual
*Este entorno virtual es dependiente de tu computadora, acá van
a estar todas las librerías que necesites para correr el proyecto*

*Activar primero el entorno virtual antes de correr el proyecto e instalar librerias*

```
# Crear entorno virtual
python3 -m venv venv

# Linux
source venv/bin/activate

# Windows
venv\Scripts\activate

# Desactivar entorno virtual
deactivate

# Generar archivo de requerimientos
pip freeze > requirements.txt

# Instalar requerimientos
pip install -r requirements.txt


```

# Comandos de git 
*Estos comandos son para subir los cambios que hagas en tu computadora*

## Hacer git clone
```
git clone "link del repositorio"
```

## Hacer git pull
*Este comando es para actualizar tu repositorio local con los cambios que se hayan hecho en el repositorio remoto*
```
git pull
```

## Crear una rama
*Este comando es para crear una rama, es importante que le pongas un nombre descriptivo*
```
git checkout -b "nombre de la rama"
```

## Cambiar de rama
*Este comando es para cambiar de rama, es importante que le pongas un nombre descriptivo*
```
git checkout "nombre de la rama"
```

## Merge
*Este comando es para unir dos ramas, es importante que estés en la rama que quieres unir*
```
git merge "nombre de la rama"
```

## Agregar cambios
*Este comando es para agregar los cambios que hiciste en tu computadora*
```
git add .
```

## Hacer commit
*Este comando es para hacer commit de los cambios que agregaste*
```
git commit -m "mensaje descriptivo"
```

## Hacer push
*Este comando es para subir los cambios que hiciste en tu computadora*
```
# Rama main
git push

# Otra rama
git push origin "nombre de la rama"
```