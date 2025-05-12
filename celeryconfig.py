from celery import Celery
from celery.schedules import crontab

app = Celery(
    "late_checkout_tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)


app.conf.beat_schedule = {
    "send-daily-checkout-sms": {
        "task": "schedule_today_checkouts",
        "schedule": crontab(minute='*/1'),  # crontab(hour=16, minute=40)  todos los días a las 6am UTC (3am ARG)
    }
}

app.conf.timezone = "UTC"
app.conf.enable_utc = True
