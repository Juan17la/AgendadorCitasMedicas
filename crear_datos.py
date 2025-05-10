import os
import django
from datetime import time, date, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.citasMedicas.models import Especialidad, Doctor, JornadaDiaria, HorarioSemanal, BloqueHorario, Cita, CitaConfirmada

User = get_user_model()

def limpiar_datos():
    """Limpia todos los datos existentes relacionados con citas médicas"""
    print("Limpiando datos existentes...")
    
    # Eliminar en orden para respetar las dependencias
    print("- Eliminando citas confirmadas...")
    CitaConfirmada.objects.all().delete()
    
    print("- Eliminando citas...")
    Cita.objects.all().delete()
    
    print("- Eliminando bloques horarios...")
    BloqueHorario.objects.all().delete()
    
    print("- Eliminando horarios semanales...")
    HorarioSemanal.objects.all().delete()
    
    print("- Eliminando jornadas diarias...")
    JornadaDiaria.objects.all().delete()
    
    print("- Eliminando doctores...")
    Doctor.objects.all().delete()
    
    print("- Eliminando especialidades...")
    Especialidad.objects.all().delete()
    
    print("- Eliminando usuarios doctores...")
    User.objects.filter(email__in=[
        'juan.perez@ejemplo.com',
        'maria.garcia@ejemplo.com',
        'carlos.lopez@ejemplo.com'
    ]).delete()
    
    print("Datos limpiados exitosamente.")

def crear_datos_prueba():
    # Primero limpiar datos existentes
    limpiar_datos()
    
    # Crear especialidades
    especialidades = [
        ('Medicina General', 'Consultas y atención médica general'),
        ('Cardiología', 'Atención especializada en el corazón'),
        ('Pediatría', 'Atención médica para niños'),
    ]
    
    for nombre, descripcion in especialidades:
        especialidad = Especialidad.objects.create(
            nombre=nombre,
            descripcion=descripcion
        )
        print(f"Especialidad creada: {especialidad.nombre}")

    # Crear usuarios doctores
    doctores_data = [
        {
            'cedula_ti': '1001',
            'nombres': 'Juan',
            'apellidos': 'Pérez',
            'email': 'juan.perez@ejemplo.com',
            'especialidad': 'Medicina General',
            'consultorio': '101',
            'rol': 'Doctor'
        },
        {
            'cedula_ti': '1002',
            'nombres': 'María',
            'apellidos': 'García',
            'email': 'maria.garcia@ejemplo.com',
            'especialidad': 'Cardiología',
            'consultorio': '202',
            'rol': 'Doctor'
        },
        {
            'cedula_ti': '1003',
            'nombres': 'Carlos',
            'apellidos': 'López',
            'email': 'carlos.lopez@ejemplo.com',
            'especialidad': 'Pediatría',
            'consultorio': '303',
            'rol': 'Doctor'
        }
    ]

    for data in doctores_data:
        # Crear nuevo usuario
        user = User.objects.create_user(
            cedula_ti=data['cedula_ti'],
            email=data['email'],
            nombres=data['nombres'],
            apellidos=data['apellidos'],
            rol=data['rol'],
            password='12345'
        )
        print(f"Usuario creado: {user.email}")

        # Crear doctor
        especialidad = Especialidad.objects.get(nombre=data['especialidad'])
        doctor = Doctor.objects.create(
            user=user,
            especialidad=especialidad,
            consultorio=data['consultorio']
        )
        print(f"Doctor creado: Dr. {user.nombres} {user.apellidos}")

        # Crear jornadas para el doctor
        jornadas = []
        for dia in range(5):  # Lunes a Viernes
            # Jornada mañana
            jornada_m = JornadaDiaria.objects.create(
                dia_semana=dia,
                hora_inicio=time(8, 0),
                hora_fin=time(12, 0),
                duracion_bloque=30
            )
            # Jornada tarde
            jornada_t = JornadaDiaria.objects.create(
                dia_semana=dia,
                hora_inicio=time(14, 0),
                hora_fin=time(18, 0),
                duracion_bloque=30
            )
            jornadas.extend([jornada_m, jornada_t])

        # Crear horario semanal
        horario = HorarioSemanal.objects.create(
            doctor=doctor,
            inicio_horario=date.today()
        )
        
        # Agregar jornadas al horario
        horario.jornadas.add(*jornadas)

        # Generar bloques para las próximas 8 semanas
        print(f"Generando bloques para Dr. {user.nombres} {user.apellidos}")
        horario.generar_bloques_rango(
            fecha_inicio=date.today(),
            fecha_fin=date.today() + timedelta(weeks=8)
        )

if __name__ == '__main__':
    print("Iniciando creación de datos de prueba...")
    crear_datos_prueba()
    print("¡Datos de prueba creados exitosamente!")
