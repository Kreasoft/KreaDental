# KreaDental Cloud - Sistema de Despliegue

## 🚀 Sistema Listo para Producción

### 📋 Características del Sistema

- **Sistema de Citas** - Gestión completa de citas médicas
- **Gestión de Pacientes** - Historial clínico y tratamientos
- **Profesionales** - Gestión de profesionales y especialidades
- **Tratamientos** - Seguimiento de tratamientos y procedimientos
- **Cierres de Caja** - Sistema de caja con retiros
- **Informes** - Reportes financieros y estadísticos
- **Configuración** - Gestión de empresas y sucursales

### 🛠️ Instalación

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements_production.txt
   ```

2. **Configurar base de datos:**
   - Editar `config/settings.py` con credenciales de PostgreSQL
   - Ejecutar migraciones: `python manage.py migrate`

3. **Crear superusuario:**
   ```bash
   python manage.py createsuperuser
   ```

4. **Recopilar archivos estáticos:**
   ```bash
   python manage.py collectstatic --noinput
   ```

5. **Ejecutar servidor:**
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

### 🔧 Configuración de Producción

- **Base de datos:** PostgreSQL
- **Servidor:** Gunicorn (recomendado)
- **Archivos estáticos:** Nginx (recomendado)
- **Variables de entorno:** Configurar en `config/settings.py`

### 📁 Estructura del Sistema

```
deploy_kreadental_final/
├── config/                 # Configuración Django
├── templates/              # Templates HTML
├── static/                 # Archivos estáticos
├── media/                  # Archivos de medios
├── cierres_caja/          # Módulo de cierres de caja
├── citas/                 # Módulo de citas
├── pacientes/             # Módulo de pacientes
├── profesionales/         # Módulo de profesionales
├── tratamientos/          # Módulo de tratamientos
├── informes/              # Módulo de informes
├── manage.py              # Script de Django
├── requirements_production.txt
└── README_DEPLOY.md
```

### 🌐 Acceso al Sistema

- **URL:** http://localhost:8000
- **Admin:** http://localhost:8000/admin
- **Usuario por defecto:** Configurar con `createsuperuser`

### 📞 Soporte

Para soporte técnico, contactar al administrador del sistema.

---
**KreaDental Cloud v2.0** - Sistema de Gestión Dental Completo
