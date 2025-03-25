from django import forms
from .models import Cliente, Progetto
from gestione_utenti.models import User

class ClienteForm(forms.ModelForm):
    
    freelance = forms.ModelChoiceField(
        queryset=User.objects.filter(ruolo="F"),  # Mostra solo Freelance
        empty_label="Seleziona un Freelance",
        required=True  # Freelance obbligatorio
    )
    
    
    class Meta:
        model = Cliente
        fields = ["nome", "email", "azienda", "telefono_fisso", "cellulare"]
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # Ottengo l'utente che sta creando il Cliente
        super().__init__(*args, **kwargs)

        # Se l'utente è un Freelance, assegno automaticamente il campo e lo nascondo
        # Se l'utente è un Admin, mostro il campo Freelance
        if user and user.is_freelance():
            self.fields["freelance"].initial = user
            self.fields["freelance"].widget = forms.HiddenInput()
            
#Form per progetto

class ProgettoForm(forms.ModelForm):
    class Meta:
        model = Progetto
        fields = [
            "nome",
            "cliente",
            "freelance",
            "descrizione",
            "stato",
            "budget",
            "ore_lavorate",
            "scadenza",
            "avanzamento_percentuale",
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(ProgettoForm, self).__init__(*args, **kwargs)

        if user:
            if user.is_freelance():
                # Freelance può vedere solo i suoi clienti
                self.fields["cliente"].queryset = user.clienti_gestiti.all()
                # Freelance non può modificare il campo freelance
                self.fields["freelance"].widget = forms.HiddenInput()
            elif user.is_admin_app():
                # Admin vede tutti i freelance
                self.fields["freelance"].queryset = User.objects.filter(ruolo="F")
