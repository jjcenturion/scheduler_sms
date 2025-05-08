from celery import Celery

app = Celery(
    "late_checkout_tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

app.conf.timezone = "UTC"
app.conf.enable_utc = True
