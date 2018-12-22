import django_heroku

from config.settings.base import *


DEBUG = False


SECRET_KEY = os.environ['SECRET_KEY']


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# TODO EMAIL関係の設定を追加


SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'


django_heroku.settings(locals())
