"""
URL configuration for dental project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('pacientes/', include('pacientes.urls')),
    path('profesionales/', include('profesionales.urls')),
    path('configuracion/', include('configuracion.urls', namespace='configuracion')),
    path('especialidades/', include('especialidades.urls')),
    path('procedimientos/', include('procedimientos.urls')),
    path('citas/', include('citas.urls')),
    path('tratamientos/', include('tratamientos.urls')),
    path('informes/', include('informes.urls')),
    path('previsiones/', include('prevision.urls')),
    path('formas-pago/', include('formas_pago.urls')),
    path('pagos/', include('pagos_tratamientos.urls', namespace='pagos_tratamientos')),
    path('cierres-caja/', include(('cierres_caja.urls', 'cierres_caja'), namespace='cierres_caja')),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
