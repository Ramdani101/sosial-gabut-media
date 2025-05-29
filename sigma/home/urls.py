from django.urls import path
from . import views

app_name = "home"
urlpatterns = [
    # contoh : /
    path("", views.index, name="index"),
    path('like/<int:id>/', views.like_post, name='like_post'),
    path('share/<int:id>/', views.share_post, name='share_post'),
    path('get_post_comment/<int:id>/', views.get_post_comment, name='get_post_comment'),
    path('comment/<int:id>/', views.comment_post, name='comment_post'),
]
