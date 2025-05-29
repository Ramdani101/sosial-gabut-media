from django.urls import path
from . import views

app_name = "friend"
urlpatterns = [
    path("", views.friend, name="friend"),
    path("<int:user_id>/", views.friend_list, name="friend_list"),
]

