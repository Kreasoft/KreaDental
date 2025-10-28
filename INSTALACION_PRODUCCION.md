# Manual de Instalación en Servidor de Producción - KreaDental Cloud

Esta guía detalla los pasos para desplegar la aplicación KreaDental Cloud en un servidor de producción, con instrucciones para **Windows** y **Linux**.

## 1. Prerrequisitos del Servidor

### Para Windows:
- **Python 3.x**: Desde [python.org](https://www.python.org/downloads/). Marcar `Add Python to PATH`.
- **PostgreSQL**: Desde [postgresql.org](https://www.postgresql.org/download/).
- **Git**: Desde [git-scm.com](https://git-scm.com/download/win).

### Para Linux (ejemplos para Debian/Ubuntu):
- **Python 3.x y venv**:
  ```bash
  sudo apt update
  sudo apt install python3 python3-pip python3-venv -y
  ```
- **PostgreSQL y dependencias**:
  ```bash
  sudo apt install postgresql postgresql-contrib libpq-dev -y
  ```
- **Git**:
  ```bash
  sudo apt install git -y
  ```

## 2. Preparación del Código y Repositorio

Asegúrate de que tu archivo `.gitignore` contiene las siguientes líneas para evitar subir archivos innecesarios o sensibles:

```
# Archivos de entorno
.env

# Directorios de Python
__pycache__/
virt/
.venv/

# Directorio de logs
logs/
```

Sube tu proyecto a un repositorio de Git (GitHub, GitLab, etc.).

## 3. Configuración en el Servidor de Producción

### 3.1. Clonar el Repositorio

```bash
git clone <URL_DE_TU_REPOSITORIO_GIT>
cd KreaDental-Cloud
```

### 3.2. Crear y Activar el Entorno Virtual

- **Windows**:
  ```bash
  python -m venv virt
  virt\Scripts\activate
  ```
- **Linux**:
  ```bash
  python3 -m venv virt
  source virt/bin/activate
  ```

### 3.3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 3.4. Crear el Archivo de Entorno (`.env`)

Crea manualmente un archivo `.env` en la raíz del proyecto con el siguiente contenido, reemplazando los valores con los de tu entorno de producción:

```
SECRET_KEY='tu-nueva-clave-secreta-larga-y-dificil-de-adivinar'

DB_NAME=kreadental_prod
DB_USER=postgres
DB_PASSWORD=la_contraseña_de_tu_bd_de_produccion
DB_HOST=localhost
DB_PORT=5432

ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com,localhost,127.0.0.1
```

### 3.5. Preparar la Base de Datos y Archivos Estáticos

```bash
python manage.py migrate --settings=config.settings_production
python manage.py collectstatic --settings=config.settings_production --noinput
```

## 4. Ejecutar la Aplicación como un Servicio

### Para Windows (con Waitress y NSSM)

1.  **Descargar NSSM**: Desde [nssm.cc](https://nssm.cc/download). Copia `nssm.exe` a `C:\Windows\System32`.
2.  **Crear el Servicio**: Abre una terminal **como Administrador** y ejecuta `nssm install KreaDentalCloud`. Se abrirá una GUI.
    -   **Pestaña `Application`**:
        -   **Path**: La ruta completa al ejecutable de `waitress`. Ejemplo: `C:\ruta\a\tu\proyecto\KreaDental-Cloud\virt\Scripts\waitress-serve.exe`
        -   **Startup directory**: La ruta a la raíz de tu proyecto. Ejemplo: `C:\ruta\a\tu\proyecto\KreaDental-Cloud`
        -   **Arguments**: `--host=0.0.0.0 --port=8000 config.wsgi:application`
3.  **Iniciar el Servicio**: `nssm start KreaDentalCloud`

### Para Linux (con Gunicorn y systemd)

1.  **Crear un archivo de servicio de systemd**:
    ```bash
    sudo nano /etc/systemd/system/kreadental.service
    ```
2.  **Pega la siguiente configuración** en el archivo. **Reemplaza `<ruta_al_proyecto>` y `<tu_usuario>`** con tus valores.

    ```ini
    [Unit]
    Description=Gunicorn instance to serve KreaDental Cloud
    After=network.target

    [Service]
    User=<tu_usuario>
    Group=www-data
    WorkingDirectory=<ruta_al_proyecto>/KreaDental-Cloud
    Environment="PATH=<ruta_al_proyecto>/KreaDental-Cloud/virt/bin"
    ExecStart=<ruta_al_proyecto>/KreaDental-Cloud/virt/bin/gunicorn --workers 3 --bind unix:/run/gunicorn.sock config.wsgi:application

    [Install]
    WantedBy=multi-user.target
    ```

3.  **Iniciar y habilitar el servicio**:
    ```bash
    sudo systemctl start kreadental
    sudo systemctl enable kreadental
    ```

4.  **Configurar Nginx como proxy inverso** (Recomendado):
    -   Instala Nginx: `sudo apt install nginx`
    -   Crea un archivo de configuración para tu sitio: `sudo nano /etc/nginx/sites-available/kreadental`
    -   Pega esta configuración (reemplaza `tu_dominio.com`):
        ```nginx
        server {
            listen 80;
            server_name tu_dominio.com www.tu_dominio.com;

            location = /favicon.ico { access_log off; log_not_found off; }
            location /static/ {
                root <ruta_al_proyecto>/KreaDental-Cloud;
            }
            location /media/ {
                root <ruta_al_proyecto>/KreaDental-Cloud;
            }

            location / {
                include proxy_params;
                proxy_pass http://unix:/run/gunicorn.sock;
            }
        }
        ```
    -   Activa la configuración y reinicia Nginx:
        ```bash
        sudo ln -s /etc/nginx/sites-available/kreadental /etc/nginx/sites-enabled
        sudo systemctl restart nginx
        ```

## 5. Mantenimiento y Actualizaciones

Para actualizar la aplicación, conéctate al servidor y ejecuta:

```bash
git pull
source virt/bin/activate  # O virt\Scripts\activate en Windows
pip install -r requirements.txt
python manage.py migrate --settings=config.settings_production
python manage.py collectstatic --settings=config.settings_production --noinput

# Reiniciar el servicio
# Windows
nssm restart KreaDentalCloud
# Linux
sudo systemctl restart kreadental
sudo systemctl restart nginx
```
