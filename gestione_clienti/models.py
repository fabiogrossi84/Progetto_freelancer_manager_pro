from django.db import models
from gestione_utenti.models import User
from django.urls import reverse




""" Questa app si occupa della gestione dei clienti e dei progetti.
    Un progetto è associato a un cliente e ha uno stato di avanzamento,
    In Attesa, In Corso, Completato.
    
    Il modello Cliente memorizza le informazioni dei clienti, 
    che possono avere più progetti e sono assegnati a un freelance.
    Contiene: 
    Nome, email, telefono, azienda
    Freelance assegnato (relazione con User)
    Data di creazione. 
    
    Aggiungo un segnale per creare in automatico un user cliente 
    quando viene aggiunto un cliente e l'invio mail con psw, 
    lo aggiungo con il file signals.py. """

# Create your models here.

class Cliente(models.Model):
    
    """ Modello per rappresentare i clienti. Ogni cliente è gestito da un freelance. 
    
    Ho aggiunto il collegamento del cliente con il suo user autogenerato. """
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profilo_cliente", null=True, blank=True)
    freelance = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'ruolo': 'F'}, 
        related_name="clienti_gestiti")
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefono_fisso = models.CharField(max_length=20, blank=True, null=True)
    cellulare = models.CharField(max_length=20, blank=True, null=True)
    azienda = models.CharField(max_length=255, blank=True, null=True)
    data_creazione = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clienti"

    def __str__(self):
        return self.user.username if self.user else self.nome
    
    def get_absolute_url(self):
        return reverse("cliente-detail", kwargs={"pk": self.pk}) #Redirect al dettaglio cliente
    
    
""" Modello progetto: memorizza i dettagli dei progetti associati ai clienti. """    

class Progetto(models.Model):
    
    """ Modello per gestire i progetti. Ogni progetto è associato a un cliente 
         e ha uno stato di avanzamento. """
    
    class StatoProgetto(models.TextChoices):
        IN_ATTESA = 'IA', 'In Attesa'
        IN_CORSO = 'IC', 'In Corso'
        COMPLETATO = 'CO', 'Completato'

    nome = models.CharField(max_length=255)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="progetti")
    freelance = models.ForeignKey("gestione_utenti.User", on_delete=models.CASCADE, limit_choices_to={'ruolo': 'F'}, related_name="progetti_gestiti")
    descrizione = models.TextField(blank=True, null=True)
    stato = models.CharField(max_length=2, choices=StatoProgetto.choices, default=StatoProgetto.IN_ATTESA)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    ore_lavorate = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    data_creazione = models.DateTimeField(auto_now_add=True)
    scadenza = models.DateField(blank=True, null=True)
    avanzamento_percentuale = models.PositiveSmallIntegerField(default=0)

    
    class Meta:
        verbose_name = "Progetto"
        verbose_name_plural = "Progetti"

    def __str__(self):
        return f"{self.nome} ({self.cliente.nome})" #Restituisce stringa leggibile

