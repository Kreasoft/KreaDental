from django.contrib import admin
from .models import Prevision

@admin.register(Prevision)
class PrevisionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'estado', 'created_at', 'updated_at')
    list_filter = ('estado',)
    search_fields = ('nombre', 'descripcion')
    ordering = ('nombre',)
