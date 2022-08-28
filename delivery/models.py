from django.db import models

# Create your models here.


class Delivery(models.Model):
    email = models.CharField(max_length=30, unique=True)
    mobile_no = models.CharField(max_length=12)
    address = models.CharField(max_length=50)
    password = models.CharField(max_length=20, default="")


    def __str__(self):
        return self.shop_name