import os
from pathlib import Path
from datetime import datetime, timezone, timedelta


class Config:

    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent
    LOCALES_PATH = f'{BASE_DIR}/locales/'
    SUPPORTED_LANGUAGES = ['en', 'uk']

    @staticmethod
    def CURRENT_TIME():
        return datetime.now(timezone.utc)

    # SET PROJECT NAME
    PROJECT_NAME = os.environ.get('PROJECT_NAME', 'Boilerplate')

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = os.environ.get('SECRET_KEY', 'SET_SECRET_KEY')

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = bool(int(os.environ.get('DEBUG'), 0))

    # SWAGGER URL
    DOCKS_URL = os.environ.get('DOCKS_URL', None)
    REDOC_URL = os.environ.get('REDOC_URL', None)
    OPEN_API_URL = os.environ.get('OPEN_API_URL', '')

    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'warning')
    LOGGING_CONFIG_PATH = f'{BASE_DIR}/core/services/logging_config.json'

    # Cookies
    DOMAIN = os.environ.get('DOMAIN', 'localhost')
    COOKIES_SECURE = bool(int(os.environ.get('COOKIES_SECURE', 0)))
    SAME_SITE = os.environ.get('SAME_SITE', None)

    # HOST
    ALLOWED_HOSTS = []
    ALLOWED_HOSTS.extend(
        filter(
            None,
            os.environ.get('ALLOWED_HOSTS', '*').split(','),
        )
    )

    # CORS
    CORS_ALLOWED_ORIGINS = []
    CORS_ALLOWED_ORIGINS.extend(
        filter(
            None,
            os.environ.get('CORS_ALLOWED_ORIGINS', '*').split(','),
        )
    )
    CORS_ALLOW_METHODS = []
    CORS_ALLOW_METHODS.extend(
        filter(
            None,
            os.environ.get('CORS_ALLOW_METHODS', '*').split(','),
        )
    )

    # MongoDB
    MD_DB = os.environ.get('MD_DB')
    MD_USER = os.environ.get('MD_USER')
    MD_PASSWORD = os.environ.get('MD_PASSWORD')
    MD_HOST = os.environ.get('MD_HOST')
    MD_PORT = os.environ.get('MD_PORT')
    MONGO_DB_URL = 'mongodb://{user}:{password}@{host}:{port}/'.format(
        user=MD_USER,
        password=MD_PASSWORD,
        host=MD_HOST,
        port=MD_PORT
    )

    # Redis
    REDIS_URL = os.environ.get('REDIS_URL')

    # JWT
    ACCESS_TOKEN_EXPIRE = timedelta(minutes=int(os.environ.get('ACCESS_TOKEN_EXPIRE', 5)))
    REFRESH_TOKEN_EXPIRE = timedelta(days=int(os.environ.get('REFRESH_TOKEN', 7)))
    COOKIES_EXPIRE = timedelta(days=int(os.environ.get('COOKIES_EXPIRE', 7)))
    ALGORITHM = "HS256"  # HS256 OR RS256
    JWT_SECRET_KEY = SECRET_KEY

    # Sentry
    USE_SENTRY = bool(int(os.environ.get('USE_SENTRY')))
    SENTRY_DSN = os.environ.get('SENTRY_DSN')
    SENTRY_TRACE_SAMPLE_RATE = float(os.environ.get('SENTRY_TRACE_SAMPLE_RATE', 1.0))
    SENTRY_PROFILE_SAMPLE_RATE = float(os.environ.get('SENTRY_PROFILE_SAMPLE_RATE', 1.0))

    # Celery
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')
    CELERY_IMPORTS = [
        'apps.test.tasks'
    ]

    CELERY_TASK_TRACK_STARTED = True
    CELERY_TASK_TIME_LIMIT = 60 * 10  # 10 хвилин
    CELERY_TIMEZONE = 'UTC'

    CELERY_BEAT_SCHEDULE = {
        'simple-task': {
            'task': 'apps.test.tasks.simple_task',
            'schedule': timedelta(seconds=30),
        }
    }
