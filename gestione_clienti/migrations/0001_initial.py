# Generated by Django 5.1.7 on 2025-03-15 17:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gestione_utenti', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('telefono_fisso', models.CharField(blank=True, max_length=20, null=True)),
                ('cellulare', models.CharField(blank=True, max_length=20, null=True)),
                ('azienda', models.CharField(blank=True, max_length=255, null=True)),
                ('data_creazione', models.DateTimeField(auto_now_add=True)),
                ('freelance', models.ForeignKey(limit_choices_to={'ruolo': 'F'}, on_delete=django.db.models.deletion.CASCADE, related_name='clienti_gestiti', to='gestione_utenti.user')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profilo_cliente', to='gestione_utenti.user')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clienti',
            },
        ),
        migrations.CreateModel(
            name='Progetto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('descrizione', models.TextField(blank=True, null=True)),
                ('stato', models.CharField(choices=[('IA', 'In Attesa'), ('IC', 'In Corso'), ('CO', 'Completato')], default='IA', max_length=2)),
                ('budget', models.DecimalField(decimal_places=2, max_digits=10)),
                ('data_creazione', models.DateTimeField(auto_now_add=True)),
                ('scadenza', models.DateField(blank=True, null=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progetti', to='gestione_clienti.cliente')),
            ],
            options={
                'verbose_name': 'Progetto',
                'verbose_name_plural': 'Progetti',
            },
        ),
    ]
