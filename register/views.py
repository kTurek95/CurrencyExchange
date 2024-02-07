import smtplib
from django.shortcuts import render, redirect
from django.urls import reverse
from os import getenv
from dotenv import load_dotenv
from .forms import RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_registration_email(user)
            return redirect(reverse('register:home'))
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def send_registration_email(user):
    load_dotenv()
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    username = getenv('EMAIL_USERNAME')
    password = getenv('EMAIL_PASSWORD')
    sender = getenv('EMAIL_SENDER')
    receiver = [user.email]
    message = f'Hello {user} your account was created'
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(username, password)
        server.sendmail(sender, receiver, message)
        print(f'Email has been sent to {user}')