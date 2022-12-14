from django.db import models
from patient.models import Patient
from pharmacy.models import Pharmacy
from deliveryman.models import Deliveryman

# Create your models here.


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Got_deliveryman', 'Got_deliveryman'),
        ('Picked', 'Picked'),
        ('Delivered', 'Delivered')
    ]
    customer = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    address = models.CharField(max_length=50)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    deliveryman = models.ForeignKey(Deliveryman, on_delete=models.CASCADE, null=True)
