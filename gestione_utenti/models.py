from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

""" Questa app si occupa della gestione degli utenti, che nel nostro caso sono:
   Admin → Supervisiona tutto il sistema.
   Freelance → Gestisce i clienti, i progetti e i ticket assegnati.

   Struttura dell’app:
   nell’app gestione_utenti, definiamo il modello User, 
   che estende il modello predefinito di Django (AbstractUser). """

# Create your models here.

""" Modello User
    Questo modello rappresenta tutti gli utenti del sistema.
    Lo utilizzo al posto del modello predefinito di Django (auth.User), 
    così posso personalizzare i campi e i permessi. """
    
class User(AbstractUser):
    """
    Modello personalizzato per gli utenti del sistema.
    Eredita da `AbstractUser` e aggiunge un campo `ruolo` per distinguere i tipi di utenti.
    """
    class Ruolo(models.TextChoices):
        FREELANCE = "F", "Freelance"
        ADMIN = "A", "Admin"

    ruolo = models.CharField(
        max_length=1,
        choices=Ruolo.choices,
        default=Ruolo.FREELANCE,
        verbose_name="Ruolo Utente"
    )
    
    # Risolvo il conflitto con `auth.User.groups`
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",
        blank=True
    )
    
    # Risolvo il conflitto con `auth.User.user_permissions`
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",
        blank=True
    )

    class Meta:
        verbose_name = "Utente"
        verbose_name_plural = "Utenti"

    def __str__(self):
        return f"{self.username} ({self.get_ruolo_display()})"

    def is_freelance(self):
        """Restituisce True se l'utente è un Freelance"""
        return self.ruolo == self.Ruolo.FREELANCE

    def is_admin_app(self):
        """Restituisce True se l'utente è un Admin"""
        return self.ruolo == self.Ruolo.ADMIN  

    @property
    def is_staff(self):
        """Django usa questo per l’accesso all'Admin Panel."""
        return self.is_admin_app()    