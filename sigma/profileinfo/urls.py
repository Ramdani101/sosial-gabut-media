from django.urls import path
from . import views

app_name = "profileinfo"
urlpatterns = [
    # contoh : /
    path("", views.index, name="index"),
]
