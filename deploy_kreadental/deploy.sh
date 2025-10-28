#!/bin/bash

# KreaDental Cloud - Script de Despliegue
# Sistema de Gestión Dental Completo

echo "🚀 Iniciando despliegue de KreaDental Cloud..."

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado. Por favor instalar Python 3.8+"
    exit 1
fi

# Verificar pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 no está instalado. Por favor instalar pip"
    exit 1
fi

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements_production.txt

# Configurar base de datos
echo "🗄️ Configurando base de datos..."
python manage.py makemigrations
python manage.py migrate

# Crear superusuario
echo "👤 Creando superusuario..."
python manage.py createsuperuser --noinput --username admin --email admin@kreadental.com

# Recopilar archivos estáticos
echo "📁 Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

# Crear directorio de medios
echo "📂 Creando directorio de medios..."
mkdir -p media/avatars media/empresas media/logos

# Configurar permisos
echo "🔐 Configurando permisos..."
chmod 755 media/
chmod 755 static/

echo "✅ Despliegue completado exitosamente!"
echo ""
echo "🌐 Para iniciar el servidor:"
echo "   source venv/bin/activate"
echo "   python manage.py runserver 0.0.0.0:8000"
echo ""
echo "👤 Usuario administrador:"
echo "   Usuario: admin"
echo "   Email: admin@kreadental.com"
echo "   Contraseña: (configurar manualmente)"
echo ""
echo "📖 Para más información, ver README_DEPLOY.md"
