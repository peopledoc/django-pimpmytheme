"""
Django settings for example project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(BASE_DIR, ".."))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#^qtdm4ad9_44k+pf+2^ecrm(w9j@w(+s(^e$@s8l=zq%pqtwl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'pimpmytheme',
    'example',
    'subapp',
    'compressor',
    'django_nose'
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'example.urls'

WSGI_APPLICATION = 'example.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/


STATIC_ROOT = os.path.join(BASE_DIR, "example", "static")
STATIC_URL = '/static/'

SITE_ID = 1

COMPRESS_PRECOMPILERS = (('text/less', 'lessc {infile} {outfile}'),)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
                "pimpmytheme.context_processors.get_site",
            ],
            'builtins': [
                'django.templatetags.i18n',
                'django.templatetags.static',
                'django.templatetags.tz',
            ],
            'loaders': [
                'pimpmytheme.template_loader.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        }
    },
]

STATICFILES_FINDERS = (
    "pimpmytheme.static_finder.CustomFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder"
    )

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=pimpmytheme',
    '--verbosity=3',
    '--nocapture'
    ]

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
CUSTOM_THEME_LOOKUP_OBJECT = "example.models.PimpSite"
CUSTOM_THEME_LOOKUP_ATTR = "name"
PIMPMYTHEME_FOLDER = os.path.join(BASE_DIR, "pimp_theme")


LOGGING = {
    'version': 1,
    'formatters': {
        'oneline': {
            'format': '%(asctime)s %(levelname)-8s %(name)s  %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'oneline',
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    },
}
