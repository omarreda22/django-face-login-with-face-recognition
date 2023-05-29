from __future__ import absolute_import, unicode_literals
from celery import shared_task



from django.core.mail import EmailMessage


@shared_task
def send_email(title, email):
    subject = "Hello Our New User, Welcome."
    send_email = EmailMessage(title, subject, to=[email])
    send_email.send()    

############################################################################
## schedules tasks
from celery import Celery

app = Celery()

@app.task(name="add_two_numbers")
def add(x, y):
    return x + y