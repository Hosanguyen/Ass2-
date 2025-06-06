# Generated by Django 5.0.12 on 2025-03-03 02:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'address',
            },
        ),
        migrations.CreateModel(
            name='FullName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'fullname',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=15)),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('customer_type', models.CharField(choices=[('admin', 'Admin'), ('vendor', 'Vendor'), ('registered', 'Registered Customer'), ('guest', 'Guest')], default='registered', max_length=20)),
                ('address', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.address')),
                ('fullname', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.fullname')),
            ],
            options={
                'db_table': 'customer',
            },
        ),
    ]
