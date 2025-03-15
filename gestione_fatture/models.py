from django.db import models
from gestione_clienti.models import Progetto, Cliente
from gestione_ticket.models import Ticket
from django.core.exceptions import ValidationError

"""  Questa app si occupa della gestione delle fatture, che possono essere collegate a: 
     Un progetto (fatturazione per un intero progetto).
     Un ticket (fatturazione per assistenza o interventi singoli).
     Regole importanti:
     Una fattura può essere associata solo a un progetto o a un ticket, mai entrambi.
     Le fatture possono essere pagate o non pagate.
     Solo gli admin e i freelance possono segnare una fattura come pagata. """
     
     # Create your models here.

class Fattura(models.Model):
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="fatture")
    progetto = models.ForeignKey(Progetto, on_delete=models.SET_NULL, blank=True, null=True, related_name="fatture")
    ticket = models.ForeignKey(Ticket, on_delete=models.SET_NULL, blank=True, null=True, related_name="fatture")
    importo = models.DecimalField(max_digits=10, decimal_places=2)
    data_emissione = models.DateField(auto_now_add=True)
    pagata = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Fattura"
        verbose_name_plural = "Fatture"

    def clean(self):
        
        """ Evita che una fattura sia collegata sia a un Ticket 
        che a un Progetto contemporaneamente. """
        
        if self.progetto and self.ticket:
            raise ValidationError("Una fattura non può essere collegata sia a un Ticket che a un Progetto.")

    def __str__(self):
        if self.progetto:
            return f"Fattura {self.id} - Progetto {self.progetto.nome} ({'Pagata' if self.pagata else 'Da Pagare'})"
        elif self.ticket:
            return f"Fattura {self.id} - Ticket {self.ticket.titolo} ({'Pagata' if self.pagata else 'Da Pagare'})"
        return f"Fattura {self.id} - Senza riferimento ({'Pagata' if self.pagata else 'Da Pagare'})"