from django import forms
from .models import CierreCaja

class CierreCajaForm(forms.ModelForm):
    class Meta:
        model = CierreCaja
        fields = ['monto_inicial', 'observaciones']
        widgets = {
            'monto_inicial': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'min': '0',
                'step': '0.01'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones adicionales'
            })
        }

class CerrarCajaForm(forms.ModelForm):
    class Meta:
        model = CierreCaja
        fields = ['monto_final', 'observaciones']
        widgets = {
            'monto_final': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'min': '0',
                'step': '0.01'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones del cierre'
            })
        }
