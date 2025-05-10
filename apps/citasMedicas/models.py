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
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]
    dia_semana = models.IntegerField(choices=DIAS_SEMANA)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    duracion_bloque = models.IntegerField(default=20)  # minutos

    def __str__(self):
        return f"{self.get_dia_semana_display()} {self.hora_inicio}-{self.hora_fin}"

    def generar_bloques(self, fecha, doctor):
        """
        Genera bloques horarios para una fecha específica
        Solo genera bloques si el día de la semana coincide y la fecha es futura
        """
        from datetime import datetime, timedelta

        # Solo generar si el día de la semana coincide
        if fecha.weekday() != self.dia_semana:
            return []

        bloques = []
        hora_actual = datetime.combine(fecha, self.hora_inicio)
        hora_fin = datetime.combine(fecha, self.hora_fin)

        while hora_actual + timedelta(minutes=self.duracion_bloque) <= hora_fin:
            # Verificar si ya existe un bloque para esta hora
            bloque, creado = BloqueHorario.objects.get_or_create(
                doctor=doctor,
                jornada=self,
                fecha=fecha,
                hora_inicio=hora_actual.time(),
                hora_fin=(hora_actual + timedelta(minutes=self.duracion_bloque)).time(),
                defaults={'disponible': True}
            )
            if bloque.disponible:  # Solo incluir bloques disponibles
                bloques.append(bloque)
            hora_actual += timedelta(minutes=self.duracion_bloque)

        return bloques


class HorarioSemanal(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='horarios_semanales')
    inicio_horario = models.DateField()
    jornadas = models.ManyToManyField(JornadaDiaria)

    def __str__(self):
        return f"Horario desde {self.inicio_horario} para {self.doctor}"
    
    def generar_bloques_rango(self, fecha_inicio, fecha_fin):
        """
        Genera bloques horarios para un rango de fechas, solo para días laborables
        """
        from datetime import timedelta
        bloques = []
        fecha_actual = fecha_inicio

        while fecha_actual <= fecha_fin:
            # Solo procesar días de lunes a viernes (0-4)
            if fecha_actual.weekday() < 5:
                for jornada in self.jornadas.all():
                    bloques.extend(jornada.generar_bloques(fecha_actual, self.doctor))
            fecha_actual += timedelta(days=1)

        return bloques


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
    def dias_restantes(self):
        fecha_y_hora = datetime.combine(self.bloque.fecha, self.bloque.hora_inicio)
        fecha_y_hora_aware = timezone.make_aware(fecha_y_hora)
        dias_restantes = (fecha_y_hora_aware - timezone.now()).days
        if dias_restantes > 1:
            return f"{dias_restantes} días"
        elif dias_restantes == 1:
            return "1 día"
        else:
            return "Hoy"

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
