from celery import Celery

celery = Celery(
    "payment_tasks",
    broker="amqp://admin:mypass@rabbit:5672",
    backend="amqp://admin:mypass@rabbit:5672",
)
