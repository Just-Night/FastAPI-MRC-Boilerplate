from celery import Celery
from core.config import Config


app = Celery('app')
app.config_from_object('core.config:Config', namespace='CELERY')

app.autodiscover_tasks(lambda: Config.CELERY_IMPORTS, force=True)
