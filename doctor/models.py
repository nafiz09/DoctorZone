from django.db import models

# Create your models here.
from django.db import models
from patient.models import *

# Create your models here.


class Doctor(models.Model):

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('T', 'Non-Binary')
    ]

    VERIFICATION_CHOICES = [
        ('verified', 'verified'),
        ('pending', 'pending'),
        ('rejected', 'rejected')
    ]

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    birthday = models.DateField(null=True)
    email = models.CharField(max_length=30, unique=True)
    mobile_no = models.CharField(max_length=14)
    address = models.CharField(max_length=50, blank=True)
    password = models.CharField(max_length=20)
    license_no = models.CharField(max_length=10)
    specialist = models.CharField(max_length=20)
    verified = models.CharField(max_length=10, choices=VERIFICATION_CHOICES)
    prescriptionFields = models.CharField(max_length=250, default='NAME#AGE#SEX')

    def __str__(self):
        return self.first_name + " " + self.email


class DegreeOfDoctor(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    degree_name = models.CharField(max_length=20)
    institute = models.CharField(max_length=30)
    degree_date = models.DateField(null=True)


class Chamber(models.Model):
    WEEKDAY_CHOICES = [
        ('sat', 'SATURDAY'),
        ('sun', 'SUNDAY'),
        ('mon', 'MONDAY'),
        ('tues', 'TUESDAY'),
        ('wed', 'WEDNESDAY'),
        ('thrs', 'TRURSDAY'),
        ('fri', 'FRIDAY')
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    sat_starttime = models.TimeField(null=True)
    sat_endtime = models.TimeField(null=True)
    sun_starttime = models.TimeField(null=True)
    sun_endtime = models.TimeField(null=True)
    mon_starttime = models.TimeField(null=True)
    mon_endtime = models.TimeField(null=True)
    tues_starttime = models.TimeField(null=True)
    tues_endtime = models.TimeField(null=True)
    wed_starttime = models.TimeField(null=True)
    wed_endtime = models.TimeField(null=True)
    thrs_starttime = models.TimeField(null=True)
    thrs_endtime = models.TimeField(null=True)
    fri_starttime = models.TimeField(null=True)
    fri_endtime = models.TimeField(null=True)
    address = models.CharField(max_length=100)
    payment = models.IntegerField()
    max_capacity = models.IntegerField(default=3)

    def __str__(self):
        return self.address


class Appointment(models.Model):
    STATE_CHOICES = [
        ('Requested', 'requested'),
        ('Ongoing', 'ongoing'),
        ('Completed', 'completed')
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    chamber = models.ForeignKey(Chamber, on_delete=models.CASCADE)
    date = models.DateField()
    state = models.CharField(max_length=10, default='R', choices=STATE_CHOICES)
#
# class PrescriptionType(models.Model):
# #     there will be a apoointment id attached to it.
#     doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
#     fields = models.CharField(max_length=200, default="patient_name#age#sex#bloodGroup")

