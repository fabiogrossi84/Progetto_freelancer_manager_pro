from django.contrib import admin
from .models import Cliente, Progetto

# Register your models here.

class ClienteAdmin(admin.ModelAdmin):
    
    """ Nasconde il campo 'user' nel Django Admin perché viene generato automaticamente. """
    
    exclude = ('user',)  # Rimuove il campo dal form in Admin


admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Progetto)