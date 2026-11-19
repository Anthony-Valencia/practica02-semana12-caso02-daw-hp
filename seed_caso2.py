# seed_caso2.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from citas_medicas.models import Medico, Paciente, Cita
from datetime import date, time

Usuario = get_user_model()

# 1. Crear Grupos y Asignar Permisos
g_medicos, _ = Group.objects.get_or_create(name='Médicos')
g_recep, _ = Group.objects.get_or_create(name='Recepcionistas')
g_pacientes, _ = Group.objects.get_or_create(name='Pacientes')
g_admins, _ = Group.objects.get_or_create(name='Admins')

# Permisos
g_medicos.permissions.add(Permission.objects.get(codename='view_consulta'))
g_medicos.permissions.add(Permission.objects.get(codename='add_consulta'))
g_recep.permissions.add(Permission.objects.get(codename='add_cita'))
g_recep.permissions.add(Permission.objects.get(codename='change_cita'))
g_pacientes.permissions.add(Permission.objects.get(codename='add_cita'))

# 2. Crear Usuarios
admin, _ = Usuario.objects.get_or_create(username='admin', defaults={'email': 'admin@uncp.edu.pe', 'is_superuser': True, 'is_staff': True})
admin.set_password('admin123')
admin.save()
admin.groups.add(g_admins)

u_medico, _ = Usuario.objects.get_or_create(username='medico1', defaults={'first_name': 'Carlos', 'last_name': 'Pérez', 'email': 'carlos@uncp.edu.pe'})
u_medico.set_password('medico123')
u_medico.save()
u_medico.groups.add(g_medicos)
Medico.objects.get_or_create(usuario=u_medico, defaults={'cmp': '12345', 'especialidad': 'Cardiología', 'consultorio': 'C-101'})

u_recep, _ = Usuario.objects.get_or_create(username='recepcion1', defaults={'first_name': 'Ana', 'last_name': 'Gómez'})
u_recep.set_password('recepcion123')
u_recep.save()
u_recep.groups.add(g_recep)

u_pac, _ = Usuario.objects.get_or_create(username='paciente1', defaults={'first_name': 'Luis', 'last_name': 'Torres', 'email': 'luis@uncp.edu.pe'})
u_pac.set_password('paciente123')
u_pac.save()
u_pac.groups.add(g_pacientes)
Paciente.objects.get_or_create(usuario=u_pac, defaults={'dni': '12345678', 'fecha_nacimiento': date(2000, 5, 20), 'tipo': 'estudiante', 'codigo_uncp': '2020001'})

print("Datos del Caso 2 creados exitosamente.")