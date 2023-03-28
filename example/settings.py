"""Django settings for example project."""

# Django development

SECRET_KEY = "django-insecure-secret"

DEBUG = True

# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django_user_trace",  # <- ADD THIS
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_user_trace.middleware.django_user_trace_middleware",  # <- ADD THIS
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "example.urls"

WSGI_APPLICATION = "example.wsgi.application"

ASGI_APPLICATION = "example.asgi.application"

# Database definition

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}

# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "user_attrs": {"()": "django_user_trace.log.DjangoUserAttrs"},  # <- ADD THIS
    },
    "formatters": {
        "verbose": {
            "format": "{asctime} {name} {process:d} {thread:d} {username} {levelname} - {message}",  # <- MODIFY THIS
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "filters": ["user_attrs"],  # <- MODIFY THIS
        },
    },
    "loggers": {
        "django": {
            "level": "INFO",
            "handlers": ["console"],
        },
        "example": {
            "level": "DEBUG",
            "handlers": ["console"],
        },
        "django_user_trace": {
            "level": "DEBUG",
            "handlers": ["console"],
        },
    },
}
