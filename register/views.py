"""
This module provides the backend logic for user registration, email validation,
and account activation for a Django-based CurrencyExchangeApp. It includes functions
to handle registration requests, send email confirmations,
verify email validity using NeverBounce SDK,
and activate user accounts.
"""


# pylint: disable=import-error
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import neverbounce_sdk
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from dotenv import load_dotenv
from .forms import RegisterForm


def register(request):
    """
    Handle registration request. If the POST request is valid,
    it checks for existing username or email.
    If validation passes, it creates the user, sends a registration email,
    and renders the activation view.

    Parameters:
    request: HttpRequest object containing metadata about the request.

    Returns:
    HttpResponse object with the registration form or activation page.
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            if User.objects.filter(username=username).exists():
                messages.error(request, 'The username already taken. Please try again.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'The email already taken. Please try again.')
            else:
                if check_if_email_is_valid(email):
                    user = form.save()
                    user.is_active = False
                    user.save()
                    send_registration_email(request, user)
                    messages.success(request, 'Account created successfully.')
                    return render(request, 'accounts/activate_email.html')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


# pylint: disable=too-many-locals
def send_registration_email(request, user):
    """
   Send a registration email to the user with an activation link.

   Parameters:
   request: HttpRequest object containing metadata about the request.
   user: User object representing the user to send the email to.

   """
    load_dotenv()
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_link = request.build_absolute_uri(
        reverse('register:activate_account', kwargs={'uidb64': uid, 'token': token})
    )
    smtp_server = os.environ.get('SMTP_SERVER')
    smtp_port = os.environ.get('SMTP_PORT')
    username = os.environ.get('MAIL_USERNAME')
    password = os.environ.get('MAIL_PASSWORD')
    sender = os.environ.get('SENDER')
    receiver = user.email
    subject = 'Welcome to CurrencyExchangeApp'

    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = subject

    email_body = f'''
    Hello {user} your account on CurrencyExchangeApp was created.
    Please confirm your email by clicking this link {activation_link} to activate your account.
    '''
    message.attach(MIMEText(email_body, "plain"))

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(username, password)
            server.sendmail(sender, receiver, message.as_string())
            print(f'Email has been sent to {user}')
    # pylint: disable=broad-exception-caught
    except Exception as e:
        print(f'Email could not be sent to {user}. Error: {e}')


def check_if_email_is_valid(email):
    """
    Check if the provided email is valid using the NeverBounce SDK.

    Args:
    email: A string representing the email address to validate.

    Returns:
    A boolean indicating whether the email is valid.
    """
    api_key = os.environ.get('API_EMAIL_KEY')
    client = neverbounce_sdk.client(api_key=api_key, timeout=30)
    resp = client.single_check(email)

    if resp['status'] == 'success':
        return True
    return False


def activate_account(request, uidb64, token):
    """
   Activate the user account after verifying the token and uidb64.

   Args:
   request: HttpRequest object containing metadata about the request.
   uidb64: A string representing the base64 encoded user ID.
   token: A string representing the token to verify the user.

   Returns:
   HttpResponse object with the account activation status.
   """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

    return render(request, 'accounts/activate_account.html')
