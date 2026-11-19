# citas_medicas/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Cita, Consulta

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['paciente', 'medico', 'fecha', 'hora', 'motivo']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
            'motivo': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_motivo(self):
        motivo = self.cleaned_data.get('motivo')
        if motivo and len(motivo) < 20:
            raise ValidationError("El motivo de consulta debe tener al menos 20 caracteres.")
        return motivo

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha and fecha < timezone.now().date():
            raise ValidationError("No se pueden agendar citas en fechas pasadas.")
        return fecha

    def clean(self):
        cleaned_data = super().clean()
        paciente = cleaned_data.get('paciente')
        medico = cleaned_data.get('medico')
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')

        # Paciente no puede tener 2 citas el mismo día
        if paciente and fecha:
            if Cita.objects.filter(paciente=paciente, fecha=fecha).exclude(estado='cancelada').exists():
                raise ValidationError("El paciente ya tiene una cita agendada para este día.")

        # Médico no puede tener citas superpuestas
        if medico and fecha and hora:
            if Cita.objects.filter(medico=medico, fecha=fecha, hora=hora).exclude(estado='cancelada').exists():
                raise ValidationError("El médico ya tiene una cita agendada en este horario.")

        return cleaned_data

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['diagnostico', 'tratamiento', 'medicamentos', 'proxima_cita', 'notas_adicionales']
        widgets = {
            'proxima_cita': forms.DateInput(attrs={'type': 'date'}),
            'diagnostico': forms.Textarea(attrs={'rows': 3}),
            'tratamiento': forms.Textarea(attrs={'rows': 3}),
        }