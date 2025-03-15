from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
from gestione_utenti.models import User
from .models import Cliente
from django.utils.crypto import get_random_string

@receiver(post_save, sender=Cliente)
def crea_utente_cliente(sender, instance, created, **kwargs):
    
    """ Quando un cliente viene creato, genera automaticamente un utente Django con ruolo Cliente."""
    
    if created:
        password_generata = get_random_string(12) # ho tolto "User.objects.make_random_password()"
        user = User.objects.create(
            username=instance.email,
            email=instance.email,
            password=make_password(password_generata),
            ruolo=User.Ruolo.CLIENTE
        )
        print(f"Cliente {instance.nome} registrato. Email: {instance.email} - Password: {password_generata}")
