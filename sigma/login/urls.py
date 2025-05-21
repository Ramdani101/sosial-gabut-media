from django.urls import path

from . import views

app_name = "login"
urlpatterns = [
    #contoh : /login/
    path("", views.index, name="index"),
]