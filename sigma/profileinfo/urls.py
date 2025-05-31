from django.urls import path
from . import views

app_name = "profileinfo"
urlpatterns = [
    # contoh : /
    path("post/<int:id>/", views.post, name="post"),
    path("friend/<int:id>/", views.friend, name="friend"),
]
