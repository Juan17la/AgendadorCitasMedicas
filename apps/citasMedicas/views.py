from django.shortcuts import render
from .forms import CitaForm
from .models import Cita
from apps.users.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# Create your views here.
@login_required
def agendarCita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            citaAgendada = Cita.objects.create(
                doctor=form.cleaned_data['doctor'],
                paciente=request.user,
                fecha_hora=form.cleaned_data['fecha_hora'],
                motivo=form.cleaned_data['motivo'],
                estado='pendiente'
            )
            return render(request, 'citadetalles.html', {
                'cita': citaAgendada,
            })
    else:
        form = CitaForm()
    return render(request, 'agendarcita.html', {'form': form})

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