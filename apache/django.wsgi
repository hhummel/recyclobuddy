"""
WSGI config for mysite project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import sys

#Takes advantage of setting up parallel file structure for mysite/apache/wsgi.py and mysite/mysite/settings.py 
root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, root)

#Seems to need the absolute path as well
sys.path.append('/usr/local/django/recyclocity')
sys.path.append('/usr/local/django/recyclocity/static')

os.environ['PYTHON_EGG_CACHE'] = '/usr/local/django/recyclocity/.python.egg'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()

# Apply WSGI middleware here.
#from helloworld.wsgi import HelloWorldApplication
#application = HelloWorldApplication(application)
