#!/bin/bash

# Script de configuración inicial para KreaDental-Cloud en producción
# Uso: sudo ./setup_production.sh

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para logging
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Verificar que se ejecute como root
if [ "$EUID" -ne 0 ]; then
    error "Este script debe ejecutarse como root (sudo)"
    exit 1
fi

# Configuración
PROJECT_DIR="/var/www/kreadental"
BACKUP_DIR="/var/backups/kreadental"
DB_NAME="kreadental_prod"
DB_USER="kreadental_user"

log "🚀 Iniciando configuración de KreaDental-Cloud para producción"

# 1. Actualizar sistema
log "📦 Actualizando sistema..."
apt update && apt upgrade -y
success "Sistema actualizado"

# 2. Instalar dependencias base
log "📦 Instalando dependencias base..."
apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx git curl ufw fail2ban
success "Dependencias instaladas"

# 3. Crear usuario para la aplicación
log "👤 Creando usuario kreadental..."
if ! id "kreadental" &>/dev/null; then
    adduser --system --group kreadental
    success "Usuario kreadental creado"
else
    warning "Usuario kreadental ya existe"
fi

# 4. Crear directorios
log "📁 Creando directorios..."
mkdir -p "$PROJECT_DIR"
mkdir -p "$BACKUP_DIR"
mkdir -p "$PROJECT_DIR/logs"
chown -R kreadental:kreadental "$PROJECT_DIR"
chown -R kreadental:kreadental "$BACKUP_DIR"
success "Directorios creados"

# 5. Configurar PostgreSQL
log "🗄️ Configurando PostgreSQL..."

# Crear usuario y base de datos
sudo -u postgres psql << EOF
-- Crear usuario si no existe
DO \$\$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$DB_USER') THEN
        CREATE USER $DB_USER WITH PASSWORD 'temp_password_change_me';
    END IF;
END
\$\$;

-- Crear base de datos si no existe
SELECT 'CREATE DATABASE $DB_NAME OWNER $DB_USER'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$DB_NAME')\gexec

-- Otorgar permisos
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
EOF

success "PostgreSQL configurado"

# 6. Configurar firewall
log "🔥 Configurando firewall..."
ufw --force enable
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
success "Firewall configurado"

# 7. Configurar fail2ban
log "🛡️ Configurando fail2ban..."
cat > /etc/fail2ban/jail.local << EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log
maxretry = 3

[nginx-http-auth]
enabled = true
filter = nginx-http-auth
port = http,https
logpath = /var/log/nginx/error.log
maxretry = 3
EOF

systemctl enable fail2ban
systemctl restart fail2ban
success "Fail2ban configurado"

# 8. Configurar Nginx
log "🌐 Configurando Nginx..."
# Eliminar sitio por defecto
rm -f /etc/nginx/sites-enabled/default

# Crear configuración básica de Nginx
cat > /etc/nginx/sites-available/kreadental << 'EOF'
server {
    listen 80;
    server_name _;

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
EOF

ln -sf /etc/nginx/sites-available/kreadental /etc/nginx/sites-enabled/
nginx -t
systemctl enable nginx
systemctl restart nginx
success "Nginx configurado"

# 9. Configurar servicios systemd
log "⚙️ Configurando servicios systemd..."

# Copiar archivos de configuración de systemd
cp kreadental.service /etc/systemd/system/
cp kreadental.socket /etc/systemd/system/

systemctl daemon-reload
systemctl enable kreadental.socket
systemctl enable kreadental.service
success "Servicios systemd configurados"

# 10. Configurar cron para backups
log "📅 Configurando tareas programadas..."

# Crear script de backup
cat > /usr/local/bin/kreadental_backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/kreadental"
DB_NAME="kreadental_prod"
DB_USER="kreadental_user"

mkdir -p $BACKUP_DIR

# Backup de la base de datos
pg_dump -h localhost -U $DB_USER $DB_NAME > $BACKUP_DIR/kreadental_$DATE.sql
gzip $BACKUP_DIR/kreadental_$DATE.sql

# Backup de archivos media
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /var/www/kreadental/media/

# Eliminar backups antiguos (más de 30 días)
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete

echo "Backup completado: $DATE"
EOF

chmod +x /usr/local/bin/kreadental_backup.sh

# Agregar tarea cron
(crontab -u kreadental -l 2>/dev/null; echo "0 2 * * * /usr/local/bin/kreadental_backup.sh") | crontab -u kreadental -
success "Tareas programadas configuradas"

# 11. Configurar logrotate
log "📋 Configurando rotación de logs..."
cat > /etc/logrotate.d/kreadental << EOF
/var/www/kreadental/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 kreadental kreadental
    postrotate
        systemctl reload kreadental.service > /dev/null 2>&1 || true
    endscript
}
EOF
success "Rotación de logs configurada"

# 12. Crear archivo .env de ejemplo
log "📝 Creando archivo de configuración de ejemplo..."
cat > "$PROJECT_DIR/.env.example" << 'EOF'
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
DEFAULT_FROM_EMAIL=noreply@tu-dominio.com
EOF

chown kreadental:kreadental "$PROJECT_DIR/.env.example"
success "Archivo de configuración de ejemplo creado"

# 13. Mostrar resumen
echo ""
success "🎉 Configuración inicial completada!"
echo ""
echo "📋 Resumen de la configuración:"
echo "   - Usuario: kreadental"
echo "   - Directorio: $PROJECT_DIR"
echo "   - Base de datos: $DB_NAME"
echo "   - Usuario DB: $DB_USER"
echo "   - Backup: $BACKUP_DIR"
echo ""
echo "🔧 Próximos pasos:"
echo "   1. Clonar el repositorio en $PROJECT_DIR"
echo "   2. Crear archivo .env basado en .env.example"
echo "   3. Cambiar la contraseña de la base de datos"
echo "   4. Instalar dependencias Python"
echo "   5. Aplicar migraciones"
echo "   6. Ejecutar ./deploy.sh"
echo ""
echo "⚠️  IMPORTANTE:"
echo "   - Cambiar la contraseña de PostgreSQL:"
echo "     sudo -u postgres psql"
echo "     ALTER USER $DB_USER PASSWORD 'nueva_password_segura';"
echo ""
echo "   - Configurar el archivo .env con tus datos reales"
echo ""
echo "📚 Documentación completa en GUIA_PRODUCCION.md"

log "Configuración inicial completada exitosamente"
