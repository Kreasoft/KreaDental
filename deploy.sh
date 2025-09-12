#!/bin/bash

# Script de despliegue automatizado para KreaDental-Cloud
# Uso: ./deploy.sh [environment]
# Ejemplo: ./deploy.sh production

set -e  # Salir si algún comando falla

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

# Configuración
ENVIRONMENT=${1:-production}
PROJECT_DIR="/var/www/kreadental"
VENV_DIR="$PROJECT_DIR/venv"
BACKUP_DIR="/var/backups/kreadental"
LOG_FILE="$PROJECT_DIR/logs/deploy.log"

# Crear directorio de logs si no existe
mkdir -p "$PROJECT_DIR/logs"
mkdir -p "$BACKUP_DIR"

# Función para logging en archivo
log_to_file() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Función para hacer backup
make_backup() {
    log "Creando backup de la base de datos..."
    log_to_file "Iniciando backup de base de datos"
    
    DATE=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="$BACKUP_DIR/kreadental_$DATE.sql"
    
    # Backup de la base de datos
    if pg_dump -h localhost -U kreadental_user kreadental_prod > "$BACKUP_FILE" 2>/dev/null; then
        success "Backup de base de datos creado: $BACKUP_FILE"
        log_to_file "Backup de base de datos creado exitosamente"
        
        # Comprimir backup
        gzip "$BACKUP_FILE"
        success "Backup comprimido: $BACKUP_FILE.gz"
        
        # Eliminar backups antiguos (más de 7 días)
        find "$BACKUP_DIR" -name "*.sql.gz" -mtime +7 -delete 2>/dev/null || true
        
    else
        error "Error creando backup de la base de datos"
        log_to_file "Error creando backup de base de datos"
        exit 1
    fi
}

# Función para verificar servicios
check_services() {
    log "Verificando servicios del sistema..."
    
    # Verificar PostgreSQL
    if systemctl is-active --quiet postgresql; then
        success "PostgreSQL está ejecutándose"
    else
        error "PostgreSQL no está ejecutándose"
        exit 1
    fi
    
    # Verificar Nginx
    if systemctl is-active --quiet nginx; then
        success "Nginx está ejecutándose"
    else
        error "Nginx no está ejecutándose"
        exit 1
    fi
}

# Función para actualizar código
update_code() {
    log "Actualizando código desde el repositorio..."
    log_to_file "Iniciando actualización de código"
    
    cd "$PROJECT_DIR"
    
    # Verificar si hay cambios pendientes
    if ! git diff-index --quiet HEAD --; then
        warning "Hay cambios locales sin commit. Haciendo stash..."
        git stash
    fi
    
    # Obtener últimos cambios
    if git pull origin master; then
        success "Código actualizado exitosamente"
        log_to_file "Código actualizado desde repositorio"
    else
        error "Error actualizando código desde el repositorio"
        log_to_file "Error actualizando código desde repositorio"
        exit 1
    fi
}

# Función para instalar dependencias
install_dependencies() {
    log "Instalando/actualizando dependencias..."
    log_to_file "Iniciando instalación de dependencias"
    
    cd "$PROJECT_DIR"
    
    # Activar entorno virtual
    source "$VENV_DIR/bin/activate"
    
    # Actualizar pip
    pip install --upgrade pip
    
    # Instalar dependencias
    if pip install -r requirements.txt; then
        success "Dependencias instaladas exitosamente"
        log_to_file "Dependencias instaladas correctamente"
    else
        error "Error instalando dependencias"
        log_to_file "Error instalando dependencias"
        exit 1
    fi
}

# Función para aplicar migraciones
run_migrations() {
    log "Aplicando migraciones de la base de datos..."
    log_to_file "Iniciando aplicación de migraciones"
    
    cd "$PROJECT_DIR"
    source "$VENV_DIR/bin/activate"
    
    # Verificar migraciones pendientes
    MIGRATIONS=$(python manage.py showmigrations --settings=config.settings_production | grep -c '\[ \]' || true)
    
    if [ "$MIGRATIONS" -gt 0 ]; then
        warning "Hay $MIGRATIONS migraciones pendientes"
        
        # Aplicar migraciones
        if python manage.py migrate --settings=config.settings_production; then
            success "Migraciones aplicadas exitosamente"
            log_to_file "Migraciones aplicadas correctamente"
        else
            error "Error aplicando migraciones"
            log_to_file "Error aplicando migraciones"
            exit 1
        fi
    else
        success "No hay migraciones pendientes"
        log_to_file "No hay migraciones pendientes"
    fi
}

# Función para recopilar archivos estáticos
collect_static() {
    log "Recopilando archivos estáticos..."
    log_to_file "Iniciando recopilación de archivos estáticos"
    
    cd "$PROJECT_DIR"
    source "$VENV_DIR/bin/activate"
    
    # Limpiar archivos estáticos antiguos
    rm -rf "$PROJECT_DIR/staticfiles/*"
    
    # Recopilar archivos estáticos
    if python manage.py collectstatic --noinput --settings=config.settings_production; then
        success "Archivos estáticos recopilados exitosamente"
        log_to_file "Archivos estáticos recopilados correctamente"
    else
        error "Error recopilando archivos estáticos"
        log_to_file "Error recopilando archivos estáticos"
        exit 1
    fi
}

# Función para reiniciar servicios
restart_services() {
    log "Reiniciando servicios..."
    log_to_file "Iniciando reinicio de servicios"
    
    # Reiniciar Gunicorn
    if systemctl is-active --quiet kreadental.service; then
        if systemctl restart kreadental.service; then
            success "Servicio KreaDental reiniciado"
            log_to_file "Servicio KreaDental reiniciado correctamente"
        else
            error "Error reiniciando servicio KreaDental"
            log_to_file "Error reiniciando servicio KreaDental"
            exit 1
        fi
    else
        warning "Servicio KreaDental no está ejecutándose, iniciando..."
        systemctl start kreadental.service
    fi
    
    # Recargar Nginx
    if systemctl reload nginx; then
        success "Nginx recargado"
        log_to_file "Nginx recargado correctamente"
    else
        error "Error recargando Nginx"
        log_to_file "Error recargando Nginx"
        exit 1
    fi
}

# Función para verificar despliegue
verify_deployment() {
    log "Verificando despliegue..."
    log_to_file "Iniciando verificación del despliegue"
    
    # Verificar que los servicios estén ejecutándose
    if systemctl is-active --quiet kreadental.service; then
        success "Servicio KreaDental está ejecutándose"
    else
        error "Servicio KreaDental no está ejecutándose"
        log_to_file "Servicio KreaDental no está ejecutándose"
        exit 1
    fi
    
    # Verificar que Nginx esté ejecutándose
    if systemctl is-active --quiet nginx; then
        success "Nginx está ejecutándose"
    else
        error "Nginx no está ejecutándose"
        log_to_file "Nginx no está ejecutándose"
        exit 1
    fi
    
    # Verificar archivos estáticos
    if [ -d "$PROJECT_DIR/staticfiles" ] && [ "$(ls -A $PROJECT_DIR/staticfiles)" ]; then
        success "Archivos estáticos están presentes"
        log_to_file "Archivos estáticos verificados correctamente"
    else
        error "Archivos estáticos no están presentes"
        log_to_file "Error: archivos estáticos no están presentes"
        exit 1
    fi
    
    success "Verificación del despliegue completada"
    log_to_file "Verificación del despliegue completada exitosamente"
}

# Función para limpiar archivos temporales
cleanup() {
    log "Limpiando archivos temporales..."
    
    cd "$PROJECT_DIR"
    
    # Limpiar archivos Python compilados
    find . -type f -name "*.pyc" -delete
    find . -type d -name "__pycache__" -delete
    
    # Limpiar logs antiguos (más de 30 días)
    find "$PROJECT_DIR/logs" -name "*.log" -mtime +30 -delete 2>/dev/null || true
    
    success "Limpieza completada"
    log_to_file "Limpieza de archivos temporales completada"
}

# Función principal
main() {
    log "🚀 Iniciando despliegue de KreaDental-Cloud en modo $ENVIRONMENT"
    log_to_file "Iniciando proceso de despliegue en modo $ENVIRONMENT"
    
    # Verificar que se ejecute como usuario correcto
    if [ "$USER" != "kreadental" ] && [ "$USER" != "root" ]; then
        error "Este script debe ejecutarse como usuario 'kreadental' o 'root'"
        exit 1
    fi
    
    # Verificar que el directorio del proyecto existe
    if [ ! -d "$PROJECT_DIR" ]; then
        error "Directorio del proyecto no encontrado: $PROJECT_DIR"
        exit 1
    fi
    
    # Ejecutar pasos del despliegue
    check_services
    make_backup
    update_code
    install_dependencies
    run_migrations
    collect_static
    restart_services
    verify_deployment
    cleanup
    
    success "🎉 Despliegue completado exitosamente!"
    log_to_file "Despliegue completado exitosamente"
    
    # Mostrar información del despliegue
    echo ""
    echo "📊 Información del despliegue:"
    echo "   - Ambiente: $ENVIRONMENT"
    echo "   - Directorio: $PROJECT_DIR"
    echo "   - Log: $LOG_FILE"
    echo "   - Backup: $BACKUP_DIR"
    echo ""
    echo "🔗 Servicios:"
    systemctl status kreadental.service --no-pager -l
    echo ""
    systemctl status nginx --no-pager -l
}

# Manejo de señales
trap 'error "Despliegue interrumpido por el usuario"; log_to_file "Despliegue interrumpido por el usuario"; exit 1' INT TERM

# Ejecutar función principal
main "$@"
