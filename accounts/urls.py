from django.urls import path
from .views import home

urlpatterns = [
    path('dashboard/', home, name='dashboard'),
]
