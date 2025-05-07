from django.db import models
from apps.users.models import User
from django.utils import timezone

# Create your models here.
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor')
    especialidad = models.CharField(max_length=100)
    consultorio = models.CharField(max_length=100)

    def __str__(self):
        return f'Dr.{self.user.nombres} {self.user.apellidos}'

class Cita(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='citas')
    paciente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='citas')
    fecha_hora = models.DateTimeField()
    motivo = models.TextField(max_length=2000)
    estado = models.CharField(max_length=20, 
                              choices=[
                                        ('pendiente', 'Pendiente'), 
                                        ('confirmada', 'Confirmada'), 
                                        ('cancelada', 'Cancelada')], 
                              default='pendiente')
    @property
    def dia_fecha_cita(self):
        return self.fecha_hora.strftime("%d")
    
    @property
    def mes_fecha_cita(self):
        mes = self.fecha_hora.strftime("%m")
        meses = {
            '01': 'Enero',
            '02': 'Febrero',
            '03': 'Marzo',
            '04': 'Abril',
            '05': 'Mayo',
            '06': 'Junio',
            '07': 'Julio',
            '08': 'Agosto',
            '09': 'Septiembre',
            '10': 'Octubre',
            '11': 'Noviembre',
            '12': 'Diciembre'
        }
        return meses[mes]
    
    @property
    def hora_cita(self):
        return self.fecha_hora.strftime("%H:%M")
    
    @property
    def dias_restantes(self):
        return (self.fecha_hora - timezone.now()).days
    
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
