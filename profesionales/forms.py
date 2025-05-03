from django import forms
from .models import Profesional
from especialidades.models import Especialidad
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class ProfesionalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asegurarse de que las especialidades estén disponibles
        especialidades = Especialidad.objects.filter(estado=True).order_by('nombre')
        print(f"Cargando {especialidades.count()} especialidades")
        
        # Hacer todos los campos requeridos excepto los que pueden ser nulos
        for field_name, field in self.fields.items():
            if field_name not in ['telefono', 'email', 'direccion']:
                field.required = True
                field.widget.attrs['required'] = 'required'
        
        self.fields['especialidad'] = forms.ModelChoiceField(
            queryset=especialidades,
            widget=forms.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            }),
            required=True,
            label='Especialidad',
            empty_label='Seleccione una especialidad'
        )

    class Meta:
        model = Profesional
        fields = [
            'rut', 'nombres', 'apellido_paterno', 'apellido_materno',
            'fecha_nacimiento', 'genero', 'telefono', 'email',
            'direccion', 'especialidad'
        ]
        widgets = {
            'rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 12345678-9',
                'required': 'required'
            }),
            'nombres': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'text-transform: uppercase;',
                'required': 'required'
            }),
            'apellido_paterno': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'text-transform: uppercase;',
                'required': 'required'
            }),
            'apellido_materno': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'text-transform: uppercase;',
                'required': 'required'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': 'required'
            }),
            'genero': forms.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            }),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'rut': 'RUT',
            'nombres': 'Nombres',
            'apellido_paterno': 'Apellido Paterno',
            'apellido_materno': 'Apellido Materno',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'genero': 'Género',
            'telefono': 'Teléfono',
            'email': 'Correo Electrónico',
            'direccion': 'Dirección',
            'especialidad': 'Especialidad'
        }

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if not rut:
            raise ValidationError(_('El RUT es obligatorio.'))
        if rut:
            # Verificar si el RUT ya existe
            if Profesional.objects.filter(rut=rut).exclude(pk=self.instance.pk if self.instance else None).exists():
                raise ValidationError(_('Este RUT ya está registrado en el sistema.'))
        return rut

    def clean_nombres(self):
        nombres = self.cleaned_data.get('nombres')
        if not nombres:
            raise ValidationError(_('Los nombres son obligatorios.'))
        return nombres.upper()

    def clean_apellido_paterno(self):
        apellido = self.cleaned_data.get('apellido_paterno')
        if not apellido:
            raise ValidationError(_('El apellido paterno es obligatorio.'))
        return apellido.upper()

    def clean_apellido_materno(self):
        apellido = self.cleaned_data.get('apellido_materno')
        if not apellido:
            raise ValidationError(_('El apellido materno es obligatorio.'))
        return apellido.upper()

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get('fecha_nacimiento')
        if not fecha:
            raise ValidationError(_('La fecha de nacimiento es obligatoria.'))
        return fecha

    def clean_genero(self):
        genero = self.cleaned_data.get('genero')
        if not genero:
            raise ValidationError(_('El género es obligatorio.'))
        return genero

    def clean_especialidad(self):
        especialidad = self.cleaned_data.get('especialidad')
        if not especialidad:
            raise ValidationError(_('La especialidad es obligatoria.'))
        return especialidad

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Verificar si el email ya existe
            if Profesional.objects.filter(email=email).exclude(pk=self.instance.pk if self.instance else None).exists():
                raise ValidationError(_('Este correo electrónico ya está registrado en el sistema.'))
        return email

    def save(self, commit=True):
        try:
            profesional = super().save(commit=False)
            if commit:
                profesional.save()
            return profesional
        except Exception as e:
            print(f"Error al guardar profesional: {str(e)}")
            raise ValidationError(_(f'Error al guardar el profesional: {str(e)}'))

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
        }

class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        } 