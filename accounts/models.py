from django.db import models

# Create your models here.

class Account(models.Model):

    USER_CHOICES = [
        ('Doctor', 'Doctor'),
        ('Patient', 'Patient'),
        ('Pharmacy', 'Pharmacy'),
        ('Deliveryman', 'Deliveryman')
    ]

    email = models.CharField(max_length=30, primary_key=True)
    password = models.CharField(max_length=20)
    usertype = models.CharField(max_length=12, choices=USER_CHOICES)

    def __str__(self):
        return self.email
        
