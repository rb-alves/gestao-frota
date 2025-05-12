from pathlib import Path
from decouple import config, Csv 
import os

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent


# Configurações principais do Django
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", cast=bool, default=False)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())


# Aplicativos instalados
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "colaboradores.apps.ColaboradoresConfig",
    "fornecedores.apps.FornecedoresConfig",
    "cadastros.apps.CadastrosConfig",
    "frota.apps.FrotaConfig",
    "seguranca.apps.SegurancaConfig"
    "home.apps.HomeConfig",
    "allauth",
    "allauth.account",
]

SITE_ID = 1

# Middlewares
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

# Configurações de URLs
ROOT_URLCONF = "setup.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "setup.wsgi.application"


# Banco de Dados
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config('DB_NAME'),
        "USER": config('DB_USER'),
        "PASSWORD": config('DB_PASSWORD'),
        "HOST": config('DB_HOST'),
        "PORT": config('DB_PORT', cast=int),
    }
}

# Autenticação
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]



# Validação de senha
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Configurações de Internacionalização
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True


# Arquivos estáticos e mídia
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "public")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Configuração de campo padrão
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Login e autenticação
LOGIN_URL = 'account_login'  # URL para onde os usuários não autenticados serão redirecionados

# Permite login com nome de usuário ou e-mail
ACCOUNT_AUTHENTICATION_METHOD = "username_email"

# URL de redirecionamento após login/logout
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'account_login'

# Configurações de Envio de emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

ACCOUNT_EMAIL_SUBJECT_PREFIX = "" # Retira o prexifo do assunto dos emails