# citas_medicas/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

User = settings.AUTH_USER_MODEL

class Medico(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_medico')
    cmp = models.CharField(
        max_length=10, unique=True,
        validators=[RegexValidator(r'^\d{5}$', 'El CMP debe tener exactamente 5 dígitos numéricos.')]
    )
    especialidad = models.CharField(max_length=100)
    consultorio = models.CharField(max_length=50)

    def __str__(self):
        return f"Dr(a). {self.usuario.get_full_name()} - {self.especialidad}"

class Paciente(models.Model):
    TIPO_CHOICES = [('estudiante', 'Estudiante'), ('docente', 'Docente')]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_paciente')
    dni = models.CharField(
        max_length=8, unique=True,
        validators=[RegexValidator(r'^\d{8}$', 'El DNI debe tener 8 dígitos numéricos.')]
    )
    fecha_nacimiento = models.DateField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    codigo_uncp = models.CharField(max_length=20)
    alergias = models.TextField(blank=True, null=True)

    def clean(self):
        super().clean()
        if self.fecha_nacimiento and self.fecha_nacimiento > timezone.now().date():
            raise ValidationError({'fecha_nacimiento': 'La fecha de nacimiento no puede ser futura.'})
        if self.tipo == 'estudiante' and self.usuario.email and not self.usuario.email.endswith('@uncp.edu.pe'):
            raise ValidationError({'usuario': 'El estudiante debe tener un correo institucional @uncp.edu.pe.'})

    def edad(self):
        hoy = timezone.now().date()
        return hoy.year - self.fecha_nacimiento.year - ((hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))

    def __str__(self):
        return f"{self.usuario.get_full_name()} (DNI: {self.dni})"

class Cita(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='citas')
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='citas')
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.TextField(help_text="Mínimo 20 caracteres")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        return f"Cita: {self.paciente} con {self.medico} el {self.fecha} a las {self.hora}"

class Consulta(models.Model):
    cita = models.OneToOneField(Cita, on_delete=models.CASCADE, related_name='consulta')
    diagnostico = models.TextField()
    tratamiento = models.TextField()
    medicamentos = models.TextField()
    proxima_cita = models.DateField(null=True, blank=True)
    notas_adicionales = models.TextField(blank=True, help_text="Solo se pueden agregar notas.")
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def dias_desde_consulta(self):
        return (timezone.now().date() - self.fecha_registro.date()).days

    def __str__(self):
        return f"Consulta de {self.cita.paciente} - {self.fecha_registro.date()}"