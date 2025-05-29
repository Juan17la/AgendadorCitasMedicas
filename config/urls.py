"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apps.core import views as core_views
from apps.users import views as users_views
from apps.citasMedicas import views as citasMedicas_views
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.index, name='index'),
    path('signup/', users_views.signUp_view, name='signup'),
    path('signin/', users_views.signIn_view, name='signin'),
    path('signout/', users_views.signOut_view, name='signout'),
    
    path('citas/', citasMedicas_views.citas, name='citas'),
    path('historial/', citasMedicas_views.historial, name='historial'),
    path('doctores/', citasMedicas_views.doctores, name='doctores'),
    
    path('agendarcita/', citasMedicas_views.agendarCita, name='agendar_cita'),
    path('editar-cita/<int:cita_id>', citasMedicas_views.editarCita, name='editar_cita'),
    path('cancelarcita/<int:cita_id>', citasMedicas_views.cancelarCita, name='cancelar_cita'),
    path('cita/<int:cita_id>', citasMedicas_views.citaDetalles, name='cita_detalles'),
    path('dashboarpaciente/', citasMedicas_views.pacienteDashboard, name='paciente_dashboard'),
    
    #peticiones ajax
    path('agendarcita/get_especialidades/', citasMedicas_views.get_especialidades, name='get_especialidades'),
    path('agendarcita/get_doctores/<int:especialidad_id>/', citasMedicas_views.get_doctores, name='get_doctores'),
    path('agendarcita/get_fechas/<int:doctor_id>/', citasMedicas_views.get_fechas, name='get_fechas'),
    path('agendarcita/get_bloques/<int:jornada_id>/<int:doctor_id>/', citasMedicas_views.get_bloques, name='get_bloques'),
    ]
