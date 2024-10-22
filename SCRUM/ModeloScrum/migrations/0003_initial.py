# Generated by Django 4.2 on 2024-10-22 23:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ModeloScrum', '0002_remove_sprint_backlog_sprint_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('objetivo', models.TextField()),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('velocidad', models.IntegerField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tarea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('descripcion', models.TextField(blank=True)),
                ('criterios_aceptacion', models.TextField()),
                ('prioridad', models.IntegerField()),
                ('estado', models.CharField(choices=[('POR_HACER', 'Por Hacer'), ('EN_PROGRESO', 'En Progreso'), ('COMPLETADA', 'Completada')], default='POR_HACER', max_length=12)),
                ('esfuerzo_estimado', models.IntegerField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('bloqueadores', models.TextField(null=True)),
                ('dependencias', models.ManyToManyField(blank=True, to='ModeloScrum.tarea')),
                ('responsable', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('sprint_asignado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ModeloScrum.sprint')),
            ],
        ),
        migrations.AddField(
            model_name='sprint',
            name='backlog_sprint',
            field=models.ManyToManyField(blank=True, related_name='backlogs', to='ModeloScrum.tarea'),
        ),
        migrations.AddField(
            model_name='sprint',
            name='equipo_desarrollo',
            field=models.ManyToManyField(blank=True, related_name='sprints_equipo', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sprint',
            name='scrum_master',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Epica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.TextField(blank=True)),
                ('criterios_aceptacion', models.TextField()),
                ('estado', models.CharField(choices=[('POR_HACER', 'Por Hacer'), ('EN_PROGRESO', 'En Progreso'), ('COMPLETADA', 'Completada')], default='POR_HACER', max_length=12)),
                ('esfuerzo_estimado_total', models.IntegerField()),
                ('fecha_inicio', models.DateField(blank=True)),
                ('fecha_fin', models.DateField(blank=True)),
                ('progreso', models.FloatField()),
                ('dependencias', models.ManyToManyField(blank=True, to='ModeloScrum.epica')),
                ('responsable', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('tareas_asociadas', models.ManyToManyField(to='ModeloScrum.tarea')),
            ],
        ),
        migrations.AddConstraint(
            model_name='tarea',
            constraint=models.CheckConstraint(check=models.Q(('prioridad__gte', 0)), name='prioridad_no_negativa'),
        ),
        migrations.AddConstraint(
            model_name='tarea',
            constraint=models.CheckConstraint(check=models.Q(('esfuerzo_estimado__gte', 0)), name='esfuerzo_estimado_no_negativo'),
        ),
        migrations.AddConstraint(
            model_name='tarea',
            constraint=models.CheckConstraint(check=models.Q(('estado__in', ['POR_HACER', 'EN_PROGRESO', 'COMPLETADA'])), name='estado_valido_tarea'),
        ),
        migrations.AddConstraint(
            model_name='sprint',
            constraint=models.CheckConstraint(check=models.Q(('fecha_fin__gte', models.F('fecha_inicio'))), name='fecha_fin_posterior'),
        ),
        migrations.AddConstraint(
            model_name='sprint',
            constraint=models.CheckConstraint(check=models.Q(('velocidad__gte', 0)), name='velocidad_no_negativa'),
        ),
        migrations.AddConstraint(
            model_name='epica',
            constraint=models.CheckConstraint(check=models.Q(('esfuerzo_estimado_total__gte', 0)), name='esfuerzo_total_no_negativo'),
        ),
        migrations.AddConstraint(
            model_name='epica',
            constraint=models.CheckConstraint(check=models.Q(('progreso__gte', 0), ('progreso__lte', 1)), name='progreso_valido'),
        ),
        migrations.AddConstraint(
            model_name='epica',
            constraint=models.CheckConstraint(check=models.Q(('estado__in', ['POR_HACER', 'EN_PROGRESO', 'COMPLETADA'])), name='estado_valido_epica'),
        ),
        migrations.AddConstraint(
            model_name='epica',
            constraint=models.CheckConstraint(check=models.Q(('fecha_fin__gte', models.F('fecha_inicio'))), name='fecha_fin_posterior_epica'),
        ),
    ]
