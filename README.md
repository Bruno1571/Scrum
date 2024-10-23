Cree el readme para ver si se ejecutaron los cambios


PASOS

## Ejecutar el script
python .\generar_datos_prueba.py

## Abrir shell
python manage.py Shell

## Consultar
from ModeloScrum.models import User, Sprint, Epica, Tarea 		(ESTE PRIMERO PARA IMPORTAR LOS MODELOS)

print(User.objects.count())  # Cantidad de usuarios
print(Sprint.objects.count())  # Cantidad de sprints
print(Epica.objects.count())  # Cantidad de épicas
print(Tarea.objects.count())  # Cantidad de tareas

## Eliminar
User.objects.all().delete()
Sprint.objects.all().delete()
Epica.objects.all().delete()
Tarea.objects.all().delete()
