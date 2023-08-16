import os
import environ
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()

# reading env vars in .env file
env_file_path = BASE_DIR / '.env'

if (secrets_data := os.environ.get('SECRETS')):
    with open(env_file_path, 'w') as f:
        f.write(secrets_data)

if env_file_path.is_file():
    env.read_env(env_file_path.open())

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', cast=str)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', cast=bool, default=False)

ADMINS = env('ADMIN_LIST', default=[
    ( 'Uhtred M.', 'am@uhtred.dev' )])

TESTING = env('TESTING', cast=bool,
    default= len(sys.argv) > 1 and sys.argv[1] == 'test')

SEND_EMAIL_ON_TESTING = env('SEND_EMAIL_ON_TESTING', cast=bool, default=False)

ALLOWED_HOSTS: list = env('ALLOWED_HOSTS', default=[
    '0.0.0.0',
    '127.0.0.1',
    'localhost'])

CORS_ORIGIN_WHITELIST = env('CORS_ORIGIN_WHITELIST', default=[])
CORS_ORIGIN_ALLOW_ALL = env('CORS_ORIGIN_ALLOW_ALL', default=False)

CSRF_COOKIE_SECURE = env('CSRF_COOKIE_SECURE', default=True)
CSRF_TRUSTED_ORIGINS = env('CSRF_TRUSTED_ORIGINS', default=[])

# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'uhtred.user',
    'uhtred.base',
    'uhtred.case',
    'uhtred.store',
    'uhtred.insight',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'martor'
]

MIDDLEWARE = [
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ADMIN_PATH = env('ADMIN_PATH', default='admin/')

ROOT_URLCONF = 'uhtred.urls'

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

WSGI_APPLICATION = 'uhtred.wsgi.application'

AUTH_USER_MODEL = 'user.User'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

if not env('DATABASE_URL', default=''):
    sqlite_url: str = 'sqlite:///' + (BASE_DIR / 'db.sqlite3').__str__()
    DATABASES = {
        'default': env.db('SQLITE_URL', default=sqlite_url)}
else:
    DATABASES = {'default': env.db()}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
PASSWORD_RESET_TIMEOUT = 3600

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ('en', 'English'),
    ('pt', 'Português')
]

TIME_ZONE = 'Africa/Luanda'

LOCALE_PATHS = (
    BASE_DIR / '../locale',)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

MEDIA_URL = '/upload/'
MEDIA_ROOT = BASE_DIR / 'uploads'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    "default": {
        "BACKEND": env('DEFAULT_FILE_STORAGE',
                        default='storages.backends.gcloud.GoogleCloudStorage')
    },
    "staticfiles": {
        "BACKEND": env('STATICFILES_STORAGE',
                        default='storages.backends.gcloud.GoogleCloudStorage')
    }
}

GS_BUCKET_NAME = env('GS_BUCKET_NAME', default='uhtred')
GS_DEFAULT_ACL = env('GS_DEFAULT_ACL', default=None, cast=str)
GS_QUERYSTRING_AUTH = env('GS_QUERYSTRING_AUTH', default=False)
GS_OBJECT_PARAMETERS = {
    'cache_control': 'max-age=31536000'}

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework_simplejwt.authentication.JWTAuthentication'
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )}
