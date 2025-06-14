# base.py의 모든 것을 가져오는 것
from .base import *

def read_secret(secret_name):
    file = open('/run/secrets/' + secret_name)
    secret = file.read()
    secret = secret.rstrip().lstrip()
    file.close()
    return secret

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Reading .env file
environ.Env.read_env(
    env_file = os.path.join(BASE_DIR,'.env')
)
# Quick-start development settingss - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = read_secret('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['citypilgrims.com', 'www.citypilgrims.com', '64.176.228.128']

CSRF_TRUSTED_ORIGINS = [
    'https://citypilgrims.com',
    'https://www.citypilgrims.com',
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# 쿠키 보안 설정 강화
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django',
        'USER': 'django',
        'PASSWORD': read_secret('MYSQL_PASSWORD'),
        'HOST': 'mariadb',
        'PORT': '3306',
    }
}
