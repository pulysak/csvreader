import logging
import datetime
from celery.task import periodic_task
from celery.schedules import crontab

from .reader import ProductReader

logger = logging.getLogger(__name__)


@periodic_task(run_every=crontab(minute=0, hour=12))
def update_products():
    logger.info('Start products updating - %s', datetime.datetime.now())
    reader = ProductReader()
    reader.update_products()
    logger.info('Finish products updating - %s', datetime.datetime.now())
