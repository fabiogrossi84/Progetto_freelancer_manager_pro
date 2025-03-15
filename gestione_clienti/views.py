from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Cliente
from .forms import ClienteForm

# Create your views here.

# Lista Clienti (Solo Admin e Freelance vedono i propri clienti)
class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = "gestione_clienti/cliente_list.html"
    context_object_name = "clienti"

    def get_queryset(self):
        user = self.request.user
        if user.is_admin_app():
            return Cliente.objects.all()
        elif user.is_freelance():
            return Cliente.objects.filter(freelance=user)
        else:
            return Cliente.objects.filter(user=user)

# Dettaglio Cliente (Solo Freelance e Admin)
class ClienteDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Cliente
    template_name = "gestione_clienti/cliente_detail.html"

    def test_func(self):
        cliente = self.get_object()
        return self.request.user.is_admin_app() or cliente.freelance == self.request.user

# Creazione Cliente (Solo Admin e Freelance)
class ClienteCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "gestione_clienti/cliente_form.html"

    def test_func(self):
        return self.request.user.is_admin_app() or self.request.user.is_freelance()

    def form_valid(self, form):
        form.instance.freelance = self.request.user if self.request.user.is_freelance() else form.instance.freelance
        return super().form_valid(form)

# Modifica Cliente
class ClienteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "gestione_clienti/cliente_form.html"
    success_url = reverse_lazy("cliente-list") # Redirect alla lista dei clienti
    
    def test_func(self):
        cliente = self.get_object()
        return self.request.user.is_admin_app() or cliente.freelance == self.request.user

# Eliminazione Cliente (Solo Admin)
class ClienteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Cliente
    template_name = "gestione_clienti/cliente_confirm_delete.html"
    success_url = reverse_lazy("cliente-list")

    def test_func(self):
        return self.request.user.is_admin_app()