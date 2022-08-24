from django.db import models
from patient.models import Patient
from product.models import *
from order.models import *


# Create your models here.


class Item(models.Model):
    status_choices = [
        ('C','Cart'),
        ('O','Ordered')
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    status  = models.CharField(max_length=2, choices=status_choices, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)
    # order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.patient.first_name + " " + self.patient.email

    