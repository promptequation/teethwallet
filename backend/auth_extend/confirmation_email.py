import os
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .email_verification_token import account_activation_token


def send_confirmation_email(email, user):
    context = {
        'small_text_detail': 'Please verify your email address to set up your account.',
        'email': email,
        'domain': os.environ.get("SITE_URL"),
        'uuid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'first_name': user.first_name,
        'last_name': user.last_name
    }
    msg_html = render_to_string('verification_email.html', context)
    send_mail(
        'Verification Email',
        os.environ.get("DEFAULT_FROM_NAME"),
        os.environ.get("DEFAULT_FROM_EMAIL"),
        [email],
        html_message=msg_html,
        fail_silently=False,
    )


def email_confirmation_text(user):
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name
    }
    msg_html = render_to_string('email_verification_text.html', context)
    send_mail(
        'Confirmation Sign In to OeHMP - Keep track of what makes you smile.',
        os.environ.get("DEFAULT_FROM_NAME"),
        os.environ.get("DEFAULT_FROM_EMAIL"),
        [user.email],
        html_message=msg_html,
        fail_silently=False,
    )
