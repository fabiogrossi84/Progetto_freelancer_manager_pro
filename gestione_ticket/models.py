from django.db import models
from gestione_clienti.models import Cliente, Progetto
from gestione_utenti.models import User

""" Questa app gestisce il sistema di supporto clienti tramite ticket.
    I freelance assegnati possono gestire e risolvere i ticket.
    I ticket possono essere collegati a un progetto, ma possono anche essere indipendenti.
    Sistema di comunicazione interna nei ticket:
    i clienti e i freelance possono scambiarsi messaggi. """

# Create your models here.

class Ticket(models.Model):
    
    class StatoTicket(models.TextChoices):
        APERTO = 'A', 'Aperto'
        IN_LAVORAZIONE = 'I', 'In Lavorazione'
        RISOLTO = 'R', 'Risolto'

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="ticket")
    progetto = models.ForeignKey(Progetto, on_delete=models.SET_NULL, blank=True, null=True, related_name="ticket")
    titolo = models.CharField(max_length=255)
    descrizione = models.TextField()
    stato = models.CharField(max_length=1, choices=StatoTicket.choices, default=StatoTicket.APERTO)
    assegnato_a = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, 
        related_name="ticket_assegnati", limit_choices_to={'ruolo': 'F'}
    )
    data_creazione = models.DateTimeField(auto_now_add=True)
    ultima_modifica = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Ticket"

    def __str__(self):
        return f"{self.titolo} ({self.get_stato_display()})"
    
class CommentoTicket(models.Model):
    
    """ Modello per i commenti all'interno di un Ticket.
    Permette la comunicazione tra il cliente e il freelance. """
    
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="commenti")
    autore = models.ForeignKey(User, on_delete=models.CASCADE)
    testo = models.TextField()
    data_creazione = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Commento Ticket"
        verbose_name_plural = "Commenti Ticket"

    def __str__(self):
        return f"{self.autore.username} - {self.data_creazione.strftime('%d/%m/%Y %H:%M')}"
    