import django_heroku
from secrets import *  # в .gitignore
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# для того, чтобы можно было тестировать локально:
SECRET_KEY = bool(os.getenv('SECRET_KEY', S_SECRET_KEY))
DEBUG = bool(os.getenv('DEBUG', True))
#

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'core',
    'polls',
    'tests',
    'nested_admin',
    ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

ROOT_URLCONF = 'sh-world-views.urls'

TEMPLATES = [{
            'BACKEND':'django.template.backends.django.DjangoTemplates',
            'DIRS':[],
            'APP_DIRS':True,
            'OPTIONS':{
                    'context_processors': [
                                        'django.template.context_processors.debug',
                                        'django.template.context_processors.request',
                                        'django.contrib.auth.context_processors.auth',
                                        'django.contrib.messages.context_processors.messages',
                                        ]
                    }
            }]

WSGI_APPLICATION = 'sh-world-views.wsgi.application'

DATABASES = {
            'default': {
                        'ENGINE':'django.db.backends.sqlite3',
                        'NAME':os.path.join(BASE_DIR, 'db.sqlite3')
                        }
            }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    ]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}

django_heroku.settings(locals())
