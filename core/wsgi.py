import os
import sys

# caminho absoluto do projeto (com hífen)
project_path = '/home/matheusmiguelsa/tintim-desafio'
if project_path not in sys.path:
    sys.path.insert(0, project_path)

# pasta onde está o manage.py e core/settings.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
