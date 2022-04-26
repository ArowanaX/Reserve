from celery import shared_task
from .utils import Send_sms

#----------------celery broker task---------------
@shared_task()
def my_validate(to_phone,uid):
    Send_sms(to_phone,uid)