from django.shortcuts import render
from user.models import Profile

def homeView(request):
    return render(request, "home/index.html")
