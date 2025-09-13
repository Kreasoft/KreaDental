# 🚀 Migración a PostgreSQL - KreaDental Cloud

## Resumen

Este proyecto ha sido configurado para migrar de SQLite a PostgreSQL, proporcionando mejor rendimiento, escalabilidad y características avanzadas para el sistema de gestión dental.

## 📋 Archivos de Migración

### Scripts Principales
- `migrate_to_postgresql.py` - Script principal de migración automatizada
- `config_database.py` - Configuración de la base de datos PostgreSQL
- `backup_sqlite.py` - Creación de respaldos de SQLite
- `migrate_data.py` - Migración de datos específica

### Archivos de Configuración
- `config/settings.py` - Configuración actualizada para PostgreSQL
- `requirements.txt` - Dependencias actualizadas
- `.env` - Variables de entorno (crear manualmente)

### Documentación
- `MIGRACION_POSTGRESQL.md` - Guía detallada de migración
- `README_MIGRACION.md` - Este archivo

## 🚀 Inicio Rápido

### 1. Instalar PostgreSQL
```bash
# Windows: Descargar desde https://www.postgresql.org/download/windows/
# Linux: sudo apt install postgresql postgresql-contrib
```

### 2. Configurar Variables de Entorno
Crear archivo `.env`:
```env
DB_NAME=kreadental_cloud
DB_USER=postgres
DB_PASSWORD=tu_password_aqui
DB_HOST=localhost
DB_PORT=5432
```

### 3. Ejecutar Migración Automática
```bash
python migrate_to_postgresql.py
```

## 🔧 Migración Manual

Si prefieres hacer la migración paso a paso:

### 1. Crear Respaldo
```bash
python backup_sqlite.py
```

### 2. Exportar Datos
```bash
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission > datos_exportados.json
```

### 3. Configurar PostgreSQL
```bash
python config_database.py
```

### 4. Aplicar Migraciones
```bash
python manage.py migrate
```

### 5. Importar Datos
```bash
python manage.py loaddata datos_exportados.json
```

## ✅ Verificación

Después de la migración, verifica que todo funcione:

```bash
# Ejecutar servidor
python manage.py runserver

# Verificar en el navegador
# http://localhost:8000
```

## 🆘 Solución de Problemas

### Error de Conexión
- Verificar que PostgreSQL esté ejecutándose
- Verificar credenciales en `.env`
- Verificar que el puerto 5432 esté disponible

### Error de Permisos
- Asegurar que el usuario `postgres` tenga permisos
- En Linux: `sudo -u postgres psql`

### Error de Datos
- Verificar que `datos_exportados.json` existe
- Revisar logs de Django para errores específicos

## 📊 Beneficios de PostgreSQL

- **Rendimiento**: Mejor para aplicaciones con muchos usuarios
- **Escalabilidad**: Soporte para grandes volúmenes de datos
- **Características Avanzadas**: Índices, vistas, procedimientos almacenados
- **Concurrencia**: Mejor manejo de múltiples usuarios simultáneos
- **Integridad**: Mejor control de transacciones y consistencia

## 🔄 Rollback

Si necesitas volver a SQLite:

1. Restaurar configuración en `config/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

2. Restaurar respaldo:
```bash
cp backups/db_backup_YYYYMMDD_HHMMSS.sqlite3 db.sqlite3
```

## 📞 Soporte

Si encuentras problemas durante la migración:

1. Revisar logs de Django
2. Verificar configuración de PostgreSQL
3. Consultar `MIGRACION_POSTGRESQL.md` para detalles
4. Verificar que todas las dependencias estén instaladas

---

**¡La migración a PostgreSQL está lista!** 🎉



## Resumen

Este proyecto ha sido configurado para migrar de SQLite a PostgreSQL, proporcionando mejor rendimiento, escalabilidad y características avanzadas para el sistema de gestión dental.

## 📋 Archivos de Migración

### Scripts Principales
- `migrate_to_postgresql.py` - Script principal de migración automatizada
- `config_database.py` - Configuración de la base de datos PostgreSQL
- `backup_sqlite.py` - Creación de respaldos de SQLite
- `migrate_data.py` - Migración de datos específica

### Archivos de Configuración
- `config/settings.py` - Configuración actualizada para PostgreSQL
- `requirements.txt` - Dependencias actualizadas
- `.env` - Variables de entorno (crear manualmente)

### Documentación
- `MIGRACION_POSTGRESQL.md` - Guía detallada de migración
- `README_MIGRACION.md` - Este archivo

## 🚀 Inicio Rápido

### 1. Instalar PostgreSQL
```bash
# Windows: Descargar desde https://www.postgresql.org/download/windows/
# Linux: sudo apt install postgresql postgresql-contrib
```

### 2. Configurar Variables de Entorno
Crear archivo `.env`:
```env
DB_NAME=kreadental_cloud
DB_USER=postgres
DB_PASSWORD=tu_password_aqui
DB_HOST=localhost
DB_PORT=5432
```

### 3. Ejecutar Migración Automática
```bash
python migrate_to_postgresql.py
```

## 🔧 Migración Manual

Si prefieres hacer la migración paso a paso:

### 1. Crear Respaldo
```bash
python backup_sqlite.py
```

### 2. Exportar Datos
```bash
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission > datos_exportados.json
```

### 3. Configurar PostgreSQL
```bash
python config_database.py
```

### 4. Aplicar Migraciones
```bash
python manage.py migrate
```

### 5. Importar Datos
```bash
python manage.py loaddata datos_exportados.json
```

## ✅ Verificación

Después de la migración, verifica que todo funcione:

```bash
# Ejecutar servidor
python manage.py runserver

# Verificar en el navegador
# http://localhost:8000
```

## 🆘 Solución de Problemas

### Error de Conexión
- Verificar que PostgreSQL esté ejecutándose
- Verificar credenciales en `.env`
- Verificar que el puerto 5432 esté disponible

### Error de Permisos
- Asegurar que el usuario `postgres` tenga permisos
- En Linux: `sudo -u postgres psql`

### Error de Datos
- Verificar que `datos_exportados.json` existe
- Revisar logs de Django para errores específicos

## 📊 Beneficios de PostgreSQL

- **Rendimiento**: Mejor para aplicaciones con muchos usuarios
- **Escalabilidad**: Soporte para grandes volúmenes de datos
- **Características Avanzadas**: Índices, vistas, procedimientos almacenados
- **Concurrencia**: Mejor manejo de múltiples usuarios simultáneos
- **Integridad**: Mejor control de transacciones y consistencia

## 🔄 Rollback

Si necesitas volver a SQLite:

1. Restaurar configuración en `config/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

2. Restaurar respaldo:
```bash
cp backups/db_backup_YYYYMMDD_HHMMSS.sqlite3 db.sqlite3
```

## 📞 Soporte

Si encuentras problemas durante la migración:

1. Revisar logs de Django
2. Verificar configuración de PostgreSQL
3. Consultar `MIGRACION_POSTGRESQL.md` para detalles
4. Verificar que todas las dependencias estén instaladas

---

**¡La migración a PostgreSQL está lista!** 🎉






