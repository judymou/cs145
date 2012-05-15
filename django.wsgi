import os, sys
sys.path.append('/home/ubuntu')
sys.path.append('/home/ubuntu/project_name')
sys.path.append('/home/ubuntu/project_name/apps')
os.environ['DJANGO_SETTINGS_MODULE'] = 'project_name.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()