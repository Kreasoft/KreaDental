from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Empresa, Sucursal, UsuarioEmpresa
from django.core.validators import RegexValidator
from datetime import datetime

User = get_user_model()

class DateInput(forms.DateInput):
    input_type = 'date'
    
    def format_value(self, value):
        if value is None:
            return ''
        
        # Si es un string en formato dd/mm/yyyy, convertirlo
        if isinstance(value, str) and '/' in value:
            try:
                # Convertir dd/mm/yyyy a yyyy-mm-dd
                parts = value.split('/')
                if len(parts) == 3:
                    day, month, year = parts
                    return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            except:
                pass
        
        # Si es un objeto date, usar strftime
        if hasattr(value, 'strftime'):
            return value.strftime('%Y-%m-%d')
        
        # Si ya está en formato yyyy-mm-dd, devolverlo
        if isinstance(value, str) and len(value) == 10 and value[4] == '-' and value[7] == '-':
            return value
        
        return str(value) if value else ''

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = [
            'razon_social', 
            'nombre_fantasia', 
            'rut', 
            'direccion', 
            'telefono', 
            'email', 
            'sitio_web', 
            'logo', 
            'activa'
        ]
        widgets = {
            'razon_social': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Razón Social'}),
            'nombre_fantasia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de Fantasía'}),
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RUT'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Dirección'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'sitio_web': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Sitio Web'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class SucursalForm(forms.ModelForm):
    class Meta:
        model = Sucursal
        fields = [
            'nombre',
            'direccion',
            'telefono',
            'email',
            'horario_apertura',
            'horario_cierre',
            'activa'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la Sucursal'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Dirección'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'horario_apertura': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'horario_cierre': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class UsuarioEmpresaForm(forms.ModelForm):
    email = forms.EmailField(
        label='Email del Usuario',
        help_text='Ingrese el email del usuario. Si no existe, se creará una cuenta nueva.',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email del usuario'})
    )
    password = forms.CharField(
        label='Contraseña',
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña (dejar en blanco para mantener la actual)'}),
        help_text='Dejar en blanco para mantener la contraseña actual si el usuario ya existe.'
    )
    
    class Meta:
        model = UsuarioEmpresa
        fields = ['sucursal', 'tipo_usuario', 'activo', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'sucursal': forms.Select(attrs={'class': 'form-select'}),
            'tipo_usuario': forms.Select(attrs={'class': 'form-select'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'fecha_inicio': DateInput(attrs={
                'class': 'form-control', 
                'pattern': '[0-9]{4}-[0-9]{2}-[0-9]{2}',
                'placeholder': 'YYYY-MM-DD'
            }),
            'fecha_fin': DateInput(attrs={
                'class': 'form-control', 
                'pattern': '[0-9]{4}-[0-9]{2}-[0-9]{2}',
                'placeholder': 'YYYY-MM-DD'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa', None)
        usuario_actual = kwargs.pop('usuario_actual', None)
        super().__init__(*args, **kwargs)
        
        if empresa:
            # Filtrar sucursales por empresa
            self.fields['sucursal'].queryset = Sucursal.objects.filter(empresa=empresa, activa=True)
            
            # Filtrar tipos de usuario según el rol del usuario actual
            if usuario_actual:
                if usuario_actual.tipo_usuario == 'super_admin':
                    # Super admin puede crear cualquier tipo de usuario
                    pass
                elif usuario_actual.tipo_usuario == 'admin_empresa':
                    # Admin empresa no puede crear super_admin
                    choices = [choice for choice in self.fields['tipo_usuario'].choices if choice[0] != 'super_admin']
                    self.fields['tipo_usuario'].choices = choices
                else:
                    # Otros usuarios no pueden crear usuarios
                    self.fields['tipo_usuario'].choices = []
        
        # Si es una edición (instance existe), inicializar los campos con los valores existentes
        if self.instance and self.instance.pk and hasattr(self.instance, 'usuario') and self.instance.usuario:
            # Inicializar el email con el valor del usuario
            self.fields['email'].initial = self.instance.usuario.email
            
            # El widget DateInput se encargará del formateo de fechas automáticamente
            # No necesitamos inicializar manualmente las fechas
            
            # Cambiar el texto de ayuda para la contraseña en edición
            self.fields['password'].help_text = 'Dejar en blanco para mantener la contraseña actual. Ingrese una nueva contraseña para cambiarla.'
            self.fields['password'].widget.attrs['placeholder'] = 'Nueva contraseña (dejar en blanco para mantener la actual)'
    
    def clean_email(self):
        email = self.cleaned_data['email']
        # Verificar que el email no esté ya asignado a esta empresa
        if self.instance.pk:  # Si es una edición
            existing = UsuarioEmpresa.objects.filter(
                usuario__email=email,
                empresa=self.instance.empresa
            ).exclude(pk=self.instance.pk)
        else:  # Si es una creación
            existing = UsuarioEmpresa.objects.filter(
                usuario__email=email,
                empresa=self.instance.empresa if hasattr(self.instance, 'empresa') else None
            )
        
        if existing.exists():
            raise forms.ValidationError('Este email ya está asignado a un usuario en esta empresa.')
        
        return email
    
    def save(self, commit=True):
        email = self.cleaned_data['email']
        password = self.cleaned_data.get('password')
        
        # Si es una edición y el email no cambió, usar el usuario existente
        if self.instance and self.instance.pk and hasattr(self.instance, 'usuario') and self.instance.usuario:
            if self.instance.usuario.email == email:
                # El email no cambió, usar el usuario existente
                usuario = self.instance.usuario
                if password:
                    usuario.set_password(password)
                    usuario.save()
            else:
                # El email cambió, buscar o crear nuevo usuario
                try:
                    usuario = User.objects.get(email=email)
                    if password:
                        usuario.set_password(password)
                        usuario.save()
                except User.DoesNotExist:
                    # Crear nuevo usuario sin username
                    usuario = User.objects.create_user(
                        email=email,
                        password=password or 'temp_password_123'  # Contraseña temporal
                    )
        else:
            # Es una creación nueva
            try:
                usuario = User.objects.get(email=email)
                if password:
                    usuario.set_password(password)
                    usuario.save()
            except User.DoesNotExist:
                # Crear nuevo usuario sin username
                usuario = User.objects.create_user(
                    email=email,
                    password=password or 'temp_password_123'  # Contraseña temporal
                )
        
        # Asignar el usuario al modelo UsuarioEmpresa
        self.instance.usuario = usuario
        
        return super().save(commit)