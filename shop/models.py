from django.db import models

# Create your models here.


class Car(models.Model):
    make = models.CharField(max_length=20)
    series = models.CharField(max_length=20, null=True, blank=True)
    model = models.CharField(max_length=20)
    year = models.CharField(max_length=10)
    body_type = models.CharField(max_length=20)
    engine = models.CharField(max_length=20)


class Part(models.Model):
    part_no = models.CharField(max_length=20)
    cars = models.ManyToManyField(Car, blank=True)