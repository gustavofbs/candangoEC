import os
import sys

# Adiciona os diretórios necessários ao PYTHONPATH
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
project_dir = os.path.join(base_dir, 'candangoEcommerce')

# Adiciona os diretórios ao PYTHONPATH
paths = [
    base_dir,
    project_dir,
    os.path.join(project_dir, 'candangoEcommerce')
]
for path in paths:
    if path not in sys.path:
        sys.path.insert(0, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'candangoEcommerce.settings')

# Debug dos caminhos
print("BASE_DIR:", base_dir)
print("PROJECT_DIR:", project_dir)
print("sys.path:", sys.path)

from django.core.wsgi import get_wsgi_application
from django.core.handlers.wsgi import WSGIRequest
from django.middleware.csrf import get_token

# Inicializa a aplicação Django
application = get_wsgi_application()

def app(event, context):
    # Garante que o token CSRF está disponível
    if event.get('httpMethod') == 'POST':
        # Cria uma requisição WSGI
        environ = {
            'REQUEST_METHOD': event.get('httpMethod', 'GET'),
            'CONTENT_TYPE': event.get('headers', {}).get('content-type', ''),
            'HTTP_COOKIE': event.get('headers', {}).get('cookie', ''),
        }
        request = WSGIRequest(environ)
        # Gera o token CSRF se necessário
        get_token(request)
    
    return application(event, context)
