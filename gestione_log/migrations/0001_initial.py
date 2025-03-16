# Generated by Django 5.1.7 on 2025-03-16 00:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gestione_clienti', '0001_initial'),
        ('gestione_fatture', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportProgetto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ore_lavorate', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('spese_totali', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('fatture_progetto', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('fatture_ticket', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('data_generazione', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Report Progetto',
                'verbose_name_plural': 'Report Progetti',
            },
        ),
        migrations.CreateModel(
            name='AttivitaLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('azione', models.CharField(max_length=255)),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('dettagli', models.TextField(blank=True, null=True)),
                ('fattura', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='log_fattura', to='gestione_fatture.fattura')),
                ('progetto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='log_progetto', to='gestione_clienti.progetto')),
            ],
            options={
                'verbose_name': 'Attività Log',
                'verbose_name_plural': 'Attività Log',
            },
        ),
    ]
