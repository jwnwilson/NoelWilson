# Django settings for noelwilson project.

import socket, os, sys, platform

DEBUG = False
DEV_SERVER = True
TEMPLATE_DEBUG = DEBUG
LOG_LEVEL = "INFO"

# We can't use SMTP for app engine and will use the appengine backend instead
USE_SMTP = False
EMAIL_SUBJECT_PREFIX = '[Canvas Clothes] '
if USE_SMTP:
    with open('main/pass', 'rb') as fp:
        password = fp.read().decode('base64')

    if password is None:
        raise RuntimeError("No password for SMTP set.")

    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = 'jwnwilson88@gmail.com'
    EMAIL_HOST_PASSWORD = password
else:
    if DEBUG:
      EMAIL_BACKEND = 'appengine_emailbackend.EmailBackend'
    else:
      EMAIL_BACKEND = 'appengine_emailbackend.EmailBackend'
      #EMAIL_BACKEND = 'appengine_emailbackend.async.EmailBackend'

SERVER_EMAIL = 'jwnwilsonuk@appspot.gserviceaccount.com'

ADMINS = (
  ('Noel Wilson', 'jwnwilson@hotmail.co.uk'),
)
MANAGERS = ADMINS

ALLOWED_HOSTS = ["127.0.0.1","localhost","jwnwilsonuk.appspot.com"]

# Database settings
if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine'):
    # Running on production App Engine, so use a Google Cloud SQL database.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '/cloudsql/jwnwilsonuk:sqldb',
            'NAME': 'jwnwilson',
            'USER': 'jwnwilson',
        }
    }
elif DEV_SERVER:
    # Running in development, but want to access the Google Cloud SQL instance
    # in production.
    DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '173.194.105.35',
        'NAME': 'jwnwilson',
        'USER': 'anu',
        'PASSWORD': 'sqlgoogle1',
        }
    }
else:
    # Running in development, so use a local MySQL database.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'jwnwilson',
            'USER': 'root',
            'PASSWORD': '',
        }
    }


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
PROJECT_ROOT = os.path.normpath( os.path.dirname( __file__) )
MEDIA_ROOT = os.path.join( PROJECT_ROOT, 'media' )

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(os.path.dirname(__file__),'static').replace('\\','/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
	#"/home/DjangoProjects/noelwilson/noelwilson/static/",
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '6tr=1vmg$5cn0hkor(11b+2!gje^1(qyx2ky157+_x^uxx$89e'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'noelwilson.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'noelwilson.wsgi.application'

TEMPLATE_DIRS = (
	( PROJECT_ROOT + '/apps/main/templates').replace('\\','/'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'noelwilson.apps.main',
    'noelwilson.apps.data',
    'noelwilson.apps.flickr',
    'noelwilson.apps.blog',
    'noelwilson.apps.accounts',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

#CSRF_FAILURE_VIEW = 'blogv2.custom.csrf.views.csrf_rejected'

EMAIL_HOST 		= "jwnwilson@hotmail.co.uk"
EMAIL_HOST_USER		= "noelwilson"
EMAIL_HOST_PASSWORD	= "johnathan"
EMAIL_PORT			= 25
EMAIL_USE_TLS		= True

LOGIN_REDIRECT_URL = "/profile/"
LOGIN_URL = "/login/"

AUTHENTICATION_BACKENDS = ('noelwilson.apps.accounts.auth.backends.AccountsBackend',)
AUTH_PROFILE_MODULE = "accounts.UserProfile"

DEFAULT_FILE_STORAGE = "/static/data/"

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}