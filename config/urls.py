from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from core import views
from configuracion.models import ConfiguracionEmpresa

def get_empresa_config():
    try:
        return {'empresa': ConfiguracionEmpresa.objects.first()}
    except:
        return {'empresa': None}

def test_format(request):
    return render(request, 'test_format.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('citas/', include('citas.urls')),
    path('pacientes/', include('pacientes.urls')),
    path('profesionales/', include('profesionales.urls')),
    # Las URLs de especialidades ahora están en la app profesionales
    # path('especialidades/', include('especialidades.urls')),
    path('procedimientos/', include('procedimientos.urls')),
    path('cierres-caja/', include(('cierres_caja.urls', 'cierres_caja'), namespace='cierres_caja')),
    path('tratamientos/', include(('tratamientos.urls', 'tratamientos'), namespace='tratamientos')),
    path('informes/', include('informes.urls')),
    path('pagos/', include(('pagos_tratamientos.urls', 'pagos_tratamientos'), namespace='pagos_tratamientos')),
    path('configuracion/', include('configuracion.urls', namespace='configuracion')),
    path('previsiones/', include('prevision.urls', namespace='prevision')),
    path('formas-pago/', include('formas_pago.urls', namespace='formas_pago')),
    path('laboratorios/', include(('lab_dental.urls', 'lab_dental'), namespace='lab_dental')),
    path('empresas/', include(('empresa.urls', 'empresa'), namespace='empresa')),
    path('usuarios/', include(('usuarios.urls', 'usuarios'), namespace='usuarios')),
    path('test-format/', test_format, name='test_format'),
    path('login/', auth_views.LoginView.as_view(
        template_name='core/login.html',
        extra_context=get_empresa_config()
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # URLs para recuperación de contraseña
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='core/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='core/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='core/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='core/password_reset_complete.html'), name='password_reset_complete'),
    
    # URL para registro
    path('register/', views.register, name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 