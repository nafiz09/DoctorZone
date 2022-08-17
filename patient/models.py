from django.db import models

# Create your models here.


class Patient(models.Model):
    GENDER_CHOICES =[
        ('M', 'Male'),
        ('F', 'Female'),
        ('T', 'Non-Binary')
    ]

    BLOODGROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-')
    ]

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    birthday = models.DateField(null=True)
    email = models.CharField(max_length=30, unique=True)
    mobile_no = models.CharField(max_length=12)
    address = models.CharField(max_length=50)
    password = models.CharField(max_length=20, default="")

    blood_group = models.CharField(max_length=4, choices=BLOODGROUP_CHOICES, null=True, blank=True)
    height = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.first_name + " " + self.email
