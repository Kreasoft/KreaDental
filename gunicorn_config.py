# Gunicorn configuration file for KreaDental-Cloud
import multiprocessing
import os

# Server socket
bind = "127.0.0.1:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100

# Restart workers after this many requests, to help prevent memory leaks
preload_app = True

# Logging
accesslog = os.path.join(os.path.dirname(__file__), "logs", "gunicorn_access.log")
errorlog = os.path.join(os.path.dirname(__file__), "logs", "gunicorn_error.log")
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "kreadental_gunicorn"

# Server mechanics
daemon = False
pidfile = os.path.join(os.path.dirname(__file__), "gunicorn.pid")
user = None
group = None
tmp_upload_dir = None

# SSL (descomentar cuando tengas certificados SSL)
# keyfile = "/etc/ssl/private/kreadental.key"
# certfile = "/etc/ssl/certs/kreadental.crt"

# Environment variables
raw_env = [
    'DJANGO_SETTINGS_MODULE=config.settings_production',
]

# Server hooks
def on_starting(server):
    """Called just before the master process is initialized."""
    server.log.info("Starting KreaDental-Cloud server")

def on_reload(server):
    """Called to recycle workers during a reload via SIGHUP."""
    server.log.info("Reloading KreaDental-Cloud server")

def when_ready(server):
    """Called just after the server is started."""
    server.log.info("KreaDental-Cloud server is ready")

def worker_int(worker):
    """Called just after a worker exited on SIGINT or SIGQUIT."""
    worker.log.info("Worker received SIGINT or SIGQUIT")

def pre_fork(server, worker):
    """Called just before a worker is forked."""
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_fork(server, worker):
    """Called just after a worker has been forked."""
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def pre_exec(server):
    """Called just before a new master process is forked."""
    server.log.info("Forked child, re-executing")

def when_ready(server):
    """Called just after the server is started."""
    server.log.info("Server is ready. Spawning workers")

def worker_abort(worker):
    """Called when a worker receives the SIGABRT signal."""
    worker.log.info("Worker received SIGABRT")

def on_exit(server):
    """Called just before exiting."""
    server.log.info("Shutting down KreaDental-Cloud server")
