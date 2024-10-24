# Proyecto SCRUM
Es una aplicación basada en la metodología SCRUM para gestionar proyectos, con modelos construidos en Django que se relacionan entre sí para reflejar el funcionamiento de esta metodología ágil. Consta de 3 modelos principales: Tarea, Epica y Sprint, los cuales interactuan a su vez con el modelo de usuario que propociona por defecto Django. No cuenta con vistas, pues su uso se limita a realizar consultas con el Shell. 

## Instalación
1. Clonar el repositorio.
   Utilizando el siguiente link, puede clonarse desde Visual Studio Code y colocarse en la carpeta de preferencia:
   https://github.com/Bruno1571/Scrum.git

3. Crear y activar el entorno virtual.
   Dentro de la carpeta que se creará el Entorno Virtual se ejecuta el siguiente comando:
   python -m venv env
   Estando dentro de la carpeta, para activarlo hay que ejecutar:
   En Linux: source env/bin/activate
   En Windows: env\Scripts\activate

5. Instalar las dependencias.
   Para instalar las dependecias uno debe estar parado en la carpeta SCRUM, que es donde se encuentra el archivo requirements.txt:
   pip install -r requirements.txt

7. Aplicar las migraciones de la base de datos.
   El comando migrate aplicará las migraciones a la base de datos local, creando las tablas necesarias para que el proyecto funcione correctamente:
   python manage.py migrate

## Consultas
A continuación se muestran algunos de los comandos que pueden ser utilizados para consultar los datos almacenados en la base de datos.
Primero hay que ejecutar el comando python manage.py Shell para así abrir el Shell de Django. U
Una vez hecho, antes de pasar a las consultas, hay que importar las constantes y los modelos como están a continuación:

from ModeloScrum.models import Sprint, Tarea, Epica, POR_HACER, EN_PROGRESO, COMPLETADA
from django.contrib.auth.models import User
from django.db.models import Count

1. Obtener todas las tareas asignadas a un usuario específico. 
usuario = User.objects.get(id=usuario_id)  # Cambia 'usuario_id' por el ID real del usuario
tareas_asignadas = Tarea.objects.filter(responsable=usuario)
print(tareas_asignadas)

2. Obtener las tareas completadas dentro de un sprint determinado.
sprint = Sprint.objects.get(id=sprint_id)  # Cambia 'sprint_id' por el ID real del sprint
tareas_completadas = Tarea.objects.filter(sprint_asignado=sprint, estado=COMPLETADA)
print(tareas_completadas)

3. Listar todas las tareas que dependen de una tarea específica.
tarea = Tarea.objects.get(id=tarea_id)  # Cambia 'tarea_id' por el ID real de la tarea
tareas_dependientes = tarea.dependencias.all()
print(tareas_dependientes)

4. Listar todas las épicas que tienen tareas en progreso. 
epicas_en_progreso = Epica.objects.filter(tareas_asociadas__estado=EN_PROGRESO).distinct()
print(epicas_en_progreso)

5. Calcular el número total de tareas por estado (por hacer, en progreso,completada).
total_por_estado = Tarea.objects.values('estado').annotate(total=Count('estado'))
print(total_por_estado)

6. Obtener la suma de esfuerzo estimado de todas las tareas asociadas a una épica específica.
epica = Epica.objects.get(id=epica_id)  # Cambia 'epica_id' por el ID real de la épica
esfuerzo_total = epica.tareas_asociadas.aggregate(total_esfuerzo=models.Sum('esfuerzo_estimado'))
print(esfuerzo_total)

7. Listar los sprints que tiene un Scrum Master asignado.
sprints_con_scrum_master = Sprint.objects.exclude(scrum_master__isnull=True)
print(sprints_con_scrum_master)

8. Obtener el progreso total de una épica en base a las tareas completadas.
epica = Epica.objects.get(id=epica_id)  # Cambia 'epica_id' por el ID real de la épica
total_tareas = epica.tareas_asociadas.count()
tareas_completadas = epica.tareas_asociadas.filter(estado=COMPLETADA).count()
progreso_total = (tareas_completadas / total_tareas) * 100 if total_tareas > 0 else 0
print(f"El progreso total de la epica elegida es: {progreso_total}%")

9. Obtener el backlog de un sprint específico y sus responsables. 
sprint = Sprint.objects.get(id=sprint_id)  # Cambia 'sprint_id' por el ID real del sprint
backlog = sprint.backlog_sprint.all().select_related('responsable')
for tarea in backlog:
    print(f"Tarea: {tarea.titulo}, Responsable: {tarea.responsable.username if tarea.responsable else 'No asignado'}")

10. Listar todas las tareas que están bloqueadas.
tareas_bloqueadas = Tarea.objects.exclude(bloqueadores__isnull=True).exclude(bloqueadores__exact='')
print(tareas_bloqueadas)

## Requisitos
Python 3.12.5, Django 4.2 y SQLlite (u otra base de datos compatible).
