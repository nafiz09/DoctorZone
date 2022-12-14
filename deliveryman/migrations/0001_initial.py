# Generated by Django 4.1 on 2022-08-25 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deliveryman',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(blank=True, max_length=20)),
                ('birthday', models.DateField(null=True)),
                ('email', models.CharField(max_length=30, unique=True)),
                ('mobile_no', models.CharField(max_length=12)),
                ('address', models.CharField(max_length=50)),
                ('password', models.CharField(default='', max_length=20)),
            ],
        ),
    ]
