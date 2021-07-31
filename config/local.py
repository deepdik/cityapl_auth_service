# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u*mvv8s^0&bu8#fact-k#g7rh-rz5!izrtbrlnii-o!+n$jjp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

API_ROOT = DEBUG # enable root api view

SITE_URL = ''
APP_LOGO = ''

############################# Database #############################
# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
# mysql --host=cityapl-database-1.cyvpsljpkc8d.ap-south-1.rds.amazonaws.com --port=3306 --user=admin --password=cityapl_rds123


# MYSQL RDS

# DATABASES = {
# 	'default': {
# 		'ENGINE': 'django.db.backends.mysql',
# 		'NAME': 'cityapl',
# 		'USER': 'admin',
# 		'PASSWORD': 'cityapl_rds123',
# 		'HOST': 'cityapl-database-1.cyvpsljpkc8d.ap-south-1.rds.amazonaws.com',
# 		'PORT': '3306',
# 	}
# }

##local Postgres database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'cityapl',
        'USER': 'myprojectuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}

#  Server Postgresql

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'cityapl',
#         'USER': 'myprojectuser',
#         'PASSWORD': 'password',
#         'HOST': '13.233.128.251',
#         'PORT': '5432',
#     }
# }


########################## DRF Settings #############################
REST_FRAMEWORK = {
	'DEFAULT_PERMISSION_CLASSES': (
		'rest_framework.permissions.AllowAny',
	),
	'DEFAULT_RENDERER_CLASSES': (
		'rest_framework.renderers.JSONRenderer',
		'rest_framework.renderers.BrowsableAPIRenderer',
		# 'rest_framework.renderers.AdminRenderer',
	),
	'DEFAULT_AUTHENTICATION_CLASSES': (
		'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
		'rest_framework.authentication.SessionAuthentication',
		'rest_framework.authentication.BasicAuthentication',
	),
	'DEFAULT_FILTER_BACKENDS': (
		'django_filters.rest_framework.DjangoFilterBackend',
		'rest_framework.filters.SearchFilter',
		'rest_framework.filters.OrderingFilter',
	),
	'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
	'DEFAULT_VERSION': 'v1',
	'ALLOWED_VERSIONS': ('v1', 'v2'),
	'DEFAULT_PAGINATION_CLASS': 'cityapl.pagination.StandardResultsPageNumberPagination',
	# 'EXCEPTION_HANDLER': 'cityapl.exceptions.custom_exception_handler',
}

with open(BASE_DIR + '/config/keys/jwt-key.pub','r') as f:
    PUBLIC_KEY = f.read()

with open(BASE_DIR + '/config/keys/jwt-key','r') as f:
    PRIVATE_KEY = f.read()

JWT_AUTH = {
    'JWT_ENCODE_HANDLER':
    'rest_framework_jwt.utils.jwt_encode_handler',

    'JWT_DECODE_HANDLER':
    'rest_framework_jwt.utils.jwt_decode_handler',

    'JWT_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_payload_handler',

    'JWT_PAYLOAD_GET_USER_ID_HANDLER':
    'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',

    'JWT_RESPONSE_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_response_payload_handler',

    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_GET_USER_SECRET_KEY': None,
    'JWT_PUBLIC_KEY': PUBLIC_KEY,
    'JWT_PRIVATE_KEY': PRIVATE_KEY,
    'JWT_ALGORITHM': 'RS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=30000),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,

    'JWT_ALLOW_REFRESH': False,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),

    'JWT_AUTH_HEADER_PREFIX': 'token',
    'JWT_AUTH_COOKIE': None,

}


############################# Static ###############################
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
	os.path.join(BASE_DIR, "cityapl/static"),
	#'/var/project/static/',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

############################# Logging ###############################
PY_LOGGING = DEBUG  # True/False
ADMINS = (('Admin', ''),)

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'filters': {
		'require_debug_true': {
			'()': 'django.utils.log.RequireDebugTrue'
		},
		'require_debug_false': {
			'()': 'django.utils.log.RequireDebugFalse',
		}
	},
	'handlers': {
		'mail_admins': {
			'level': 'ERROR',
			'filters': [
				'require_debug_false',
				# 'require_debug_true'
			],
			'class': 'django.utils.log.AdminEmailHandler'
		}
	},
	'loggers': {
		'django.request': {
			'handlers': ['mail_admins'],
			'level': 'ERROR',
			'propagate': True
		}
	}
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

SOCIAL_AUTH_GOOGLE_OAUTH_KEY = '961513181020-ll6lp4qe015ufmgi6udqk4q6qmul53fj.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH_SECRET = 'CoFFeTOJNoDgQxMJAJ2BcdGc'
