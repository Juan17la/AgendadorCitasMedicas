from django.db import models
from apps.users.models import User
from django.utils import timezone
from datetime import datetime, timedelta

# MODELOS BÁSICOS 

class Especialidad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor')
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE, related_name='doctores')
    consultorio = models.CharField(max_length=100)

    def __str__(self):
        return f'Dr. {self.user.nombres} {self.user.apellidos}'


# SISTEMA DE HORARIOS 

class JornadaDiaria(models.Model):
    DIAS_SEMANA = [
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    ]
    dia = models.CharField(max_length=10, choices=DIAS_SEMANA)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    duracion_bloque = models.IntegerField(default=20)  # minutos

    def __str__(self):
        return f"{self.dia.title()} {self.hora_inicio}-{self.hora_fin} ({self.duracion_bloque}min)"


class HorarioSemanal(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='horarios_semanales')
    inicio_horario = models.DateField()
    jornadas = models.ManyToManyField(JornadaDiaria)

    def __str__(self):
        return f"Horario desde {self.inicio_horario} para {self.doctor}"


class BloqueHorario(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='bloques_horarios')
    jornada = models.ForeignKey(JornadaDiaria, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    disponible = models.BooleanField(default=True)

    def __str__(self):
        estado = "Libre" if self.disponible else "Ocupado"
        return f"{self.fecha} {self.hora_inicio}-{self.hora_fin} ({estado})"


#  CITAS 

class Cita(models.Model):
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE, related_name='citas', null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='citas')
    paciente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='citas')
    bloque = models.OneToOneField(BloqueHorario, on_delete=models.CASCADE, null=True, related_name='cita')
    motivo = models.TextField(max_length=2000)
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada')
    ], default='pendiente')

    @property
    def fecha_hora(self):
        return datetime.combine(self.bloque.fecha, self.bloque.hora_inicio)

    @property
    def dia_fecha_cita(self):
        return self.bloque.fecha.day

    @property
    def mes_fecha_cita(self):
        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        return meses[self.bloque.fecha.month - 1]

    @property
    def hora_cita(self):
        return self.bloque.hora_inicio.strftime("%H:%M")

    @property
    def dias_restantes(self):
        return (datetime.combine(self.bloque.fecha, self.bloque.hora_inicio) - timezone.now()).days

    def __str__(self):
        return f'Cita de {self.paciente.nombres} con Dr. {self.doctor.user.apellidos} el {self.fecha_hora.strftime("%d-%m-%Y %H:%M")}'


class CitaConfirmada(models.Model):
    cita = models.OneToOneField(Cita, on_delete=models.CASCADE, related_name='cita_confirmada')
    fecha_hora_confirmada = models.DateTimeField()
    receta = models.TextField(max_length=2000, blank=True, null=True)
    observaciones = models.TextField(max_length=2000, blank=True, null=True)
    remision = models.TextField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return f'Cita confirmada: {self.cita} - {self.fecha_hora_confirmada.strftime("%d-%m-%Y %H:%M")}'
