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
from django.core import mail
from django.core.mail.backends.smtp import EmailBackend


def sendemail2(subject,message,from_email="",recipient_list="",cc_email=""):
    # backend = EmailBackend(host='mail.ims.cn', port=25, username='dop1@ims.cn', password='abc123!@#')
    from django.core.mail import  message as msg
    from_email = from_email or 'dop6@ims.cn'
    recipient_list = recipient_list or ['dop1@ims.cn']
    cc_email = cc_email or ['dop7@ims.cn']
    with mail.get_connection(host='mail.ims.cn', port=25, username='dop6@ims.cn', password='abc123!@#') as connection:
        mail.EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=recipient_list,
            cc=cc_email,
            connection=connection,
            headers={"X-Priority":"1 (High)",
                     #'X-MSMail-Priority':'High',
                     # 'Importance':'High'
                     }
            # headers={"Message-ID":msg.make_msgid(idstring='yangry',domain='wosign.com')}
        ).send()
from .models import EmailcheckModel,PowercheckModel
import json
@task
def sendEmailList():
    emails=[i.email for i in EmailcheckModel.objects.all()]
    sendemail2(subject='email list',message=json.dumps(emails))
@task
def sendIpAddress():
    ip=[i.ipaddress for i in PowercheckModel.objects.filter(status__exact='Enable')]
    sendemail2(subject='ip list', message=json.dumps(ip))
