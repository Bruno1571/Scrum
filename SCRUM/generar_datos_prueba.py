import os
import django
from datetime import date, timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SCRUM.settings')
django.setup()

from ModeloScrum.models import Tarea, Epica, Sprint
from django.contrib.auth.models import User

POR_HACER = 'POR_HACER'
EN_PROGRESO = 'EN_PROGRESO'
COMPLETADA = 'COMPLETADA'

# Función para crear usuarios
def crear_usuarios(num_usuarios=10):
    usuarios = []
    for i in range(1, num_usuarios + 1):
        usuario = User.objects.create_user(username=f'user{i}', password='password1234')
        usuarios.append(usuario)
    print("Usuarios creados.")
    return usuarios

# Función para crear tareas
def crear_tareas(usuarios, num_tareas=30):
    tareas = []
    for i in range(1, num_tareas + 1):
        # Lógica para establecer el estado de la tarea
        if i <= 5:  # Solo las primeras 5 tareas serán 'COMPLETADA'
            estado = COMPLETADA
        else:
            estado = random.choice([POR_HACER, EN_PROGRESO])

        tarea = Tarea.objects.create(
            titulo=f"Tarea {i}",
            descripcion=f"Descripción de la Tarea {i}",
            criterios_aceptacion=f"Criterios de aceptación para Tarea {i}",
            prioridad=random.randint(1, 5),
            estado=estado,
            esfuerzo_estimado=random.randint(1, 10),
            responsable=random.choice(usuarios)
        )
        tareas.append(tarea)

        # Asignar dependencias aleatorias (si corresponde)
        if i > 2:  # Solo asignar dependencias a tareas que tienen un índice mayor a 2
            num_dependencias = random.randint(1, 2)
            dependencias = random.sample(tareas[:i-1], num_dependencias)
            for dep in dependencias:
                tarea.dependencias.add(dep)  
                
    print("Tareas creadas con dependencias.")
    return tareas

# Función para crear épicas
def crear_epicas(usuarios, tareas, num_epicas=3):
    epicas = []
    for i in range(1, num_epicas + 1):
        fecha_inicio = date.today()
        fecha_fin = fecha_inicio + timedelta(days=random.randint(7, 21))

        # Crear la épica
        epica = Epica.objects.create(
            nombre=f"Épica {i}",
            descripcion=f"Descripción de la Épica {i}",
            criterios_aceptacion=f"Criterios de aceptación para Épica {i}",
            estado=random.choice([POR_HACER, EN_PROGRESO]),
            esfuerzo_estimado_total=random.randint(50, 150),
            responsable=random.choice(usuarios),
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            progreso=0.0
        )

        # Asignar tareas a la épica
        tareas_asignadas = random.sample(tareas, random.randint(8, 10))  # 8-10 tareas por épica
        for tarea in tareas_asignadas:
            epica.tareas_asociadas.add(tarea)  # Asociar la tarea a la épica

        epicas.append(epica)

    # Configurar dependencias entre épicas
    if len(epicas) > 1:
        epicas[1].dependencias.add(epicas[0])  # Épica 2 depende de Épica 1
    if len(epicas) > 2:
        epicas[2].dependencias.add(random.choice(epicas[0:2]))  # Épica 3 depende de Épica 1 o Épica 2

    print("Épicas creadas y tareas asignadas a épicas.")
    return epicas

# Función para crear sprints y asignar tareas a los sprints
def crear_sprints(usuarios, tareas, num_sprints=6):
    sprints = []
    for i in range(1, num_sprints + 1):
        sprint = Sprint.objects.create(
            nombre=f"Sprint {i}",
            objetivo=f"Objetivo del Sprint {i}",
            fecha_inicio=date.today() + timedelta(days=(i - 1) * 7),
            fecha_fin=date.today() + timedelta(days=(i * 7)),
            velocidad=random.randint(5, 15),
            scrum_master=random.choice(usuarios)
        )

        # Asignar usuarios al equipo de desarrollo
        num_miembros_equipo = random.randint(3, 5)  # Elegir entre 3 y 5 miembros
        equipo_desarrollo = random.sample(usuarios, num_miembros_equipo)
        sprint.equipo_desarrollo.set(equipo_desarrollo)  # Asignar miembros al equipo de desarrollo

        # Asignar algunas tareas al sprint (pueden ser de las tareas creadas)
        tareas_asignadas = random.sample(tareas, random.randint(5, 10))
        for tarea in tareas_asignadas:
            tarea.sprint_asignado = sprint
            tarea.save()
            sprint.backlog_sprint.add(tarea)

        sprint.save()
        sprints.append(sprint)

    print("Sprints creados y tareas asignadas a los sprints.")
    return sprints

if __name__ == "__main__":
    # Crear usuarios
    usuarios = crear_usuarios()

    # Crear tareas
    tareas = crear_tareas(usuarios)

    # Crear épicas y asignarles tareas
    epicas = crear_epicas(usuarios, tareas)

    # Crear sprints y asignarles tareas
    sprints = crear_sprints(usuarios, tareas)
