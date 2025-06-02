from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Profile
from datetime import date

def registerView(request):

    if request.method == 'POST':
        if request.POST.get('password') != request.POST.get('passwordConfirm'):
            messages.error(request, "Passwords do not match.")
            return redirect('register')
        
        if User.objects.filter(username=request.POST.get('username')).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')
        
        username    = request.POST.get('username')
        email       = request.POST.get('email')
        password    = request.POST.get('password')
        birth_day   = request.POST.get('date')
        birth_month = request.POST.get('month')
        birth_year  = request.POST.get('year')
        # Convert day, month, year into a date
        try:
            birth_date = date(int(birth_year), int(birth_month), int(birth_day))
        except ValueError:
            messages.error(request, "Invalid birth date.")
            return redirect('register')

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)

        # Profile akan otomatis dibuat oleh signals, tinggal update birth_date
        user.profile.birth_date = birth_date
        user.profile.save()

        messages.success(request, "User registered successfully.")
        return redirect('login')
    print("register failed")
    return render(request, 'register/signup.html')

def loginView(request):
    print("login page")
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        print(f"Authenticating user: {username}")
        if user is not None:
            login(request, user)

            Profile.objects.get_or_create(user=user)
            print(f"User {username} logged in with pk: {user.pk}")
            return redirect('home:index')
        else:
            messages.error(request, 'Username atau password salah.')

    return render(request, 'register/login.html')

def logout(request):
    return render(request, 'register/logout.html')