from django.urls import path
from .views import ClienteListView, ClienteDetailView, ClienteCreateView, ClienteUpdateView, ClienteDeleteView

urlpatterns = [
    path("clienti/", ClienteListView.as_view(), name="cliente-list"),
    path("clienti/<int:pk>/", ClienteDetailView.as_view(), name="cliente-detail"),
    path("clienti/nuovo/", ClienteCreateView.as_view(), name="cliente-create"),
    path("clienti/<int:pk>/modifica/", ClienteUpdateView.as_view(), name="cliente-update"),
    path("clienti/<int:pk>/elimina/", ClienteDeleteView.as_view(), name="cliente-delete"),
]
