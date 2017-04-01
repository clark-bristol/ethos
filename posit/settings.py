"""
Django settings for posit project.

Generated by 'django-admin startproject' using Django 1.9.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""
import os
from . import settings_secret as ss

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECRET KEY
SECRET_KEY = ss.secret_key
SECRET_NEO4J_DB_USER = ss.secret_neo4j_db_user
SECRET_NEO4J_DB_PASSWORD = ss.secret_neo4j_db_password
SECRET_NEO4J_DB_HOSTPORT = ss.secret_neo4j_db_hostport

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'positproject@gmail.com'
EMAIL_HOST_PASSWORD = ss.secret_email_password
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Application definition
# IMPORTANT MAINLY FOR MODELS
INSTALLED_APPS = [
    # third party apps that must be listed first
    'grappelli',  # (https://django-grappelli.readthedocs.io/en/latest)
    # first party apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',  # required for registration app
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third party apps
    'crispy_forms',
    'debug_toolbar',
    'registration',
    'rest_framework',  # http://www.django-rest-framework.org
    'taggit',  # http://django-taggit.readthedocs.org/en/latest/getting_started.html
    # my apps
    'claims',
    'userProfiles',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'posit.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'posit.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # },
    'default': {
        'ENGINE': ss.secret_postgres_db_engine,
        'NAME': ss.secret_postgres_db_name,
        'USER': ss.secret_postgres_db_user,
        'PASSWORD': ss.secret_postgres_db_password,
        'HOST': ss.secret_postgres_db_host,
        'PORT': ss.secret_postgres_db_port,
    }
}


# For Heroku
# import dj_database_url
# db_from_env = dj_database_url.config()
# DATABASES['default'].update(db_from_env)

# NEO4J_DATABASES = {
#     'default' : {
#         'HOST':'localhost',
#         'PORT':7474,
#         'ENDPOINT':'/db/data'
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
# This is the directory where static files are copied to (when you run collectstatic)
#   In deployment this will be a separate server
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_in_env", "static_root")

# These are the directories from which static files are copied into static root
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static_in_pro", "our_static"),
    # '/var/www/static/',
]

# things that are uploaded (e.g. by users)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_in_env", "media_root")


# SETTINGS FOR INSTALLED APPS ##############################################################################################

# DJANGO REGISTRATION REDUX SETTINGS
ACCOUNT_ACTIVATION_DAYS = 7
# REGISTRATION_DEFAULT_FROM_EMAIL =
# REGISTRATION_EMAIL_HTML = True
REGISTRATION_AUTO_LOGIN = True
SITE_ID = 1
LOGIN_REDIRECT_URL = '/'

# cripsy FORMS TAGs SETTINGS
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# REST API framework
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'  # This was the default recommendation
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'PAGE_SIZE': 20
}
