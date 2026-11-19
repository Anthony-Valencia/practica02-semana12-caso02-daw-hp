# citas_medicas/middleware.py
import logging
from django.utils import timezone
from django.contrib import messages
from datetime import datetime, time

logger = logging.getLogger('auditoria_medica')

class AuditoriaMedicaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated and ('/historial/' in request.path or '/consulta/' in request.path):
            ip = request.META.get('REMOTE_ADDR')
            logger.warning(f"ACCESO MÉDICO | Usuario: {request.user.username} | IP: {ip} | Ruta: {request.path}")
        return response

class HorarioAtencionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and '/citas/agendar/' in request.path:
            hora_str = request.POST.get('hora')
            fecha_str = request.POST.get('fecha')
            if hora_str and fecha_str:
                try:
                    hora_obj = datetime.strptime(hora_str, '%H:%M').time()
                    fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d').date()
                    dia_semana = fecha_obj.weekday() # 0=Lunes, 5=Sábado, 6=Domingo
                    
                    if dia_semana == 6:
                        messages.error(request, "No hay atención los domingos.")
                    
                    if dia_semana <= 4: # Lunes a Viernes
                        if not (time(8, 0) <= hora_obj <= time(18, 0)):
                            messages.error(request, "El horario de atención es de 8:00 a 18:00.")
                    elif dia_semana == 5: # Sábado
                        if not (time(8, 0) <= hora_obj <= time(13, 0)):
                            messages.error(request, "El horario de atención los sábados es de 8:00 a 13:00.")
                except ValueError:
                    pass
        return self.get_response(request)

class AlertaCitasMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.session.get('alerta_citas_mostrada'):
            if hasattr(request.user, 'perfil_medico'):
                from .models import Cita
                citas_hoy = Cita.objects.filter(
                    medico=request.user.perfil_medico,
                    fecha=timezone.now().date(),
                    estado='pendiente'
                ).count()
                if citas_hoy > 0:
                    messages.info(request, f"Tienes {citas_hoy} cita(s) pendiente(s) para el día de hoy.")
                request.session['alerta_citas_mostrada'] = True
        return self.get_response(request)