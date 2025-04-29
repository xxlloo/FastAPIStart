from datetime import timedelta

from celery import Celery, group, chain

from config.config import settings

RABBITMQ_URL = f"amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}/{settings.RABBITMQ_VHOST}"

celery_app = Celery(
    "worker",
    broker=RABBITMQ_URL,
    backend=f"{settings.REDIS_URL}/{settings.REDIS_DB}",
    include=[
        "tasks.send_email",
        "tasks.generate_report"
    ]
)

celery_app.conf.update(
    worker_prefetch_multiplier=1,
    task_acks_late=True,  # 确保任务至少执行一次
    worker_max_tasks_per_child=1000,  # 防止内存泄漏
    task_time_limit=360,
    task_soft_time_limit=300,
    broker_connection_retry=True,
    broker_connection_max_retries=100,
    worker_heartbeat_sec=10,
    timezone='Asia/Shanghai',
    broker_heartbeat=10,
    worker_concurrency=8,
    task_routes={
        "tasks.send_email": {
            'queue': 'send_email',
        },
        "tasks.generate_report": {
            'queue': 'generate_report',
        }
    },
    beat_schedule={
        'hourly-report': {
            'task': 'tasks.generate_report',
            'schedule': timedelta(seconds=10),
            'args': ('zhangsan',)
        }
    }
)
