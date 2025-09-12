# 🚀 Guía Completa para Pasar KreaDental-Cloud a Producción

## 📋 Índice
1. [Requisitos del Sistema](#requisitos-del-sistema)
2. [Configuración del Servidor](#configuración-del-servidor)
3. [Base de Datos PostgreSQL](#base-de-datos-postgresql)
4. [Configuración de Django para Producción](#configuración-de-django-para-producción)
5. [Servidor Web (Nginx + Gunicorn)](#servidor-web-nginx--gunicorn)
6. [SSL/HTTPS](#sslhttps)
7. [Backup y Monitoreo](#backup-y-monitoreo)
8. [Despliegue Automatizado](#despliegue-automatizado)
9. [Checklist de Producción](#checklist-de-producción)

---

## 🖥️ Requisitos del Sistema

### **Servidor Mínimo Recomendado:**
- **CPU:** 2 cores
- **RAM:** 4GB mínimo, 8GB recomendado
- **Almacenamiento:** 50GB SSD
- **Sistema Operativo:** Ubuntu 20.04 LTS o superior

### **Software Requerido:**
- Python 3.9+
- PostgreSQL 12+
- Nginx
- Git
- Certbot (para SSL)

---

## 🖥️ Configuración del Servidor

### **1. Actualizar el Sistema**
```bash
sudo apt update && sudo apt upgrade -y
```

### **2. Instalar Dependencias Base**
```bash
sudo apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx git curl
```

### **3. Crear Usuario para la Aplicación**
```bash
sudo adduser --system --group kreadental
sudo mkdir -p /var/www/kreadental
sudo chown kreadental:kreadental /var/www/kreadental
```

---

## 🗄️ Base de Datos PostgreSQL

### **1. Configurar PostgreSQL**
```bash
sudo -u postgres psql
```

```sql
-- Crear usuario y base de datos
CREATE USER kreadental_user WITH PASSWORD 'tu_password_seguro_aqui';
CREATE DATABASE kreadental_prod OWNER kreadental_user;
GRANT ALL PRIVILEGES ON DATABASE kreadental_prod TO kreadental_user;
\q
```

### **2. Configurar Conexiones**
```bash
sudo nano /etc/postgresql/*/main/postgresql.conf
```

Buscar y modificar:
```
listen_addresses = 'localhost'
```

```bash
sudo nano /etc/postgresql/*/main/pg_hba.conf
```

Agregar:
```
local   kreadental_prod   kreadental_user   md5
```

```bash
sudo systemctl restart postgresql
```

---

## ⚙️ Configuración de Django para Producción

### **1. Clonar el Repositorio**
```bash
cd /var/www/kreadental
sudo -u kreadental git clone https://github.com/Kreasoft/KreaDental.git .
```

### **2. Crear Entorno Virtual**
```bash
sudo -u kreadental python3 -m venv venv
sudo -u kreadental /var/www/kreadental/venv/bin/pip install --upgrade pip
```

### **3. Instalar Dependencias**
```bash
sudo -u kreadental /var/www/kreadental/venv/bin/pip install -r requirements.txt
sudo -u kreadental /var/www/kreadental/venv/bin/pip install gunicorn
```

### **4. Crear Archivo de Configuración de Producción**

Crear `config/settings_production.py`:
```python
import os
from .settings import *
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'cambiar-por-clave-secreta-muy-segura')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['tu-dominio.com', 'www.tu-dominio.com', 'IP_DEL_SERVIDOR']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'kreadental_prod'),
        'USER': os.getenv('DB_USER', 'kreadental_user'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# HTTPS settings (descomentar cuando tengas SSL)
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
```

### **5. Crear Archivo de Variables de Entorno**
```bash
sudo -u kreadental nano /var/www/kreadental/.env
```

```env
# Configuración de Django
SECRET_KEY=tu-clave-secreta-muy-segura-de-al-menos-50-caracteres
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com

# Configuración de PostgreSQL
DB_NAME=kreadental_prod
DB_USER=kreadental_user
DB_PASSWORD=tu_password_seguro_aqui
DB_HOST=localhost
DB_PORT=5432

# Configuración de Email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-password-de-aplicacion
```

### **6. Configurar Archivos Estáticos y Media**
```bash
sudo -u kreadental mkdir -p /var/www/kreadental/logs
sudo -u kreadental mkdir -p /var/www/kreadental/media
sudo -u kreadental /var/www/kreadental/venv/bin/python manage.py collectstatic --noinput --settings=config.settings_production
```

### **7. Aplicar Migraciones**
```bash
sudo -u kreadental /var/www/kreadental/venv/bin/python manage.py migrate --settings=config.settings_production
sudo -u kreadental /var/www/kreadental/venv/bin/python manage.py createsuperuser --settings=config.settings_production
```

---

## 🌐 Servidor Web (Nginx + Gunicorn)

### **1. Crear Archivo de Configuración de Gunicorn**
```bash
sudo -u kreadental nano /var/www/kreadental/gunicorn_config.py
```

```python
# Gunicorn configuration file
import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2

# Logging
accesslog = "/var/www/kreadental/logs/gunicorn_access.log"
errorlog = "/var/www/kreadental/logs/gunicorn_error.log"
loglevel = "info"

# Process naming
proc_name = "kreadental_gunicorn"

# Server mechanics
daemon = False
pidfile = "/var/www/kreadental/gunicorn.pid"
user = "kreadental"
group = "kreadental"
tmp_upload_dir = None

# SSL (descomentar cuando tengas certificados)
# keyfile = "/etc/ssl/private/kreadental.key"
# certfile = "/etc/ssl/certs/kreadental.crt"
```

### **2. Crear Archivo de Configuración de Nginx**
```bash
sudo nano /etc/nginx/sites-available/kreadental
```

```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;

    # Redirección a HTTPS (descomentar cuando tengas SSL)
    # return 301 https://$server_name$request_uri;

    # Configuración temporal para HTTP (eliminar cuando tengas SSL)
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/kreadental/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /var/www/kreadental/media/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
}

# Configuración HTTPS (descomentar cuando tengas SSL)
# server {
#     listen 443 ssl http2;
#     server_name tu-dominio.com www.tu-dominio.com;
# 
#     ssl_certificate /etc/letsencrypt/live/tu-dominio.com/fullchain.pem;
#     ssl_certificate_key /etc/letsencrypt/live/tu-dominio.com/privkey.pem;
#     ssl_protocols TLSv1.2 TLSv1.3;
#     ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
#     ssl_prefer_server_ciphers off;
#     ssl_session_cache shared:SSL:10m;
#     ssl_session_timeout 10m;
# 
#     location / {
#         proxy_pass http://127.0.0.1:8000;
#         proxy_set_header Host $host;
#         proxy_set_header X-Real-IP $remote_addr;
#         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#         proxy_set_header X-Forwarded-Proto $scheme;
#     }
# 
#     location /static/ {
#         alias /var/www/kreadental/staticfiles/;
#         expires 1y;
#         add_header Cache-Control "public, immutable";
#     }
# 
#     location /media/ {
#         alias /var/www/kreadental/media/;
#         expires 1y;
#         add_header Cache-Control "public, immutable";
#     }
# 
#     # Security headers
#     add_header X-Frame-Options "SAMEORIGIN" always;
#     add_header X-XSS-Protection "1; mode=block" always;
#     add_header X-Content-Type-Options "nosniff" always;
#     add_header Referrer-Policy "no-referrer-when-downgrade" always;
#     add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
#     add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
# }
```

### **3. Habilitar el Sitio**
```bash
sudo ln -s /etc/nginx/sites-available/kreadental /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 🔒 SSL/HTTPS

### **1. Instalar Certbot**
```bash
sudo apt install certbot python3-certbot-nginx
```

### **2. Obtener Certificado SSL**
```bash
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com
```

### **3. Configurar Renovación Automática**
```bash
sudo crontab -e
```

Agregar:
```
0 12 * * * /usr/bin/certbot renew --quiet
```

---

## 📊 Backup y Monitoreo

### **1. Script de Backup de Base de Datos**
```bash
sudo -u kreadental nano /var/www/kreadental/backup_db.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/kreadental"
DB_NAME="kreadental_prod"

mkdir -p $BACKUP_DIR

# Backup de la base de datos
pg_dump -h localhost -U kreadental_user $DB_NAME > $BACKUP_DIR/kreadental_$DATE.sql

# Backup de archivos media
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /var/www/kreadental/media/

# Eliminar backups antiguos (más de 30 días)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete

echo "Backup completado: $DATE"
```

```bash
sudo chmod +x /var/www/kreadental/backup_db.sh
sudo crontab -e
```

Agregar:
```
0 2 * * * /var/www/kreadental/backup_db.sh
```

### **2. Monitoreo con Systemd**
```bash
sudo nano /etc/systemd/system/kreadental.service
```

```ini
[Unit]
Description=KreaDental Gunicorn daemon
Requires=kreadental.socket
After=network.target

[Service]
Type=notify
User=kreadental
Group=kreadental
RuntimeDirectory=kreadental
WorkingDirectory=/var/www/kreadental
ExecStart=/var/www/kreadental/venv/bin/gunicorn --config gunicorn_config.py config.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=10
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

```bash
sudo nano /etc/systemd/system/kreadental.socket
```

```ini
[Unit]
Description=KreaDental socket

[Socket]
ListenStream=/run/kreadental.sock
SocketUser=www-data
SocketMode=600

[Install]
WantedBy=sockets.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable kreadental.socket
sudo systemctl start kreadental.socket
sudo systemctl enable kreadental.service
sudo systemctl start kreadental.service
```

---

## 🚀 Despliegue Automatizado

### **1. Script de Despliegue**
```bash
sudo -u kreadental nano /var/www/kreadental/deploy.sh
```

```bash
#!/bin/bash
set -e

echo "🚀 Iniciando despliegue de KreaDental-Cloud..."

# Ir al directorio del proyecto
cd /var/www/kreadental

# Activar entorno virtual
source venv/bin/activate

# Hacer backup de la base de datos antes del despliegue
echo "📦 Creando backup de la base de datos..."
./backup_db.sh

# Obtener últimos cambios
echo "📥 Obteniendo últimos cambios..."
git pull origin master

# Instalar/actualizar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# Aplicar migraciones
echo "🔄 Aplicando migraciones..."
python manage.py migrate --settings=config.settings_production

# Recopilar archivos estáticos
echo "🎨 Recopilando archivos estáticos..."
python manage.py collectstatic --noinput --settings=config.settings_production

# Reiniciar servicios
echo "🔄 Reiniciando servicios..."
sudo systemctl restart kreadental.service
sudo systemctl reload nginx

echo "✅ Despliegue completado exitosamente!"
```

```bash
sudo chmod +x /var/www/kreadental/deploy.sh
```

---

## ✅ Checklist de Producción

### **🔒 Seguridad**
- [ ] SECRET_KEY seguro y único
- [ ] DEBUG = False
- [ ] ALLOWED_HOSTS configurado correctamente
- [ ] HTTPS/SSL configurado
- [ ] Headers de seguridad en Nginx
- [ ] Usuario de base de datos con permisos mínimos
- [ ] Firewall configurado (ufw)
- [ ] Actualizaciones automáticas del sistema

### **🗄️ Base de Datos**
- [ ] PostgreSQL instalado y configurado
- [ ] Base de datos creada
- [ ] Usuario con permisos apropiados
- [ ] Backup automático configurado
- [ ] Migraciones aplicadas

### **🌐 Servidor Web**
- [ ] Nginx instalado y configurado
- [ ] Gunicorn configurado
- [ ] Archivos estáticos servidos correctamente
- [ ] Logs configurados
- [ ] Servicios iniciados y habilitados

### **📊 Monitoreo**
- [ ] Logs de aplicación configurados
- [ ] Logs de Nginx configurados
- [ ] Logs de Gunicorn configurados
- [ ] Monitoreo de recursos del servidor
- [ ] Alertas de error configuradas

### **🔄 Mantenimiento**
- [ ] Script de despliegue automatizado
- [ ] Backup automático de base de datos
- [ ] Backup de archivos media
- [ ] Limpieza automática de logs antiguos
- [ ] Renovación automática de SSL

### **🧪 Pruebas**
- [ ] Aplicación accesible desde el navegador
- [ ] Login funcionando correctamente
- [ ] Todas las funcionalidades probadas
- [ ] Archivos estáticos cargando correctamente
- [ ] Base de datos funcionando
- [ ] SSL/HTTPS funcionando (si aplica)

---

## 🆘 Solución de Problemas Comunes

### **Error de Permisos**
```bash
sudo chown -R kreadental:kreadental /var/www/kreadental
sudo chmod -R 755 /var/www/kreadental
```

### **Error de Base de Datos**
```bash
# Verificar conexión
sudo -u kreadental psql -h localhost -U kreadental_user -d kreadental_prod

# Verificar logs
sudo journalctl -u postgresql
```

### **Error de Nginx**
```bash
# Verificar configuración
sudo nginx -t

# Ver logs
sudo tail -f /var/log/nginx/error.log
```

### **Error de Gunicorn**
```bash
# Verificar estado
sudo systemctl status kreadental.service

# Ver logs
sudo journalctl -u kreadental.service -f
```

---

## 📞 Soporte

Para soporte técnico o consultas sobre el despliegue en producción:
- **GitHub Issues:** https://github.com/Kreasoft/KreaDental/issues
- **Documentación:** Ver archivos README en el repositorio
- **Logs:** Revisar `/var/www/kreadental/logs/` para errores específicos

---

**¡Tu aplicación KreaDental-Cloud está lista para producción! 🎉**
