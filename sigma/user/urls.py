from django.urls import path

from . import views

app_name = "user"
urlpatterns = [
    #contoh : /login/
    path("", views.registerView, name="signup"),
]