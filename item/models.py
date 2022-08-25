from django.db import models
from patient.models import Patient
from product.models import Product
from order.models import Order

# Create your models here.

class Item(models.Model):
    STATUS_CHOICES = [
        ('Cart', 'Cart'),
        ('Order', 'Order'),
    ]
    customer = models.ForeignKey(Patient, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Cart')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    total = models.IntegerField(null=True)