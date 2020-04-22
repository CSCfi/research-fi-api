# This file is part of the research.fi API service
#
# Copyright 2019 Ministry of Education and Culture, Finland
#
# :author: CSC - IT Center for Science Ltd., Espoo Finland servicedesk@csc.fi
# :license: MIT

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_ENV_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get('DEBUG', False)))

# A list of strings representing the host/domain names that this Django site can serve
ALLOWED_HOSTS = ['.csc.fi', '.researchfi.svc.cluster.local', '.rahtiapp.fi', 'localhost', '127.0.0.1']

# HA Proxy
# If value is not available in environment variables, use dummy localhost value to enable unit test execution.
HA_PROXY_HOST = os.environ.get('DJANGO_ENV_HA_PROXY_HOST') if os.environ.get('DJANGO_ENV_HA_PROXY_HOST') is not None else "http://localhost:321321"

# HTTP auth username
HTTP_AUTH_USERNAME = os.environ.get('DJANGO_ENV_HTTP_AUTH_USERNAME', None)

# HTTP auth password
HTTP_AUTH_PASSWORD = os.environ.get('DJANGO_ENV_HTTP_AUTH_PASSWORD', None)

# Email server
if os.environ.get('DJANGO_ENV_EMAIL_HOST') is not None:
    EMAIL_HOST = os.environ.get('DJANGO_ENV_EMAIL_HOST')
else:
    EMAIL_HOST = 'localhost'

# Email sender address for server errors
if os.environ.get('HOSTNAME') is not None:
    SERVER_EMAIL = 'root@' + os.environ.get('HOSTNAME')
else:
    SERVER_EMAIL = 'root@localhost'

# Admin email receivers are parsed from environment variable, for example, 'admin1@myhost.com,admin2@myhost.com'
ADMINS = []
if os.environ.get('DJANGO_ENV_ADMINS') is not None:
    try:
        admin_emails = os.environ.get('DJANGO_ENV_ADMINS').split(',')
        for email in admin_emails:
            ADMINS.append(('researchfi administrator', email.strip()))
    except:
        print('Error: Could not parse ADMIN emails from environment variable DJANGO_ENV_ADMINS')
        pass

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'portalapi',
    'revproxy',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'webapps.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'webapps.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

# Settings for https://github.com/xmlrunner/unittest-xml-reporting
TEST_RUNNER = 'xmlrunner.extra.djangotestrunner.XMLTestRunner'
TEST_OUTPUT_DIR = 'portalapi/unittest_results'
TEST_OUTPUT_FILE_NAME = 'result.xml'

# Import local settings, if defined.
# Local settings can be used to overwrite values in development and testing environments.
try:
    from .local_settings import *
except ImportError:
    pass


# Set build info from text file, if defined.
BUILD_INFO = 'Build information not available'
try:
    build_info_file = os.path.join(BASE_DIR, 'build_info.txt')
    reader = open(build_info_file, 'r')
    BUILD_INFO = reader.readline()
    reader.close()
except:
    print(build_info_file + ' not found')
    pass
