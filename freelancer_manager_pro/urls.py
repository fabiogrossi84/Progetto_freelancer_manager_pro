"""
URL configuration for freelancer_manager_pro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static # importo per le foto con debug=False

from freelancer_manager_pro import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("gestione_clienti.urls")),  # Aggiungo le URL dell’app gestione_clienti
    path("", include("home.urls")),  # Collego l'app home
    
] #+ static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0]) # lo tolgo con debug=True

"""if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])"""
    
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])    