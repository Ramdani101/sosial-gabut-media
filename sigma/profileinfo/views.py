from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

def post(request, id):
    user_profile = get_object_or_404(User, id=id)
    return render(request, "profileinfo/post.html", {"user_profile": user_profile})

def friend(request, id):
    user_profile = get_object_or_404(User, id=id)
    return render(request, "profileinfo/friend.html", {"user_profile": user_profile})
