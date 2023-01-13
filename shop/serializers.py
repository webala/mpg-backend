from rest_framework import serializers
from .models import Car, Part

class CarSerializer (serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id','make', 'series', 'model', 'year', 'body_type', 'engine']


class PartsSerializer(serializers.ModelSerializer):
    cars = CarSerializer(many=True)
    class Meta:
        model = Part
        fields = ['part_no', 'cars']


    def create(self, validated_data):
        part = Part.objects.create(part_no=validated_data.get('part_no'))
        cars = validated_data.get('cars')

        for value in cars:
            car = Car.objects.create(
                make = value.get('make'),
                series = value.get('series'),
                model = value.get('model'),
                year = value.get('year'),
                body_type = value.get('body_type'),
                engine = value.get('engine')
            )
            print('car: ',car)
            part.cars.add(car)
        
        return part
        # print('cars: ', cars)