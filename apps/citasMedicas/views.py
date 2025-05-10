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
    return render(request, 'agendarcita.html', {
        'especialidades' : Especialidad.objects.all(),
    })
    
@login_required
def citas(request):
    return render(request, 'citas.html', {
        'nCitasP' : Cita.objects.filter(paciente=request.user, estado='pendiente').count(),
        'nCitasC' : Cita.objects.filter(paciente=request.user, estado='cancelada').count(),
        'citasP' : Cita.objects.filter(paciente=request.user, estado='pendiente').order_by('fecha_hora'),
        'citasC' : Cita.objects.filter(paciente=request.user, estado='cancelada').order_by('fecha_hora'),
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
        'CitaProxima' : Cita.objects.filter(paciente=request.user, estado='pendiente').order_by('fecha_hora').first(),
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
    try:
        fechas = HorarioSemanal.objects.filter(doctor_id=doctor_id)
        data = [
            {
                'id': fecha.id,
                'jornadas': [
                    {
                        'id': jornada.id,
                        'dia': jornada.dia,
                        'hora_inicio': jornada.hora_inicio.strftime('%H:%M'),
                        'hora_fin': jornada.hora_fin.strftime('%H:%M'),
                        'duracion_bloque': jornada.duracion_bloque,
                    } for jornada in fecha.jornadas.all()
                ],
            } for fecha in fechas
        ]
        return JsonResponse(data, safe=False, status=200)
    except Exception as e:
        return JsonResponse({'error': 'Ocurrio un error al obtener los doctores'}, status=500)

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
