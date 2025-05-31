from django.contrib import admin
from .models import Profile

admin.site.user(Profile)