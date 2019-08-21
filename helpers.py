from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from uuid import uuid4
from datetime import datetime, date


def send_user_mail(**kwargs):
    message = render_to_string(kwargs.get('template'), {
        'first_name': kwargs.get('first_name'),
        'last_name': kwargs.get('last_name'),
        'activation_url': kwargs.get('activation_url')
    })
    email = EmailMultiAlternatives(kwargs.get('subject'), message, settings.EMAIL_HOST_USER, [kwargs.get('user').email])
    email.content_subtype = 'html'
    email.mixed_subtype = 'related'
    email.send(fail_silently=False)


def generate_activation_token():
    return str(uuid4()).replace('-', '')


def generate_unique_name(name):
    token = generate_activation_token()
    res = name + token
    result = ''.join(res.split(' '))
    return result


def generate_game_link():
    now = datetime.now()
    today = date.today()
    date_pattern = today.day + today.month + today.year
    time = datetime.time(now)
    time_pattern = time.hour + time.minute + time.second
    random_token = generate_activation_token()
    game_link = 'tictactoe' + str(date_pattern) + random_token + str(time_pattern)
    return game_link
