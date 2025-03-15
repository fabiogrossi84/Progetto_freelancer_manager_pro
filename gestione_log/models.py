from django.db import models
from gestione_clienti.models import Progetto
from gestione_utenti.models import User
from gestione_ticket.models import Ticket
from gestione_fatture.models import Fattura
from django.db.models import Sum

"""Questa app si occupa di registrare le attività importanti nel sistema 
   e generare report automatici su ticket e progetti. """

# Create your models here.

class AttivitaLog(models.Model):
    
    """ Modello per registrare le attività degli utenti nel sistema.
    Registra azioni relative a Ticket, Fatture e Progetti. """
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    azione = models.CharField(max_length=255)
    data = models.DateTimeField(auto_now_add=True)
    dettagli = models.TextField(blank=True, null=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.SET_NULL, blank=True, null=True, related_name="log_ticket")
    fattura = models.ForeignKey(Fattura, on_delete=models.SET_NULL, blank=True, null=True, related_name="log_fattura")
    progetto = models.ForeignKey(Progetto, on_delete=models.SET_NULL, blank=True, null=True, related_name="log_progetto")

    class Meta:
        verbose_name = "Attività Log"
        verbose_name_plural = "Attività Log"

    def __str__(self):
        riferimento = "Sistema"
        if self.user:
            riferimento = self.user.username
        if self.ticket:
            return f"{riferimento} - {self.azione} sul Ticket '{self.ticket.titolo}' ({self.data.strftime('%d/%m/%Y %H:%M')})"
        if self.fattura:
            return f"{riferimento} - {self.azione} sulla Fattura #{self.fattura.id} ({self.data.strftime('%d/%m/%Y %H:%M')})"
        if self.progetto:
            return f"{riferimento} - {self.azione} sul Progetto {self.progetto.nome} ({self.data.strftime('%d/%m/%Y %H:%M')})"
        return f"{riferimento} - {self.azione} ({self.data.strftime('%d/%m/%Y %H:%M')})"
    
class ReportProgetto(models.Model):
    
    """ Modello per tracciare le statistiche su un progetto.
    Registra ore lavorate, spese totali e fatturazione totale. """
    
    progetto = models.ForeignKey(Progetto, on_delete=models.CASCADE, related_name="report")
    ore_lavorate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    spese_totali = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fatture_progetto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fatture_ticket = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data_generazione = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Report Progetto"
        verbose_name_plural = "Report Progetti"

    def __str__(self):
        return f"Report {self.progetto.nome} - {self.data_generazione.strftime('%d/%m/%Y')}"

    def aggiorna_dati(self):
        
        """ Aggiorna il report con i nuovi dati dal database."""
        
        self.fatture_progetto = Fattura.objects.filter(progetto=self.progetto).aggregate(Sum('importo'))['importo__sum'] or 0
        self.fatture_ticket = Fattura.objects.filter(ticket__progetto=self.progetto).aggregate(Sum('importo'))['importo__sum'] or 0
        self.save()    