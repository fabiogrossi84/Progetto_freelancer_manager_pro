from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
from gestione_utenti.models import User
from .models import Cliente
from django.utils.crypto import get_random_string

@receiver(post_save, sender=Cliente)
def crea_utente_cliente(sender, instance, created, **kwargs):
    
    """ Quando un cliente viene creato, si genera automaticamente 
        un utente Django con ruolo Cliente e cliente si collega col suo user. 
        
        MA prima di salvare un cliente devo creare l'utente."""
    
    if created and instance.user is None:  # Se il cliente non ha ancora un user
        password_generata = get_random_string(12) 
        # ho tolto "User.objects.make_random_password() e genero psw casuale."
        user = User.objects.create(
            username=instance.email,
            email=instance.email,
            first_name=instance.nome.split()[0],  # Prendo il primo nome (Faccio lo split)
            last_name=" ".join(instance.nome.split()[1:]) if " " in instance.nome else "",  # Se ha più parole, le metto nel cognome
            password=make_password(password_generata),
            ruolo=User.Ruolo.CLIENTE
        )
        
        instance.user = user  # Collega il Cliente al suo User 
        instance.save(update_fields=['user'])  # Salva il Cliente aggiornato
        
        print(f"Cliente {instance.nome} registrato. Email: {instance.email} - Password: {password_generata}")
