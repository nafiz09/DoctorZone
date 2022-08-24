from django.db import models
from pharmacy.models import *
from patient.models import *

# Create your models here.

class Order(models.Model):
    status_choices = [
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('D', 'Found deliveryman'),
        ('F', 'Picked up'),
        ('C', 'Completed'),
    ]
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    status  = models.CharField(max_length=2, choices=status_choices, default='P')
    delivery_address = models.CharField(max_length=50, null=True,default=Patient.address)
    total_amount = models.IntegerField(null=True)
