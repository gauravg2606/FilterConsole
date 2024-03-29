"""
Django settings for StickerTagger project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'iureb4oqi@om9e+%t_+mqv!b=^^b-u(ho)2qw724ors4@&q3*&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []



# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'taggie',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
   'django.contrib.auth.context_processors.auth',
   'django.core.context_processors.debug',
   'django.core.context_processors.i18n',
   'django.core.context_processors.media',
   'django.core.context_processors.static',
   'django.core.context_processors.tz',
   'django.contrib.messages.context_processors.messages',
)

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = "/tag/"
LOGIN_ERROR_URL = "/"

LOGIN_REDIRECT_URL = '/'
ROOT_URLCONF = 'StickerTagger.urls'

WSGI_APPLICATION = 'StickerTagger.wsgi.application'

TEMPLATE_DIRS = [os.path.join(BASE_DIR,'templates')]

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

#DATABASES = {
#   'default': {
#       'ENGINE': 'django.db.backends.sqlite3',
#       'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#   }
#}

DATABASES = {
     'default': {
	'ENGINE': 'django.db.backends.mysql',
        'NAME': 'taggie',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1', # Or an IP Address that your DB is hosted on
        'PORT': '3306',
      }
}

#
#DATABASES = {
#     'default': {
#	'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'taggie',
#        'USER': 'hike',
#        'PASSWORD': 'h1kerS3my59l',
#        'HOST': '10.0.1.141', # Or an IP Address that your DB is hosted on
#        'PORT': '3306',
#      }
#}
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    '/var/www/static/',
)

GOOGLE_OAUTH2_CLIENT_ID = "974130700916-acfouldofrdrv0ig7rique16f1c1nn9i.apps.googleusercontent.com"
GOOGLE_OAUTH2_CLIENT_SECRET = "8nzzGNB7KBnPDyImh5Dh1HMa"
GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {'access_type': 'offline'}
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = GOOGLE_OAUTH2_CLIENT_ID
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = GOOGLE_OAUTH2_CLIENT_SECRET
