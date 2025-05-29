from django.urls import path
from . import views

app_name = "home"
urlpatterns = [
    # contoh : /
    path("", views.index, name="index"),
]
