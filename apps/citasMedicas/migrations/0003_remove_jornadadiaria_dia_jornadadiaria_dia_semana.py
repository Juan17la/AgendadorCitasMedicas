# Generated by Django 5.1.6 on 2025-05-10 20:59

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citasMedicas', '0002_jornadadiaria_remove_cita_fecha_hora_bloquehorario_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jornadadiaria',
            name='dia',
        ),
        migrations.AddField(
            model_name='jornadadiaria',
            name='dia_semana',
            field=models.IntegerField(choices=[(0, 'Lunes'), (1, 'Martes'), (2, 'Miércoles'), (3, 'Jueves'), (4, 'Viernes'), (5, 'Sábado'), (6, 'Domingo')], default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
