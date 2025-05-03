from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

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
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 