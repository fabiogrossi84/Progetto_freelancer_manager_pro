from django.contrib import admin
from .models import User
from django import forms

# Register your models here.

# Form personalizzato per il backend per le opzioni di spunta
class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        ruolo = cleaned_data.get("ruolo")
        is_staff = cleaned_data.get("is_staff")
        is_freelance_pro = cleaned_data.get("is_freelance_pro")

        # 🔐 Solo Freelance Pro può avere is_staff=True
        if ruolo == "F":
            if is_freelance_pro and not is_staff:
                raise forms.ValidationError("Un Freelance Pro deve avere is_staff=True.")
            if not is_freelance_pro and is_staff:
                raise forms.ValidationError("Un Freelance Limitato non può avere is_staff=True.")
        return cleaned_data


#admin.site.register(User)

""" Nuova registrazione di User """
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm  # 🔧 Usa il form personalizzato
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



