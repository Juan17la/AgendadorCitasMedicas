from django.shortcuts import render

# Create your views here.
def landingPage(request):
    return render(request, 'landingpage.html')

def dashboardPaciente(request):
    return render(request, 'paciente.html')