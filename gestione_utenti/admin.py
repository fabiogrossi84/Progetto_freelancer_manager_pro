from django.contrib import admin
from .models import User

# Register your models here.

#admin.site.register(User)

""" Nuova registrazione di User """
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "ruolo", "is_freelance_pro", "is_staff")
    list_filter = ("ruolo", "is_freelance_pro", "is_staff")
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Permessi", {"fields": ("ruolo", "is_staff", "is_superuser", "is_freelance_pro")}),
        ("Informazioni personali", {"fields": ("first_name", "last_name")}),
    )

# limito l'accesso al pannello admin al freelance non pro

def has_module_permission(self, request):
    if request.user.ruolo == "F" and not request.user.is_freelance_pro:
        return False  # Freelance limitato → bloccato
    return super().has_module_permission(request)

