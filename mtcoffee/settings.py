

from pathlib import Path
# import environ

from decouple  import config
import os

# 
BASE_DIR = Path(__file__).resolve().parent.parent


# DEBUG = config('DEBUG',cast=bool)  # سيقرأ DEBUG من .env
SECRET_KEY = config('SECRET_KEY')  # سيقرأ SECRET_KEY
DEBUG = True
# pip install python-decouple
# source env/bin/activate
# from decouple import config
from django.utils.translation import gettext_lazy as _


# ALLOWED_HOSTS = ['64.23.197.169',]
ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
  
    'dbbackup',
    'pages.apps.PagesConfig',
    
    # 'hide_admin.apps.HideAdminConfig',
    'accounts.apps.AccountsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'import_export',
    'orders',
    # 'pages',
    'product',
    # 'social_django',
  
    'rosetta',
    'crispy_forms',
    'crispy_bootstrap5',
    # 'anymail',
    # 'rest_framework',
    # 'admin_honeypot'
]

# RATELIMIT_IP_META_KEY = 'HTTP_X_FORWARDED_FOR'


CRISPY_TEMPLATE_PACK = 'bootstrap4'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    
]

ROOT_URLCONF = 'mtcoffee.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.backends',
                'product.base.dase',
                'product.base.cint',

            ],
        },
    },
]

WSGI_APPLICATION = 'mtcoffee.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'bbbbbbbbbbffffffcfxf', #'ssggjj', #bbbbbbbbbbbbbbbbggg
#         'USER': 'root',
#         'PASSWORD': '',
#         'HOST': 'localhost',
#         'PORT':3306,
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': BASE_DIR / 'backup' }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'djangomypro',
#         'USER': 'root',
#         'PASSWORD': '123456',
#         'HOST': 'localhost',
#         'PORT': ''
#     }
# }
# DATABASES = {
#     'default': {
#         'ENGINE': config('ENGINE'),
#         'NAME': config('NAME'),
#         'USER': 'dbuser' ,
#         'PASSWORD': config('PASSWORD'),
#         'HOST': config('HOST'),
#         'PORT': config('PORT'),
#     }
# }




# DATABASES = {
#     'default': {
#         # 'ENGINE': 'django.db.backends.postgressql_psycopg2',
#         'ENGINE': 'django.db.backends.postgresql',

#         'NAME': 'hallo_worled',
#         'USER': 'postgres',
#         'PASSWORD': '1234',
#         'HOST': 'localhost',
#         'PORT':'5433',
#     }
# }

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Africa/Cairo'

USE_I18N = True

USE_TZ = False


# LANGUAGE_CODE = 'en'

USE_L10N = True

LANGUAGES  = (
    ('en', _('English')),
    ('ar', _('Arabic')),
)
LOCALE_PATHS = (
    os.path.join("locale"),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
import os
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

STATICFILES_DIRS =[
    os.path.join(BASE_DIR,'mtcoffee/static')
]

#media
MEDIA_ROOT=os.path.join(BASE_DIR,'media')
MEDIA_URL ='/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.ERROR: "danger",
    
}


LOGIN_URL ='login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'login'

# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "smtp.gmail.com"

# EMAIL_PORT = 587
# EMAIL_PORT = 2525

# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = "abdozxcvbnmapi@gmail.com"
# EMAIL_HOST_PASSWORD = 'pebi ztbv syxu bcue'
# ///////////////////////////////////////////





GOOGLE_RACAPTCHA_SECRET_KEY = config('GOOGLE_RACAPTCHA_SECRET_KEY')

CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND')
CELERY_BROKER_URL  = config('CELERY_BROKER_URL')



# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': 'redis://127.0.0.1:6379/1',
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#         }
#     }
# }









EMAIL_BACKEND = "anymail.backends.sendinblue.EmailBackend"  

ANYMAIL = {
    
    "SENDINBLUE_API_KEY": config('SENDINBLUE_API_KEY'),

}
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL') 


# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE=True

# server {
#     listen 80;
#     server_name 64.23.197.169;
#     client_max_body_size 1000M;

#     location = /favicon.ico { access_log off; log_not_found off; }
#     location /static/ {
#         root /home/boards_user/blog;
#     }

#     location / {
#         include proxy_params;
#         proxy_pass http://unix:/run/gunicorn.sock;
#     }
# }




#     server {
#     listen 80;
#     server_name 64.23.197.169;

#     # المجلد الجذر للملفات الثابتة
#     root /home/boards_user/blog;
    

#     location = /favicon.ico { access_log off; log_not_found off; }
#     location /static/ {
#         root /home/boards_user/blog;
#     }

#     location / {
#         include proxy_params;
#         proxy_pass http://unix:/run/gunicorn.sock;
#     }
#     # تحسين الأداء باستخدام gzip
#     gzip on;
#     gzip_types text/plain application/xml text/css text/javascript application/javascript application/json;
#     gzip_min_length 256;

#     # التعامل مع الملفات الثابتة مباشرة من Nginx (تسريع كبير)
#     location /static/ {
#         alias /home/boards_user/blog/static/;
#         expires 30d;
#         access_log off;
#     }

#     location /media/ {
#         alias /home/boards_user/blog/media/;
#         expires 30d;
#         access_log off;
#     }

#     # توجيه باقي الطلبات إلى Gunicorn
#     location / {
#         proxy_pass http://127.0.0.1:8000;
#         proxy_set_header Host $host;
#         proxy_set_header X-Real-IP $remote_addr;
#         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#         proxy_set_header X-Forwarded-Proto $scheme;

#         # تحسين الأداء
#         proxy_read_timeout 60;
#         proxy_connect_timeout 60;
#         proxy_redirect off;
#     }

#     # حماية من بعض الهجمات
#     client_max_body_size 100M;
#     keepalive_timeout 5;
# }