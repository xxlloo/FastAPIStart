import time

from celery_app import celery_app
from utils.logger import logger


@celery_app.task(
    name="tasks.generate_report",
    autoretry_for=(Exception,),
    max_retries=3,
)
def generate_report(u):
    time.sleep(1)
    logger.info(f"发送任务给 {u}")
