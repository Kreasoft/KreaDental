# Migración a PostgreSQL - KreaDental Cloud

## Pasos para migrar de SQLite a PostgreSQL

### 1. Instalar PostgreSQL

#### Windows:
1. Descargar PostgreSQL desde: https://www.postgresql.org/download/windows/
2. Instalar con las opciones por defecto
3. Recordar la contraseña del usuario `postgres`

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### 2. Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
# Configuración de PostgreSQL
DB_NAME=kreadental_cloud
DB_USER=postgres
DB_PASSWORD=tu_password_aqui
DB_HOST=localhost
DB_PORT=5432

# Configuración de Django
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Importante:** Reemplazar `tu_password_aqui` con la contraseña real de PostgreSQL.

### 3. Crear la base de datos

Ejecutar el script de configuración:

```bash
python config_database.py
```

### 4. Realizar migraciones

```bash
# Crear las migraciones
python manage.py makemigrations

# Aplicar las migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

### 5. Migrar datos existentes (opcional)

Si tienes datos importantes en SQLite que quieres migrar:

```bash
# Exportar datos de SQLite
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission > datos_exportados.json

# Cambiar temporalmente a SQLite en settings.py
# Aplicar migraciones en PostgreSQL
# Importar datos
python manage.py loaddata datos_exportados.json
```

### 6. Verificar la migración

```bash
# Ejecutar el servidor
python manage.py runserver

# Verificar en el admin que los datos estén correctos
```

## Solución de problemas

### Error de conexión
- Verificar que PostgreSQL esté ejecutándose
- Verificar las credenciales en el archivo `.env`
- Verificar que el puerto 5432 esté disponible

### Error de permisos
- Asegurarse de que el usuario `postgres` tenga permisos para crear bases de datos
- En Linux, usar `sudo -u postgres` si es necesario

### Error de encoding
- PostgreSQL usa UTF-8 por defecto, que es compatible con Django
- No debería haber problemas de encoding

## Archivos modificados

- `config/settings.py`: Configuración de base de datos
- `requirements.txt`: Dependencias de PostgreSQL
- `config_database.py`: Script de configuración (nuevo)
- `.env`: Variables de entorno (crear manualmente)

## Notas importantes

1. **Backup**: Siempre hacer backup de la base de datos SQLite antes de migrar
2. **Testing**: Probar la aplicación completamente después de la migración
3. **Performance**: PostgreSQL puede ser más lento en desarrollo, pero mejor en producción
4. **Escalabilidad**: PostgreSQL es más escalable que SQLite para aplicaciones en producción



## Pasos para migrar de SQLite a PostgreSQL

### 1. Instalar PostgreSQL

#### Windows:
1. Descargar PostgreSQL desde: https://www.postgresql.org/download/windows/
2. Instalar con las opciones por defecto
3. Recordar la contraseña del usuario `postgres`

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### 2. Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
# Configuración de PostgreSQL
DB_NAME=kreadental_cloud
DB_USER=postgres
DB_PASSWORD=tu_password_aqui
DB_HOST=localhost
DB_PORT=5432

# Configuración de Django
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Importante:** Reemplazar `tu_password_aqui` con la contraseña real de PostgreSQL.

### 3. Crear la base de datos

Ejecutar el script de configuración:

```bash
python config_database.py
```

### 4. Realizar migraciones

```bash
# Crear las migraciones
python manage.py makemigrations

# Aplicar las migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

### 5. Migrar datos existentes (opcional)

Si tienes datos importantes en SQLite que quieres migrar:

```bash
# Exportar datos de SQLite
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission > datos_exportados.json

# Cambiar temporalmente a SQLite en settings.py
# Aplicar migraciones en PostgreSQL
# Importar datos
python manage.py loaddata datos_exportados.json
```

### 6. Verificar la migración

```bash
# Ejecutar el servidor
python manage.py runserver

# Verificar en el admin que los datos estén correctos
```

## Solución de problemas

### Error de conexión
- Verificar que PostgreSQL esté ejecutándose
- Verificar las credenciales en el archivo `.env`
- Verificar que el puerto 5432 esté disponible

### Error de permisos
- Asegurarse de que el usuario `postgres` tenga permisos para crear bases de datos
- En Linux, usar `sudo -u postgres` si es necesario

### Error de encoding
- PostgreSQL usa UTF-8 por defecto, que es compatible con Django
- No debería haber problemas de encoding

## Archivos modificados

- `config/settings.py`: Configuración de base de datos
- `requirements.txt`: Dependencias de PostgreSQL
- `config_database.py`: Script de configuración (nuevo)
- `.env`: Variables de entorno (crear manualmente)

## Notas importantes

1. **Backup**: Siempre hacer backup de la base de datos SQLite antes de migrar
2. **Testing**: Probar la aplicación completamente después de la migración
3. **Performance**: PostgreSQL puede ser más lento en desarrollo, pero mejor en producción
4. **Escalabilidad**: PostgreSQL es más escalable que SQLite para aplicaciones en producción





