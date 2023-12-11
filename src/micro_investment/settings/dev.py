from micro_investment.settings.base import *
from datetime import timedelta

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-jb%wfsz-d!9378-7k&lyo*n-r@b)m28*z(xz7kx)(r4b^k3nr('

# Application definition
INSTALLED_APPS += ['debug_toolbar',]

INTERNAL_IPS = ('127.0.0.1', '0.0.0.0', 'localhost',)

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware",]

ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(',')

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

SIMPLE_JWT = {
    # When set to True, if a refresh token is submitted to the TokenRefreshView, a new refresh token will be returned
    # along with the new access token.
    'ROTATE_REFRESH_TOKENS': True,
    # refresh tokens submitted to the TokenRefreshView to be added to the blacklist
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',  # TWO types either HMAC  or RSA for HMAC 'HS256', 'HS384', 'HS512: SIGNING_KEY setting
    # will be used as both the signing key and the verifying key.  asymmetric RSA RS256', 'RS384',
    # 'RS512' SIGNING_KEY setting must be set to a string that contains an RSA private key. Likewise, the VERIFYING_KEY
    'SIGNING_KEY': SECRET_KEY,  # content of generated tokens.
    # The verifying key which is used to verify the content of generated tokens
    'VERIFYING_KEY': None,
    # The audience claim to be included in generated tokens and/or validated in decoded tokens
    'AUDIENCE': None,
    'ISSUER': None,  # issuer claim to be included in generated tokens

    # Authorization: Bearer <token> ('Bearer', 'JWT')
    'AUTH_HEADER_TYPES': ('Bearer',),
    # The database field from the user model that will be included in generated tokens to identify users.
    'USER_ID_FIELD': 'id',
    # value of 'user_id' would mean generated tokens include a “user_id” claim that contains the user’s identifier.
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    # The claim ad that is used to store a token’s type
    'TOKEN_TYPE_CLAIM': 'token_type',

    # The claim ad that is used to store a token’s unique identifier.
    'JTI_CLAIM': 'jti',
    # which specifies how long access tokens are valid
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    # how long refresh tokens are valid.
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
}

CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Baku'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda _request: DEBUG
}