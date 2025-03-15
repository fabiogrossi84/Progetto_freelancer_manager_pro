from django.contrib import admin
from .models import Ticket, CommentoTicket

# Register your models here.

admin.site.register(Ticket)
admin.site.register(CommentoTicket)
