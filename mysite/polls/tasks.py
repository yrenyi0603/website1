from __future__ import absolute_import, unicode_literals
from celery import task
from celery.utils.log import get_task_logger
logger=get_task_logger(__name__)
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

import subprocess
def masscan_check(hosts):
    ips = " ".join(hosts)
    # command="/home/yrenyi/PycharmProjects/website1/mysite/tools/masscan --rate 1000000 -p1-65535  {0}".format(ips)
    # sudopass=open('/home/yrenyi/PycharmProjects/website1/mysite/tools/sudopass')
    # echo = subprocess.Popen(['echo', '\'abc123!@#\''],stdout=subprocess.PIPE)
    child1 = subprocess.Popen("sudo /home/yrenyi/PycharmProjects/website1/mysite/tools/masscan --rate 100000 -p1-65535  {0} | grep \"open\" \|awk \'{{print $6}}\'".format(ips),
                              shell=True, stdout=subprocess.PIPE)
    child1.wait()
    out = child1.communicate()
    logger.info('result is {0}'.format(out[0]))
    # from nmap import   nmap
    return list(set(hosts) - set(out[0].split()))
@task(bind=True,autoretry_for=(Exception,),ignore_result=True)
def sendemail2(self,subject,message,from_email="",recipient_list="",cc_email=""):
    # backend = EmailBackend(host='mail.ims.cn', port=25, username='dop1@ims.cn', password='abc123!@#')
    from django.core.mail import  message as msg
    from_email = from_email or 'dop6@ims.cn'
    recipient_list = recipient_list or ['dop1@ims.cn']
    cc_email = cc_email or ['dop7@ims.cn']
    with mail.get_connection(host='mail.ims.cn', port=25, username='dop6@ims.cn', password='abc123!@#') as connection:
        msg=mail.EmailMessage(
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
        )
        msg.content_subtype="html"
        msg.send()
from .models import EmailcheckModel,PowercheckModel
import json
import datetime
from django.template.loader import get_template
# @task(bind=True,autoretry_for=(Exception,), max_retries=5,default_retry_delay=60*1,ignore_result=True)
@task(bind=True)
def sendEmailList(self):
    n=datetime.date.today()
    emails= EmailcheckModel.objects.all()
    template=get_template('emails/passwd_notice.html')

    result=[]
    for i in emails:
        try:
            d=(n-i.lastcgdate).days
            if d >= 90-7 and d < 90:
                sendemail2.delay(subject='提醒:您的邮箱密码即将过期',message=template.render({'email':i.email,'day':90-int(d)}))
                logger.info('email:{0}'.format(i.email))
                result.append(i.email)
        except TypeError as e:
            pass
    logger.info('emails:{0}'.format(result))
    # sendemail2.delay(subject='email list', message=json.dumps(result))
    # sendemail2(subject='email list', message=json.dumps(result))

# @task
# def sendIpAddress(ignore_result=True):
#     ip=[i.ipaddress for i in PowercheckModel.objects.filter(status__exact='Enable')]
#     # masscan_check(ip)
#     sendemail2(subject='ip list', message=json.dumps(masscan_check(ip)))
