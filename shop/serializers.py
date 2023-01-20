from rest_framework import serializers
from .models import Car, Part
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
        fields = ['part_no', 'cars', 'category', 'image_url', 'image_filename', 'inventory']


    def create(self, validated_data):
        part = Part.objects.create(part_no=validated_data.get('part_no'), category=validated_data.get('category'), inventory=validated_data.get('inventory'))
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