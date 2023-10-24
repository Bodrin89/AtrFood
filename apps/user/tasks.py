from django.conf import settings
from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from config.settings import LOGGER
from config.celery import app


@app.task
def confirmation_email(user_token, user_email, email_url, message, subject):
    domain = settings.ALLOWED_HOSTS[0]
    message = f'{message} {domain}/{email_url}/?token={user_token}'
    send_mail(subject, message, EMAIL_HOST_USER, [user_email, ])


@app.task
def update_email(user_token, email_url, message, subject, new_email):
    domain = settings.ALLOWED_HOSTS[0]
    message = f'{message} {domain}/{email_url}/?token={user_token}&email={new_email}'
    send_mail(subject, message, EMAIL_HOST_USER, [new_email, ])
    