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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    # /vagrant/practice/website/static/
    os.path.join(PRO_DIR, "static"),
)
# /vagrant/practice/website/media
MEDIA_ROOT = os.path.join(PRO_DIR, "media")
MEDIA_URL = '/media/'
