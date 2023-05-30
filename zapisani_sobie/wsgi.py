import os

from django.core.wsgi import get_wsgi_application

from django.core.wsgi import get_wsgi_application

import sys
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
        sys.path.append(path)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zapisani_sobie.settings')

application = get_wsgi_application()