import os
from project.settings import *

DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']

SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)

ADMINS = ((
    os.environ.get('ADMIN_EMAIL_NAME', ''), 
    os.environ.get('ADMIN_EMAIL_ADDRESS', '')
),)

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': os.environ.get('DB_NAME', ''),
       'USER': os.environ.get('DB_USER', '')
   }
}

STATIC_ROOT = os.path.join(BASE_DIR, os.environ.get('STATIC_ROOT', "static/"))
STATIC_URL = os.environ.get('STATIC_URL', STATIC_URL)

#MEDIA_ROOT = os.path.join('http://34.203.252.141/', 'media/')
#MEDIA_URL = '/media/'


MEDIA_ROOT = os.path.join(BASE_DIR, os.environ.get('MEDIA_ROOT', "media/"))
MEDIA_URL = os.environ.get('MEDIA_URL', "media/")