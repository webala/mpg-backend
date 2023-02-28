from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Car)
admin.site.register(Part)
admin.site.register(Client)
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(UserVehicle)