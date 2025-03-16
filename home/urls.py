from django.urls import path
from .views import home

# Importo la classe TemplateView per la pagina test
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", home, name="home"),  # La home sarà accessibile da "/"
    
    # Pagina test ruoli, accessibile solo se loggato
    path("test-ruoli/", login_required(TemplateView.as_view(template_name="test_ruoli.html")), name="test_ruoli"),
    
]
