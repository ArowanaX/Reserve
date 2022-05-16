from celery import Celery
from celery import shared_task
from .utils import send_email, send_mail

app = Celery('tasks', broker='redis://guest@localhost//')

@shared_task
def send_mail():
    send_mail()
    print('Send Email')