# Generated by Django 5.1.7 on 2025-04-06 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GoTravel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Destinos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destino', models.CharField(max_length=100)),
                ('pais', models.CharField(max_length=100)),
                ('continente', models.CharField(max_length=50)),
                ('idioma', models.CharField(max_length=100)),
                ('moneda', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'Destinos',
            },
        ),
    ]
