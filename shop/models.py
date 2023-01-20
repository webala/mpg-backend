from django.db import models

# Create your models here.


class Car(models.Model):
    make = models.CharField(max_length=20)
    series = models.CharField(max_length=20, null=True, blank=True)
    model = models.CharField(max_length=20, null=True, blank=True)
    year = models.CharField(max_length=10)
    body_type = models.CharField(max_length=20)
    engine = models.CharField(max_length=20)


class Part(models.Model):

    categories =[
        ('BRAKES', 'BRAKES'),
        ('WINDOW', 'WINDOW'),
        ('GEARBOX', 'GEARBOX'),
        ('DOOR', 'DOOR'), 
        ('OTHER', 'OTHER')
    ]

    name = models.CharField(max_length=100)
    part_no = models.CharField(max_length=20)
    cars = models.ManyToManyField(Car, blank=True)
    category = models.CharField(max_length=20, choices=categories, default='OTHER')
    image_url = models.CharField(max_length=200, null=True, blank=True)
    image_filename = models.CharField(max_length=20, null=True, blank=True)
    inventory = models.IntegerField()