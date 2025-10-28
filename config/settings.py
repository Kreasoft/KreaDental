import os
from pathlib import Path
import locale
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-your-secret-key-here')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'jazzmin',  # Debe ir antes de django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_extensions',
    'core',
    'citas',
    'pacientes',
    'profesionales',
    'especialidades',
    'procedimientos',
    'tratamientos',
    'pagos_tratamientos',
    'informes',
    'prevision',
    'formas_pago',
    'cierres_caja.apps.CierresCajaConfig',
    'configuracion',
    'lab_dental',
    'usuarios',  # Aplicación de usuarios personalizados
    'empresa',   # Aplicación de empresas
]

# Configuración de autenticación personalizada
AUTH_USER_MODEL = 'usuarios.Usuario'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'empresa.middleware.EmpresaMiddleware',  # Comentado temporalmente
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'empresa.context_processors.empresa_actual',
                'empresa.context_processors.sucursal_actual',
                'empresa.context_processors.sucursales_disponibles',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_TZ = True

# Configuración para formato de números
USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = ','
DECIMAL_SEPARATOR = '.'
NUMBER_GROUPING = 3

# Configuración de locale para formato de números
try:
    locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'Spanish_Chile.1252')
    except:
        pass

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login URL
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'core:home'
LOGOUT_REDIRECT_URL = 'login'

# Configuración del Admin de Django
ADMIN_SITE_HEADER = "KreaDental Cloud - Administración"
ADMIN_SITE_TITLE = "KreaDental Cloud"
ADMIN_INDEX_TITLE = "Panel de Administración"

# Configuración de templates del admin
ADMIN_TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates', 'admin')

# Configuración de Jazzmin
JAZZMIN_SETTINGS = {
    # Título del sitio
    "site_title": "KreaDental Cloud",
    "site_header": "KreaDental Cloud",
    "site_brand": "KreaDental Cloud",
    "site_logo": None,
    "site_logo_classes": "img-circle",
    "site_icon": None,
    
    # Colores del tema dental
    "brand_colour": "#1A5276",  # Dental primary
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "cosmo",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    
    # Personalización del menú
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "admin.LogEntry": "fas fa-file",
        "citas.Cita": "fas fa-calendar-alt",
        "pacientes.Paciente": "fas fa-user-injured",
        "profesionales.Profesional": "fas fa-user-md",
        "especialidades.Especialidad": "fas fa-stethoscope",
        "procedimientos.Procedimiento": "fas fa-tooth",
        "tratamientos.Tratamiento": "fas fa-teeth",
        "pagos_tratamientos.PagoTratamiento": "fas fa-credit-card",
        "informes": "fas fa-chart-bar",
        "prevision.Prevision": "fas fa-shield-alt",
        "formas_pago.FormaPago": "fas fa-money-bill-wave",
        "cierres_caja.CierreCaja": "fas fa-cash-register",
        "configuracion.ConfiguracionEmpresa": "fas fa-cog",
        "lab_dental.Laboratorio": "fas fa-flask",
        "usuarios.Usuario": "fas fa-user-circle",
        "empresa.Empresa": "fas fa-building",
        "empresa.Sucursal": "fas fa-map-marker-alt",
    },
    
    # Orden de las aplicaciones
    "order_with_respect_to": [
        "auth",
        "citas",
        "pacientes", 
        "profesionales",
        "especialidades",
        "procedimientos",
        "tratamientos",
        "pagos_tratamientos",
        "informes",
        "prevision",
        "formas_pago",
        "cierres_caja",
        "configuracion",
        "lab_dental",
        "usuarios",
        "empresa",
    ],
    
    # Personalización de la barra superior
    "show_ui_builder": True,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
    
    # Textos personalizados
    "welcome_sign": "Bienvenido a KreaDental Cloud",
    "copyright": "KreaDental Cloud Ltd",
    "search_model": ["auth.User", "pacientes.Paciente"],
    
    # Configuración de usuario
    "user_avatar": None,
    "show_full_result_count": False,
    "show_ui_builder": True,
    
    # Colores personalizados del tema dental
    "custom_css": "css/jazzmin-dental-theme.css",
    "custom_js": None,
    "show_ui_builder": True,
    
    # Configuración de colores específicos
    "navbar_color": "#1A5276",  # Dental primary
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "cosmo",
    "dark_mode_theme": None,
}

# Configuración de UI Builder de Jazzmin con colores del tema dental
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "#1A5276",  # Dental primary
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "cosmo",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}

# Configuración de localización para separadores de miles
USE_L10N = True
USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = '.'
NUMBER_GROUPING = 3

# Configuración de impresora
PRINTER_TYPE = 'THERMAL'  # 'THERMAL' o 'LASER'
THERMAL_PRINTER_WIDTH = 80  # Ancho en caracteres para impresora térmica