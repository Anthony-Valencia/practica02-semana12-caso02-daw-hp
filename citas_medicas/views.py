# citas_medicas/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Cita
from .forms import CitaForm, ConsultaForm

@login_required
def agenda_medico(request):
    if hasattr(request.user, 'perfil_medico'):
        citas = Cita.objects.filter(medico=request.user.perfil_medico).select_related('paciente__usuario')
    elif request.user.is_superuser:
        citas = Cita.objects.all().select_related('paciente__usuario', 'medico__usuario')
    else:
        citas = Cita.objects.none()
    return render(request, 'citas_medicas/agenda.html', {'citas': citas})

@login_required
@permission_required('citas_medicas.add_cita', raise_exception=True)
def agendar_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cita agendada correctamente.")
            return redirect('citas_medicas:agenda')
    else:
        form = CitaForm()
    return render(request, 'citas_medicas/form.html', {'form': form, 'titulo': 'Agendar Cita'})

@login_required
@permission_required('citas_medicas.add_consulta', raise_exception=True)
def registrar_consulta(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    if request.user != cita.medico.usuario:
        messages.error(request, "No tienes permiso para registrar esta consulta.")
        return redirect('citas_medicas:agenda')

    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.cita = cita
            consulta.save()
            cita.estado = 'completada'
            cita.save()
            messages.success(request, "Consulta registrada exitosamente.")
            return redirect('citas_medicas:agenda')
    else:
        form = ConsultaForm()
    return render(request, 'citas_medicas/form.html', {'form': form, 'titulo': 'Registrar Consulta'})