from django.urls import path, reverse_lazy
from .views import ClienteListView, ClienteDetailView, ClienteCreateView, ClienteUpdateView, ClienteDeleteView, CustomPasswordChangeView, dashboard_cliente, CustomLoginView
from django.contrib.auth import views as auth_views # Importo le viste di autenticazione di Django

urlpatterns = [
    path("clienti/", ClienteListView.as_view(), name="cliente-list"),
    path("clienti/<int:pk>/", ClienteDetailView.as_view(), name="cliente-detail"),
    path("clienti/nuovo/", ClienteCreateView.as_view(), name="cliente-create"),
    path("clienti/<int:pk>/modifica/", ClienteUpdateView.as_view(), name="cliente-update"),
    path("clienti/<int:pk>/elimina/", ClienteDeleteView.as_view(), name="cliente-delete"),
    # Cambio password obbligatorio per Clienti
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    # percorso dashboard cliente
    path('cliente/dashboard/', dashboard_cliente, name='dashboard_cliente'),
    # percorso login cliente
    path('login/', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),

    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
