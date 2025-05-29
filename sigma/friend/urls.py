from django.urls import path
from . import views

app_name = "friend"
urlpatterns = [
    # contoh : /
    path("", views.friend, name="friend"),
]