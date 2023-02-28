from django.db import models
from django.contrib.auth.models import User
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
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.CharField(max_length=300)
    brand = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Client(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    is_subscribed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name

class ShippingAddress(models.Model):
    location = models.CharField(max_length=30)
    building = models.CharField(max_length=30)
    house_number = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.location + ' ' + self.building

class Order(models.Model): 
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True)
    is_complete = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)

    @property
    def cart_items(self):
        order_items = self.orderitem_set.all()
        return sum([item.quantity for item in order_items])

    # This function return the total price of the order
    @property
    def cart_total(self):
        order_items = self.orderitem_set.all()
        return sum([item.item_total for item in order_items])


class OrderItem(models.Model):
    part = models.ForeignKey(Part, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    @property
    def item_total(self):
        return self.quantity * self.part.price

class MpesaTransaction(models.Model):
    request_id = models.CharField(max_length=30)
    date = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    is_complete = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, null=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    receipt_number = models.CharField(max_length=15, null=True)


class PesapalTransaction(models.Model):
    order_tracking_id = models.CharField(max_length=50)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)


class UserVehicle(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cars = models.ManyToManyField(Car, blank=True)