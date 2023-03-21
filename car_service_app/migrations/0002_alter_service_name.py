# Generated by Django 4.1.7 on 2023-03-07 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_service_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.CharField(blank=True, choices=[('p', 'patikra'), ('a', 'alyva'), ('s', 'sankaba')], default='p', max_length=5, verbose_name='Paslaugos pavadinimas'),
        ),
    ]