from statistics import mode
from django.db import models
from pharmacy.models import *
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    description = models.TextField(null=True,max_length=255)
    # shop_id = models.IntegerField(null=True)
    product_image = models.ImageField(upload_to='product_images')
    shop = models.ForeignKey( Pharmacy, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name