from django.urls import path
from . import views

urlpatterns = [
    path('friend/', views.index)
]
