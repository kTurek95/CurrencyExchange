from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('register:home'))
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})