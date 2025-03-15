from django.apps import AppConfig


class GestioneClientiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestione_clienti'
    
    # Attiva i signals per la creazione automatica degli utenti (clienti)
    def ready(self):
        import gestione_clienti.signals  
        