from django.apps import AppConfig


class GestioneClientiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestione_clienti'
    
    """# Attiva i signals per la creazione automatica degli utenti (clienti)
    def ready(self):
        from django.utils.module_loading import autodiscover_modules
        autodiscover_modules("signals")  # Carica i segnali in modo sicuro 
        (tolto perchè cosi cerca cartelle e non file)"""
        
    def ready(self):
        import gestione_clienti.signals  # Import diretto e sicuro   
        