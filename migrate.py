import os
import sys
import django
from django.core.management import execute_from_command_line

# Configurar o ambiente
base_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.join(base_dir, 'candangoEcommerce')
sys.path.extend([base_dir, project_dir])
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'candangoEcommerce.settings')

# Inicializar Django
django.setup()

# Executar migrações
execute_from_command_line(['manage.py', 'migrate'])
