# Generated by Django 5.1.7 on 2025-03-15 17:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gestione_clienti', '0001_initial'),
        ('gestione_ticket', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fattura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('importo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('data_emissione', models.DateField(auto_now_add=True)),
                ('pagata', models.BooleanField(default=False)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fatture', to='gestione_clienti.cliente')),
                ('progetto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fatture', to='gestione_clienti.progetto')),
                ('ticket', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fatture', to='gestione_ticket.ticket')),
            ],
            options={
                'verbose_name': 'Fattura',
                'verbose_name_plural': 'Fatture',
            },
        ),
    ]
