from django.db import models
from django.contrib.auth.models import User

POR_HACER = 'POR_HACER'
EN_PROGRESO = 'EN_PROGRESO'
COMPLETADA = 'COMPLETADA'

class Tarea(models.Model):

    ESTADO_CHOICES = [
        (POR_HACER, 'Por Hacer'),
        (EN_PROGRESO, 'En Progreso'),
        (COMPLETADA, 'Completada'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    criterios_aceptacion = models.TextField()
    prioridad = models.IntegerField()
    
    estado = models.CharField(
        max_length=12,
        choices=ESTADO_CHOICES, 
        default=POR_HACER,
    )
    
    esfuerzo_estimado = models.IntegerField()
    
    responsable = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )
    
    sprint_asignado = models.ForeignKey(
        'Sprint',
        on_delete=models.SET_NULL,
        null=True
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    dependencias = models.ManyToManyField('self', blank=True, symmetrical=False)
    
    bloqueadores = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(prioridad__gte=0), name="prioridad_no_negativa"),
            models.CheckConstraint(check=models.Q(esfuerzo_estimado__gte=0), name="esfuerzo_estimado_no_negativo"),
            models.CheckConstraint(check=models.Q(estado__in=[POR_HACER, EN_PROGRESO, COMPLETADA]), name="estado_valido_tarea"),
        ]

    def __str__(self):
        return self.titulo

#MODELO EPICA

class Epica(models.Model):

    ESTADO_CHOICES = [
        (POR_HACER, 'Por Hacer'),
        (EN_PROGRESO, 'En Progreso'),
        (COMPLETADA, 'Completada'),
    ]

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    criterios_aceptacion = models.TextField()
    
    estado = models.CharField(
        max_length=12,
        choices=ESTADO_CHOICES,
        default=POR_HACER,
    )
    
    responsable = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )
    
    tareas_asociadas = models.ManyToManyField('Tarea')
    
    esfuerzo_estimado_total = models.IntegerField()
   
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True)
    
    progreso = models.FloatField()
    
    dependencias = models.ManyToManyField('self', blank=True, symmetrical=False)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(esfuerzo_estimado_total__gte=0), name="esfuerzo_total_no_negativo"),
            models.CheckConstraint(check=models.Q(progreso__gte=0, progreso__lte=1), name="progreso_valido"),
            models.CheckConstraint(check=models.Q(estado__in=[POR_HACER, EN_PROGRESO, COMPLETADA]), name="estado_valido_epica"),
            models.CheckConstraint(check=models.Q(fecha_fin__gte=models.F('fecha_inicio')), name="fecha_fin_posterior_epica"),
        ]

    def __str__(self):
        return self.nombre

#MODELO SPRINT

class Sprint(models.Model):
    nombre = models.CharField(max_length=200)
    objetivo = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    
    velocidad = models.IntegerField()
    
    scrum_master = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )
    
    equipo_desarrollo = models.ManyToManyField(User, related_name='sprints_equipo')
    backlog_sprint = models.ManyToManyField('Tarea',  related_name='backlogs')
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(fecha_fin__gte=models.F('fecha_inicio')), name="fecha_fin_posterior"),
            models.CheckConstraint(check=models.Q(velocidad__gte=0), name="velocidad_no_negativa"),
        ]

    def __str__(self):
        return self.nombre
