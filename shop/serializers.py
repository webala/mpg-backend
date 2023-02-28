from rest_framework import serializers
from .models import Car, Part, Client, ShippingAddress,OrderItem, Order, MpesaTransaction
from .utils import upload_image

class CarSerializer (serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'make', 'series', 'model', 'year', 'body_type', 'engine']


class CreatePartSerializer(serializers.Serializer):
    cars = CarSerializer(many=True)
    image = serializers.ImageField()
    part_no = serializers.CharField()
    category = serializers.CharField()

class PartsSerializer(serializers.ModelSerializer):
    cars = CarSerializer(many=True)

    class Meta:
        model = Part
        fields = ['id', 'name', 'part_no', 'cars', 'category', 'image_url', 'image_filename', 'inventory', 'price', 'description', 'brand']


    def create(self, validated_data):
        part = Part.objects.create(
            part_no=validated_data.get('part_no'), 
            category=validated_data.get('category'), 
            inventory=validated_data.get('inventory'),
            price=validated_data.get('price'),
            description=validated_data.get('description'),
            brand=validated_data.get('brand')
        )
        cars = validated_data.get('cars')
     
        for value in cars:
            car = Car.objects.get(
                make = value.get('make'),
                series = value.get('series'),
                model = value.get('model'),
                year = value.get('year'),
                body_type = value.get('body_type'),
                engine = value.get('engine')
            )
            part.cars.add(car)
        
        return part

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class ShippingAddressSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    class Meta:
        model = ShippingAddress
        fields = ['location', 'building', 'house_number', 'description', 'client']



class CreateOrderItemSerializer(serializers.Serializer):
    part_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['part', 'quantity']

class OrderSerializer(serializers.Serializer):
    order_items = CreateOrderItemSerializer(many=True)
    shipping_address = ShippingAddressSerializer()


class OrderDetailSerializer(serializers.ModelSerializer):
    shipping_address = ShippingAddressSerializer()
    # order_items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'shipping_address', 'is_complete', 'date_created']

class MpesaPaymentSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    order_id = serializers.IntegerField()

class PesapalPaymentSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()

class MpesaTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaTransaction
        fields = '__all__'


class UserVehicleSerializer(serializers.Serializer):
    username = serializers.CharField()
    car_id = serializers.IntegerField()