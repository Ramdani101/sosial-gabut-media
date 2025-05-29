from django.urls import path

from . import views

app_name = "register"
urlpatterns = [
    #contoh : /login/
    path("", views.register, name="signup"),
]