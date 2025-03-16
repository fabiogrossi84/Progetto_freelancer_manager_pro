from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Cliente
from .forms import ClienteForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib import messages

# Create your views here.

# Lista Clienti (Solo Admin e Freelance vedono i propri clienti)
class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = "gestione_clienti/cliente_list.html"
    context_object_name = "clienti"
    
    """ Indirizzo il cliente al primo login a cambiare la password """
    """def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.ruolo == "C" and user.check_password("cliente-123"):
            return redirect(reverse("password_change"))
        return super().dispatch(request, *args, **kwargs)"""
    
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

    """def test_func(self):
        cliente = self.get_object()
        return self.request.user.is_admin_app() or cliente.freelance == self.request.user"""
        
    """ Cambio funzione perchè il cliente non vede i suoi dettagli """  
    
    def test_func(self):
        cliente = self.get_object()
        user = self.request.user
        return (
            user.is_admin_app()
            or cliente.freelance == user
            or cliente.user == user  # Cliente accede al proprio dettaglio
    )
  

# Creazione Cliente (Solo Admin e Freelance)
class ClienteCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "gestione_clienti/cliente_form.html"

#modifico dopo aggiunta di freelance pro
    def test_func(self):
        user = self.request.user
        return user.is_admin_app() or (user.is_freelance() and user.is_freelance_pro)
    
    def get_form_kwargs(self):
        """ Passo l'utente al form """
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user  # Passa l'utente corrente al form
        return kwargs
    
    def form_valid(self, form):
        """ Assegna sempre un Freelance al Cliente prima di salvarlo """

        if self.request.user.is_freelance():
            # Se il Freelance crea un Cliente, lo assegniamo automaticamente a lui
            form.instance.freelance = self.request.user

        elif form.cleaned_data.get("freelance"):
            # Se l'Admin ha selezionato un Freelance, lo assegniamo
            form.instance.freelance = form.cleaned_data.get("freelance")
            
        else:
            # Se l'Admin non ha selezionato un Freelance, mostriamo un errore
            form.add_error("freelance", "Devi selezionare un Freelance per questo Cliente.")
            return self.form_invalid(form)

        return super().form_valid(form)




# Modifica Cliente
class ClienteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "gestione_clienti/cliente_form.html"
    success_url = reverse_lazy("cliente-list") # Redirect alla lista dei clienti

# modifico per freelance pro    
    def test_func(self):
        cliente = self.get_object()
        user = self.request.user

        if user.is_admin_app():
            return True
        elif user.is_freelance() and user.is_freelance_pro and cliente.freelance == user:
            return True
        return False  # Freelance limitato e altri → bloccati


# Eliminazione Cliente (Solo Admin)
class ClienteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Cliente
    template_name = "gestione_clienti/cliente_confirm_delete.html"
    success_url = reverse_lazy("cliente-list")

    def test_func(self):
        return self.request.user.is_admin_app()
    
    # nuova funzione per concedere accesso solo al cliente
    
@login_required
def dashboard_cliente(request):
    user = request.user

    # 🔒 Blocca accesso a chi NON è Cliente
    if user.ruolo != "C":
        return redirect("cliente-list")  # Admin e Freelance vanno alla lista clienti

    # 🔐 Se Cliente ha ancora la password fissa, forza cambio password
    if user.check_password("cliente-123"):
        return redirect("password_change")

    # ✅ Recupera i dati cliente
    cliente = get_object_or_404(Cliente, user=user)
    progetti = cliente.progetti.all()

    totale = progetti.count()
    in_corso = progetti.filter(stato="IC").count()
    completati = progetti.filter(stato="CO").count()

    context = {
        "cliente": cliente,
        "progetti": progetti,
        "totale": totale,
        "in_corso": in_corso,
        "completati": completati
    }
    return render(request, "gestione_clienti/dashboard_cliente.html", context)

    
    
"""@login_required # (è una funzione e non modifica oggetti)
def dashboard_cliente(request):
    user = request.user
    if user.ruolo == "C" and user.check_password("cliente-123"):
        return redirect("password_change")

    cliente = get_object_or_404(Cliente, user=user)
    progetti = cliente.progetti.all()

    totale = progetti.count()
    in_corso = progetti.filter(stato="IC").count()
    completati = progetti.filter(stato="CO").count()

    context = {
        "cliente": cliente,
        "progetti": progetti,
        "totale": totale,
        "in_corso": in_corso,
        "completati": completati
    }
    return render(request, "gestione_clienti/dashboard_cliente.html", context)"""   

#vista per rindirizzare i clienti loggati alla dashboard

class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.ruolo == "C":
            return reverse_lazy('dashboard_cliente')
        else:
            return reverse_lazy('cliente-list')
        
#classe per salvare password e reindirizzare

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change.html'
    success_url = reverse_lazy('dashboard_cliente')  # Redirect sicuro    
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "✅ Password modificata con successo!")
        return response    
        