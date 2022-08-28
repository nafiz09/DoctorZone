from django.db import models

# Create your models here.

class Deliveryman(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, blank=True)
    birthday = models.DateField(null=True)
    email = models.CharField(max_length=30, unique=True)
    mobile_no = models.CharField(max_length=12)
    address = models.CharField(max_length=50)
    password = models.CharField(max_length=20, default="")