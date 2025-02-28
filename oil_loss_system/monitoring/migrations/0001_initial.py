# Generated by Django 5.1.3 on 2024-11-26 12:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OilProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('capacity', models.FloatField(help_text='Емкость хранилища (в литрах)')),
                ('temperature', models.FloatField(help_text='Температура в хранилище')),
                ('pressure', models.FloatField(help_text='Давление в хранилище')),
                ('oil_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoring.oilproduct')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('total_loss', models.FloatField(help_text='Общие потери за день (в литрах)')),
                ('storage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoring.storage')),
            ],
        ),
        migrations.CreateModel(
            name='Loss',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loss_type', models.CharField(choices=[('Evaporation', 'Испарение'), ('Leak', 'Утечка'), ('Chemical', 'Химический процесс'), ('Physical', 'Физический процесс')], max_length=50)),
                ('quantity', models.FloatField(help_text='Количество потерянного продукта (в литрах)')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('storage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoring.storage')),
            ],
        ),
    ]
