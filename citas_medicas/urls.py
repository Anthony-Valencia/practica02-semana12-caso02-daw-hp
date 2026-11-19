from django.urls import path
from . import views

app_name = 'citas_medicas'

urlpatterns = [
    path('', views.agenda_medico, name='agenda'),
    path('agendar/', views.agendar_cita, name='agendar'),
    path('consulta/<int:cita_id>/', views.registrar_consulta, name='registrar_consulta'),
]