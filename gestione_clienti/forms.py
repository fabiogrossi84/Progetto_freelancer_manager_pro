from django import forms
from .models import Cliente
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