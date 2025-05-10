from django.shortcuts import render, redirect
from django.http import JsonResponse 
from .models import Cita, Especialidad, Doctor, HorarioSemanal, JornadaDiaria, BloqueHorario
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

'''-------------------------------- 
Vistas Templates
-------------------------------'''
@login_required
def agendarCita(request):
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            bloque_id = request.POST.get('bloque')
            razon = request.POST.get('razon')
            
            # Validar que existan los datos necesarios
            if not bloque_id or not razon:
                return render(request, 'agendarcita.html', {
                    'error': 'Por favor, complete todos los campos requeridos.'
                })
            
            # Obtener el bloque horario y verificar disponibilidad
            bloque = BloqueHorario.objects.get(id=bloque_id, disponible=True)
            
            # Crear la cita
            cita = Cita.objects.create(
                especialidad=bloque.doctor.especialidad,
                doctor=bloque.doctor,
                paciente=request.user,
                bloque=bloque,
                motivo=razon,
                estado='pendiente'
            )
            
            # Marcar el bloque como no disponible
            bloque.disponible = False
            bloque.save()
            
            # Redirigir a la página de detalles de la cita
            return render(request, 'citadetalles.html', {
                'cita': cita,
            })
            
        except BloqueHorario.DoesNotExist:
            return render(request, 'agendarcita.html', {
                'error': 'El horario seleccionado ya no está disponible. Por favor, seleccione otro horario.'
            })
        except Exception as e:
            return render(request, 'agendarcita.html', {
                'error': f'Ocurrió un error al agendar la cita: {str(e)}'
            })
    
    # Si es GET, mostrar el formulario
    return render(request, 'agendarcita.html', {
        'especialidades' : Especialidad.objects.all(),
    })
    
@login_required
def citas(request):
    return render(request, 'citas.html', {
        'nCitasP' : Cita.objects.filter(paciente=request.user, estado='pendiente').count(),
        'nCitasC' : Cita.objects.filter(paciente=request.user, estado='cancelada').count(),
        'citasP' : Cita.objects.filter(paciente=request.user, estado='pendiente'),
        'citasC' : Cita.objects.filter(paciente=request.user, estado='cancelada'),
    })
    
@login_required
def citaDetalles(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    return render(request, 'citadetalles.html', {
        'cita': cita,
    })
    
@login_required
def pacienteDashboard(request):
    return render(request, 'dashboarpaciente.html', {
        'CitaProxima' : Cita.objects.filter(paciente=request.user, estado='pendiente').first(),
    })
'''-------------------------------- 
Agendar Citas Funciones 
-------------------------------'''
@require_GET
@login_required
def get_especialidades(request):
    try:
        especialidades = Especialidad.objects.all()
        data = [
            {
                'id': esp.id,
                'nombre': esp.nombre,
                'descripcion': esp.descripcion,
            } for esp in especialidades
        ]
        return JsonResponse(data, safe=False, status=200)
    except Exception as e:
        return JsonResponse({'error': 'Ocurrio un error al obtener las especialidades'}, status=500)

@require_GET
@login_required
def get_doctores(request, especialidad_id):
    try:
        doctores = Doctor.objects.filter(especialidad_id=especialidad_id)
        data = [
            {
                'id': doctor.id,
                'nombre': f'Dr. {doctor.user.nombres} {doctor.user.apellidos}',
            } for doctor in doctores
        ]
        return JsonResponse(data, safe=False, status=200)
    except Exception as e:
        return JsonResponse({'error': 'Ocurrio un error al obtener los doctores'}, status=500)
    
@require_GET
@login_required
def get_fechas(request, doctor_id):
    """
    Vista para obtener las fechas disponibles de un doctor en un rango de 8 semanas.
    """
    try:
        from datetime import date, timedelta, datetime
        from collections import defaultdict
        
        # Obtener fecha actual y límite de 8 semanas
        hoy = date.today()
        limite = hoy + timedelta(weeks=8)
        
        # Obtener el doctor y sus horarios
        doctor = Doctor.objects.select_related('user').get(id=doctor_id)
        horarios_semanales = HorarioSemanal.objects.filter(
            doctor=doctor,
            inicio_horario__lte=limite
        ).prefetch_related('jornadas')
        
        if not horarios_semanales:
            return JsonResponse({
                'error': 'No se encontraron horarios configurados para este doctor'
            }, status=404)
        
        # Diccionario para almacenar bloques por fecha
        bloques_por_fecha = defaultdict(list)
        fecha_actual = hoy
        
        # Iterar por cada día en el rango de 8 semanas
        while fecha_actual <= limite:
            dia_semana = fecha_actual.weekday()  # 0=Lunes, 6=Domingo
            
            # Solo procesar días de lunes a viernes (0-4)
            if dia_semana < 5:
                for horario in horarios_semanales:
                    # Obtener las jornadas para este día de la semana
                    jornadas = horario.jornadas.filter(dia_semana=dia_semana)
                    
                    for jornada in jornadas:
                        # Obtener bloques disponibles para esta fecha
                        bloques = BloqueHorario.objects.filter(
                            doctor=doctor,
                            jornada=jornada,
                            fecha=fecha_actual,
                            disponible=True
                        ).order_by('hora_inicio')
                        
                        # Si no hay bloques y la fecha es futura, crearlos
                        if not bloques.exists() and fecha_actual >= hoy:
                            hora_actual = datetime.combine(fecha_actual, jornada.hora_inicio)
                            hora_fin = datetime.combine(fecha_actual, jornada.hora_fin)
                            duracion = timedelta(minutes=jornada.duracion_bloque)
                            
                            while hora_actual + duracion <= hora_fin:
                                bloque = BloqueHorario.objects.create(
                                    doctor=doctor,
                                    jornada=jornada,
                                    fecha=fecha_actual,
                                    hora_inicio=hora_actual.time(),
                                    hora_fin=(hora_actual + duracion).time(),
                                    disponible=True
                                )
                                bloques_por_fecha[fecha_actual.strftime('%Y-%m-%d')].append({
                                    'id': bloque.id,
                                    'hora_inicio': bloque.hora_inicio.strftime('%H:%M'),
                                    'hora_fin': bloque.hora_fin.strftime('%H:%M')
                                })
                                hora_actual += duracion
                        else:
                            # Agregar bloques existentes que estén disponibles
                            for bloque in bloques:
                                bloques_por_fecha[fecha_actual.strftime('%Y-%m-%d')].append({
                                    'id': bloque.id,
                                    'hora_inicio': bloque.hora_inicio.strftime('%H:%M'),
                                    'hora_fin': bloque.hora_fin.strftime('%H:%M')
                                })
            
            fecha_actual += timedelta(days=1)
        
        # Convertir el diccionario a lista de fechas disponibles
        fechas_disponibles = [
            {
                'fecha': fecha,
                'dia_semana': datetime.strptime(fecha, '%Y-%m-%d').strftime('%A'),
                'bloques': bloques
            }
            for fecha, bloques in bloques_por_fecha.items()
            if bloques  # Solo incluir fechas que tienen bloques disponibles
        ]
        
        return JsonResponse(fechas_disponibles, safe=False)
        
    except Doctor.DoesNotExist:
        return JsonResponse({
            'error': 'No se encontró el doctor especificado'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'error': f'Ocurrió un error al obtener las fechas disponibles: {str(e)}'
        }, status=500)

@require_GET
@login_required
def get_bloques(request, jornada_id, doctor_id):
    try:
        fechas = BloqueHorario.objects.filter(jornada_id=jornada_id, doctor_id=doctor_id)
        data = [
            {
                'doctor' : fecha.doctor.user.nombres,
                'jornada' : fecha.jornada.dia,
                'fecha' : fecha.fecha,
                'hora_inicio' : fecha.hora_inicio.strftime('%H:%M'),
                'hora_fin' : fecha.hora_fin.strftime('%H:%M'),
                'disponible' : fecha.disponible,
            } for fecha in fechas
        ]
        return JsonResponse(data, safe=False, status=200)
    except Exception as e:
        return JsonResponse({'error': 'Ocurrio un error al obtener los doctores'}, status=500)
