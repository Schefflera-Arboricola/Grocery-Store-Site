import os
from twilio.rest import Client
from flask import current_app as app
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from celery.schedules import crontab

cache = Cache()

account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
sender_phone = os.environ.get("TWILIO_SENDER_PHONE")

if not (account_sid and auth_token and sender_phone):
    raise Exception(
        "Twilio API credentials are not provided. Please set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_SENDER_PHONE environment variables."
    )

client = Client(account_sid, auth_token)

stripe_public_key = os.environ.get("STRIPE_PUBLIC_KEY")
stripe_secret_key = os.environ.get("STRIPE_SECRET_KEY")

if not (stripe_public_key and stripe_secret_key):
    raise Exception(
        "Stripe API keys are not provided. Please set STRIPE_PUBLIC_KEY and STRIPE_SECRET_KEY environment variables."
    )

app.config["STRIPE_PUBLIC_KEY"] = stripe_public_key
app.config["STRIPE_SECRET_KEY"] = stripe_secret_key

app.config["PERMANENT_SESSION_LIFETIME"] = 86400  # 1 day : session time(for OTPs etc.)
app.config["SECRET_KEY"] = "secret_key"

basedir = os.path.abspath(os.path.dirname(__file__))

app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "your-secret-key")
jwt = JWTManager(app)


class Config:
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class LocalDevelopmentConfig(Config):
    # for docker
    """SQLITE_DB_DIR = (
        "/app/db_directory"
        if os.getenv("ENV") == "development"
        else os.path.join(basedir, "../db_directory")
    )
    """
    # for virtual environment
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "gs.sqlite3")
    DEBUG = True
    CELERY_BROKER_URL = 'redis://localhost:6379/0'  
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'UTC'
    CELERYBEAT_SCHEDULE = {
        'send-daily-reminders': {
            'task': 'main.send_daily_reminders',
            'schedule': crontab(hour=6, minute=30),
        },
        'send-monthly-report': {
            'task': 'main.send_monthly_report',
            'schedule': crontab(day_of_month=1, hour=6, minute=30),
        },
    }
    CELERY_MAX_INTERVAL = 120
    CELERYD_LOG_LEVEL = 'debug'

    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0

    MAIL_DEBUG = True
    MAIL_SUPPRESS_SEND = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")

    if not (MAIL_USERNAME and MAIL_PASSWORD and MAIL_DEFAULT_SENDER):
        raise Exception(
            "Mail credentials are not provided. Please set MAIL_USERNAME, MAIL_PASSWORD, and MAIL_DEFAULT_SENDER environment variables."
        )

    SECURITY_PASSWORD_SALT = "thisissaltt"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionDevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "gs.sqlite3")
    DEBUG = False
