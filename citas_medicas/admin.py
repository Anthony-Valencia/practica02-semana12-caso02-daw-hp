# citas_medicas/admin.py
from django.contrib import admin
from .models import Medico, Paciente, Cita, Consulta

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'cmp', 'especialidad', 'consultorio')
    search_fields = ('usuario__first_name', 'usuario__last_name', 'cmp')
    list_filter = ('especialidad',)

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'dni', 'tipo', 'edad', 'codigo_uncp')
    search_fields = ('dni', 'usuario__first_name', 'usuario__last_name')
    list_filter = ('tipo',)

    @admin.display(description='Edad')
    def edad(self, obj):
        return obj.edad()

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('id', 'paciente', 'medico', 'fecha', 'hora', 'estado')
    list_filter = ('estado', 'fecha', 'medico__especialidad')
    search_fields = ('paciente__dni', 'paciente__usuario__first_name')
    actions = ['marcar_completadas']

    @admin.action(description='Marcar citas seleccionadas como completadas')
    def marcar_completadas(self, request, queryset):
        actualizadas = queryset.update(estado='completada')
        self.message_user(request, f'{actualizadas} citas marcadas como completadas.')

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cita', 'fecha_registro', 'dias_transcurridos')
    readonly_fields = ('cita', 'diagnostico', 'tratamiento', 'medicamentos', 'proxima_cita', 'fecha_registro')
    
    @admin.display(description='Días desde consulta')
    def dias_transcurridos(self, obj):
        return obj.dias_desde_consulta()
    
    def has_add_permission(self, request):
        return False # No se pueden crear desde admin, solo desde el flujo de atención