from django.urls import path
from .views import home

urlpatterns = [
    path("", home, name="home"),  # La home sarà accessibile da "/"
]
