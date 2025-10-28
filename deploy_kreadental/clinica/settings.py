INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Tus apps
    'core',
    'citas',
    'prevision',
    'pacientes',
    'profesionales',
    'empresa',
    'tratamientos',  
    'procedimientos',
] 

# Configuración de formato de fecha
DATE_FORMAT = 'Y-m-d'
DATE_INPUT_FORMATS = ['%Y-%m-%d']
TIME_FORMAT = 'H:i'
TIME_INPUT_FORMATS = ['%H:%M']

USE_L10N = False  # Deshabilitar localización para usar nuestros formatos
USE_I18N = True 