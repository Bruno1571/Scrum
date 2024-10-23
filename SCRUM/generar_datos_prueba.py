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

# Función para crear sprints
def crear_sprints(usuarios, num_sprints=3):
    sprints = []
    for i in range(1, num_sprints + 1):
        sprint = Sprint.objects.create(
            nombre=f"Sprint {i}",
            objetivo=f"Objetivo del Sprint {i}",
            fecha_inicio=date.today() + timedelta(days=(i - 1) * 7),  # Cada sprint empieza una semana después
            fecha_fin=date.today() + timedelta(days=(i * 7)),
            velocidad=random.randint(5, 15),  
            scrum_master=random.choice(usuarios) 
        )
        sprints.append(sprint)
    print("Sprints creados.")
    return sprints

# Función para crear épicas
def crear_epicas(usuarios, num_epicas=5):
    epicas = []
    for i in range(1, num_epicas + 1):
        fecha_inicio = date.today()
        fecha_fin = fecha_inicio + timedelta(days=random.randint(7, 21))

        epica = Epica.objects.create(
            nombre=f"Épica {i}",
            descripcion=f"Descripción de la Épica {i}",
            criterios_aceptacion=f"Criterios de aceptación para Épica {i}",
            estado="POR_HACER" if i % 2 != 0 else "EN_PROGRESO",  # Alternar estado
            esfuerzo_estimado_total=random.randint(50, 150),
            responsable=random.choice(usuarios),  
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,  
            progreso=0.0
        )
        epicas.append(epica)
    print("Épicas creadas.")
    return epicas


# Función para crear tareas
def crear_tareas(usuarios, sprints, epicas, num_tareas=30):
    for i in range(1, num_tareas + 1):
        tarea = Tarea.objects.create(
            titulo=f"Tarea {i}",
            descripcion=f"Descripción de la Tarea {i}",
            criterios_aceptacion=f"Criterios de aceptación para Tarea {i}",
            prioridad=random.randint(1, 5),  # Prioridad aleatoria
            estado=POR_HACER if i % 3 != 0 else EN_PROGRESO,  # Alternar estado
            esfuerzo_estimado=random.randint(1, 10),
            responsable=random.choice(usuarios),  
            sprint_asignado=random.choice(sprints),  
        )
        
        # Asignar dependencias
        if i > 1:
            tarea.dependencias.add(Tarea.objects.get(titulo=f"Tarea {i-1}"))  # Tarea anterior como dependencia
            tarea.save()
        
        # Asignar tarea a una épica aleatoria
        epica = random.choice(epicas)
        epica.tareas_asociadas.add(tarea)
        epica.save()
        
    print("Tareas creadas.")

if __name__ == "__main__":
    usuarios = crear_usuarios()
    sprints = crear_sprints(usuarios)
    epicas = crear_epicas(usuarios)
    crear_tareas(usuarios, sprints, epicas)
