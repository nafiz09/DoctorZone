# Generated by Django 4.1 on 2022-08-26 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pharmacy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manager_name', models.CharField(max_length=20)),
                ('shop_name', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=30, unique=True)),
                ('mobile_no', models.CharField(max_length=12)),
                ('address', models.CharField(max_length=50)),
                ('password', models.CharField(default='', max_length=20)),
            ],
        ),
    ]
