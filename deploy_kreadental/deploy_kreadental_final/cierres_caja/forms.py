from django import forms
from .models import CierreCaja, RetiroCaja

class CierreCajaForm(forms.ModelForm):
    class Meta:
        model = CierreCaja
        fields = ['monto_inicial', 'observaciones']
        widgets = {
            'monto_inicial': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '50000',
                'pattern': '[0-9]+',
                'title': 'Ingresa el monto inicial (ej: 50000)',
                'autocomplete': 'off'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones adicionales'
            })
        }
    
    def clean_monto_inicial(self):
        monto = self.cleaned_data.get('monto_inicial')
        
        # Validar que el campo no esté vacío
        if not monto:
            raise forms.ValidationError('El monto inicial es requerido')
        
        # Convertir separadores de miles a formato entero
        if isinstance(monto, str):
            # Remover todos los separadores de miles y espacios
            monto_limpio = monto.replace('.', '').replace(',', '').replace(' ', '').strip()
            
            if not monto_limpio:
                raise forms.ValidationError('El monto inicial es requerido')
            try:
                # Convertir a float primero para manejar decimales, luego a int
                monto = int(float(monto_limpio))
            except ValueError:
                raise forms.ValidationError('Ingresa un monto válido (ej: 50000)')
        
        # Validar que el monto sea positivo
        if monto < 0:
            raise forms.ValidationError('El monto debe ser positivo')
        
        # Validar que no exceda el límite del modelo
        if monto > 999999999:
            raise forms.ValidationError('El monto no puede exceder 999,999,999')
        
        return monto

class CerrarCajaForm(forms.ModelForm):
    class Meta:
        model = CierreCaja
        fields = ['monto_final', 'observaciones']
        widgets = {
            'monto_final': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0',
                'pattern': '[0-9]+',
                'title': 'Ingresa un número válido (ej: 50000)'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones del cierre'
            })
        }
    
    def clean_monto_final(self):
        monto = self.cleaned_data.get('monto_final')
        if monto is not None:
            # Convertir separadores de miles a formato entero
            if isinstance(monto, str):
                monto = monto.replace('.', '').replace(',', '')
                try:
                    monto = int(monto)
                except ValueError:
                    raise forms.ValidationError('Ingresa un monto válido (ej: 50000)')
            return monto
        return monto


class RetiroCajaForm(forms.ModelForm):
    class Meta:
        model = RetiroCaja
        fields = ['monto', 'concepto', 'comprobante', 'observaciones']
        widgets = {
            'monto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa el monto del retiro (ej: 50000)',
                'pattern': '[0-9]+',
                'title': 'Ingresa un monto válido (ej: 50000)',
                'autocomplete': 'off'
            }),
            'concepto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción del gasto o compra especial',
                'maxlength': '200'
            }),
            'comprobante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de factura, boleta o comprobante (opcional)',
                'maxlength': '100'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Observaciones adicionales (opcional)',
                'rows': 3
            })
        }
    
    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        
        # Validar que el campo no esté vacío
        if not monto:
            raise forms.ValidationError('El monto del retiro es requerido')
        
        # Convertir separadores de miles a formato entero
        if isinstance(monto, str):
            # Remover todos los separadores de miles y espacios
            monto_limpio = monto.replace('.', '').replace(',', '').replace(' ', '').strip()
            
            if not monto_limpio:
                raise forms.ValidationError('El monto del retiro es requerido')
            try:
                # Convertir a float primero para manejar decimales, luego a int
                monto = int(float(monto_limpio))
            except ValueError:
                raise forms.ValidationError('Ingresa un monto válido (ej: 50000)')
        
        # Validar que el monto sea positivo
        if monto <= 0:
            raise forms.ValidationError('El monto debe ser mayor a 0')
        
        # Validar que no exceda el límite del modelo
        if monto > 999999999:
            raise forms.ValidationError('El monto no puede exceder 999,999,999')
        
        return monto
