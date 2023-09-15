from celery import Celery

celery = Celery(
    "tasks", broker="redis://localhost:6379/0", backend="db+sqlite:///mydatabase.db"
)
