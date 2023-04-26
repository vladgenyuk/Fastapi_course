import smtplib
from email.message import EmailMessage

from celery import Celery
from config import SMTP_USER, SMTP_PASSWORD, REDIS_HOST, REDIS_PORT

SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 465

celery = Celery('tasks', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}')


def get_email_template(username: str):
    email = EmailMessage()
    email['Subject'] = 'Traded'
    email['From'] = SMTP_USER
    email['To'] = SMTP_USER

    email.set_content(
        f'Hello {username}'
    )
    return email


@celery.task
def send_email_report(username: str):
    email = get_email_template(username)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email) #VladSMTP - gaxynhtqdmbgvecy

