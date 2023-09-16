# fastapi-stripe-service
trying to fix icn's backend

- uses stripe under the hood with a testing key (rafi's account)
- Async queue uses Celery with RabbitMQ as broker and backend
- todo: email sending with mailgun and WKHTMLTOPDF

# running
- docker-compose up -d (to run it in the background)
- check docker desktop for logs
