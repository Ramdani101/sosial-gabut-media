from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register/register.html', {'form': form})

def login(request):
    return render(request, 'register/login.html')

def logout(request):
    return render(request, 'register/logout.html')