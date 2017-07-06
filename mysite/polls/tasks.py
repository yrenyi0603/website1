from __future__ import absolute_import, unicode_literals
from celery import task


@task
def add(x, y):
    return x + y


@task
def mul(x, y):
    return x * y


@task
def xsum(numbers):
    return sum(numbers)
from django.core.mail import send_mail
from django.core.mail import EmailMessage
@task
def setemail(subject,message,from_email,recipient_list,cc_email):
    email=EmailMessage(
        subject,
        message,
        from_email,
        recipient_list,
        cc_email
    )
    email.send()
