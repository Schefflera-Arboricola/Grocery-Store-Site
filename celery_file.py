from celery import Celery 

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'],
    )
    celery.conf.update(app.config)
    celery.conf.beat_schedule = app.config['CELERYBEAT_SCHEDULE']

    return celery