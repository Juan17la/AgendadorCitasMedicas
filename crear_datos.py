import os
import django
import random
from datetime import datetime, time, timedelta, date

def configurar_django():
    # Configura el entorno de Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

def crear_datos():    # Importa los modelos después de configurar Django
    from apps.users.models import User
    from apps.citasMedicas.models import Especialidad, Doctor, JornadaDiaria, HorarioSemanal, BloqueHorario

    # Limpia los datos existentes
    print("🗑️ Limpiando datos existentes...")
    HorarioSemanal.objects.all().delete()
    Doctor.objects.all().delete()
    JornadaDiaria.objects.all().delete()
    Especialidad.objects.all().delete()
    User.objects.exclude(rol='Administrador').delete()  # Preserva usuarios admin

    # --------- Crear 10 especialidades ----------
    nombres_especialidades = [
        "Cardiología", "Dermatología", "Pediatría", "Neurología", "Psiquiatría",
        "Ginecología", "Urología", "Oftalmología", "Oncología", "Reumatología"
    ]

    especialidades = []

    for nombre in nombres_especialidades:
        e = Especialidad.objects.create(nombre=nombre, descripcion=f"Especialidad médica en {nombre.lower()}.")
        especialidades.append(e)

    print("✅ Especialidades creadas.")

    # --------- Crear jornadas de lunes a viernes 8am - 12pm (bloques de 20 min) ----------
    dias_semana = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes']

    jornadas_creadas = []

    for dia in dias_semana:
        jornada = JornadaDiaria.objects.create(
            dia=dia,
            hora_inicio=time(hour=8),
            hora_fin=time(hour=12),
            duracion_bloque=20
        )
        jornadas_creadas.append(jornada)

    print("✅ Jornadas creadas.")

    # --------- Crear 20 usuarios con rol Doctor + modelo Doctor + horario semanal ----------
    for i in range(1, 21):
        cedula = f"10{i:05d}"
        email = f"doctor{i}@ejemplo.com"
        nombres = f"Doctor{i}"
        apellidos = f"Apellido{i}"
        telefono = f"3001234{i:04d}"

        user = User.objects.create_user(
            cedula_ti=cedula,
            email=email,
            password="12345",
            nombres=nombres,
            apellidos=apellidos,
            fecha_nacimiento=date(1990, 1, 1),
            telefono=telefono,
            rol='Doctor',
        )

        especialidad = random.choice(especialidades)
        doctor = Doctor.objects.create(
            user=user,
            especialidad=especialidad,
            consultorio=f"{random.randint(100, 500)}"
        )

        # Crear horario semanal a partir de hoy
        horario = HorarioSemanal.objects.create(
            doctor=doctor,
            inicio_horario=date.today()
        )
        horario.jornadas.set(jornadas_creadas)
    print("✅ 20 doctores con horarios creados.")

    # --------- Crear bloques horarios para cada doctor ----------
    # Obtener todos los doctores
    doctores = Doctor.objects.all()
    
    # Para cada doctor, crear bloques horarios para la próxima semana
    for doctor in doctores:
        horario_semanal = doctor.horarios_semanales.first()
        if horario_semanal:
            # Para cada jornada del doctor
            for jornada in horario_semanal.jornadas.all():
                # Calcular las fechas para los próximos 7 días
                for i in range(7):
                    fecha_actual = date.today() + timedelta(days=i)
                    
                    # Mapear el día de la semana (0=lunes, 6=domingo) al formato de la base de datos
                    dias_map = {
                        0: 'lunes', 1: 'martes', 2: 'miercoles',
                        3: 'jueves', 4: 'viernes', 5: 'sabado', 6: 'domingo'
                    }
                    
                    # Si el día de la semana coincide con la jornada
                    if dias_map[fecha_actual.weekday()] == jornada.dia:
                        # Crear bloques de 20 minutos entre hora_inicio y hora_fin
                        hora_actual = datetime.combine(fecha_actual, jornada.hora_inicio)
                        hora_fin = datetime.combine(fecha_actual, jornada.hora_fin)
                        
                        while hora_actual < hora_fin:
                            # Crear el bloque
                            hora_fin_bloque = (hora_actual + timedelta(minutes=jornada.duracion_bloque))
                            
                            BloqueHorario.objects.create(
                                doctor=doctor,
                                jornada=jornada,
                                fecha=fecha_actual,
                                hora_inicio=hora_actual.time(),
                                hora_fin=hora_fin_bloque.time(),
                                disponible=True
                            )
                            
                            # Avanzar al siguiente bloque
                            hora_actual = hora_fin_bloque

    print("✅ Bloques horarios creados para todos los doctores.")

if __name__ == '__main__':
    configurar_django()
    crear_datos()
