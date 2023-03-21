# Generated by Django 4.1.7 on 2023-03-09 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_service_app', '0002_alter_service_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='car',
            options={'ordering': ['customer', 'vin_code', 'customer'], 'verbose_name': 'Car object', 'verbose_name_plural': 'car object'},
        ),
        migrations.AlterModelOptions(
            name='carmodel',
            options={'ordering': ['marke', 'model'], 'verbose_name': 'Car model', 'verbose_name_plural': 'car model'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['data', 'suma'], 'verbose_name': 'Order', 'verbose_name_plural': 'order'},
        ),
        migrations.AlterModelOptions(
            name='orderline',
            options={'ordering': ['quantity', 'price'], 'verbose_name': 'Order line', 'verbose_name_plural': 'order line'},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'ordering': ['name', 'price'], 'verbose_name': 'Service', 'verbose_name_plural': 'service'},
        ),
        migrations.AddField(
            model_name='order',
            name='servis',
            field=models.CharField(blank=True, choices=[('p', 'Patvirtintas'), ('v', 'Vykdoma'), ('a', 'Atlikta'), ('t', 'Atsaukta')], default='p', max_length=5, verbose_name='Serviso pavadinimas'),
        ),
    ]
