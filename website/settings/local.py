from .base import *

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')g%oavl$ag(vx(n0r*%&mihh%)#c8(@2v-fp*x119o_@-ik)bd'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'webdb',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306'}
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PRO_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],

            'string_if_invalid': 'INVALID EXPERSSION: %s',
        },
    },
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
# STATICFILES_DIRS = (
#     # {% load staticfiles %}
#     # /vagrant/practice/website/static/
#     os.path.join(PRO_DIR, "static"),
# )

STATIC_ROOT = os.path.join(PRO_DIR, "static")

# /vagrant/practice/website/media
MEDIA_ROOT = os.path.join(PRO_DIR, "media")
MEDIA_URL = '/media/'

# os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = 'localhost:8081/superlist/'

