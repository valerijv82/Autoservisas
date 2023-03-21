# Generated by Django 4.1.7 on 2023-03-07 17:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valstybinis_nr', models.CharField(max_length=12, verbose_name='Valstybinis numeris')),
                ('vin_code', models.CharField(max_length=20, verbose_name='VIN')),
                ('customer', models.CharField(max_length=100, verbose_name='Klientas')),
            ],
            options={
                'db_table': 'car',
                'ordering': ['customer', 'vin_code', 'customer'],
            },
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marke', models.CharField(max_length=100, verbose_name='Marke')),
                ('model', models.CharField(max_length=100, verbose_name='Modelis')),
            ],
            options={
                'db_table': 'car_model',
                'ordering': ['marke', 'model'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(max_length=10, verbose_name='Data')),
                ('suma', models.CharField(max_length=10, verbose_name='Suma')),
                ('car_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='car_service_app.car')),
            ],
            options={
                'db_table': 'order',
                'ordering': ['data', 'suma'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Paslaugos pavadinimas')),
                ('price', models.CharField(max_length=10, verbose_name='Paslaugos kaina')),
            ],
            options={
                'db_table': 'service',
                'ordering': ['name', 'price'],
            },
        ),
        migrations.CreateModel(
            name='OrderLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.CharField(max_length=10, verbose_name='Kiekis')),
                ('price', models.CharField(max_length=10, verbose_name='Kaina')),
                ('order_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='car_service_app.order')),
                ('service_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='car_service_app.service')),
            ],
            options={
                'db_table': 'order_line',
                'ordering': ['quantity', 'price'],
            },
        ),
        migrations.AddField(
            model_name='car',
            name='car_model_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='car_service_app.carmodel'),
        ),
    ]