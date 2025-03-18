from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from gestione_utenti.models import User
from .models import Cliente

class ClienteTestCase(TestCase):
    def setUp(self):
        # ✅ Crea un Admin e un Freelance Pro
        self.admin = User.objects.create_user(username="admin", password="adminpass", ruolo="A")
        self.freelance_pro = User.objects.create_user(username="freelancepro", password="freelancepass", ruolo="F", freelancepro=True)

        # ✅ Client per simulare login
        self.client = Client()

    def test_creazione_cliente_e_user(self):
        """Test: Freelance Pro crea Cliente → si genera User cliente"""

        self.client.login(username="freelancepro", password="freelancepass")

        response = self.client.post(reverse("cliente-create"), {
            "nome": "Mario Rossi",
            "email": "mario@example.com",
            "azienda": "ACME",
            "telefono_fisso": "123456789",
            "cellulare": "987654321"
        })

        # Controlla redirect dopo creazione
        self.assertEqual(response.status_code, 302)

        # Controlla se Cliente e User sono stati creati
        cliente = Cliente.objects.get(email="mario@example.com")
        self.assertIsNotNone(cliente.user)

        # Controlla se password fissa è impostata
        self.assertTrue(check_password("cliente-123", cliente.user.password))

    def test_eliminazione_cliente_elimina_user(self):
        """Test: Elimina Cliente → elimina User associato"""

        cliente_user = User.objects.create_user(username="cliente1", password="cliente-123", ruolo="C")
        cliente = Cliente.objects.create(nome="Mario", email="cliente1@example.com", freelance=self.freelance_pro, user=cliente_user)

        cliente.delete()

        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username="cliente1")

    def test_freelance_limitato_non_puo_creare_cliente(self):
        """Test: Freelance Limitato → accesso negato alla creazione cliente"""

        freelance_limitato = User.objects.create_user(username="freelancelimit", password="limitpass", ruolo="F", freelancepro=False)

        self.client.login(username="freelancelimit", password="limitpass")
        
        response = self.client.get(reverse("cliente-create"))

        # Freelance Limitato deve ricevere 403 Forbidden (non autorizzato)
        self.assertEqual(response.status_code, 403)

    def test_eliminazione_user_cliente_prima_del_cliente(self):
        """Test: Eliminare prima User, poi Cliente → deve funzionare senza errori"""

        user_cliente = User.objects.create_user(username="cliente3", password="cliente-123", ruolo="C")
        cliente = Cliente.objects.create(nome="Marco", email="cliente3@example.com", freelance=self.freelance_pro, user=user_cliente)

        # Elimino l'utente prima
        user_cliente.delete()

        # Ora elimino il cliente → il signal non deve dare errore
        try:
            cliente.delete()
            no_error = True
        except Exception as e:
            no_error = False
            print(f"Errore: {e}")

        self.assertTrue(no_error, "Errore nell'eliminare cliente dopo user associato")

    def test_accesso_dashboard_cliente_redirect_cambio_password(self):
        """Test: Cliente con password fissa → redirect a cambio password"""

        user_cliente = User.objects.create_user(username="cliente2", password="cliente-123", ruolo="C")
        cliente = Cliente.objects.create(nome="Luigi", email="cliente2@example.com", freelance=self.freelance_pro, user=user_cliente)

        self.client.login(username="cliente2", password="cliente-123")

        response = self.client.get(reverse("dashboard_cliente"))
        self.assertRedirects(response, reverse("password_change"))

