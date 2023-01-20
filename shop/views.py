from django.shortcuts import render
from rest_framework import generics
from .models import Car, Part
from .serializers import CarSerializer, PartsSerializer, CreatePartSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response

from .utils import upload_image
# Create your views here.

class Cars(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class Parts(generics.ListCreateAPIView):
    queryset = Part.objects.all()
    serializer_class = PartsSerializer


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def create_part(request):
    print('request: ', request)
    serializer = CreatePartSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        part = Part.objects.create(part_no=data.get('part_no'), category=data.get('category'))
        cars = data.get('cars')
        image = data.get('image')
        image_data = upload_image(image)
        part.image_url = image_data['image_url']
        part.image_filename = image_data['filename']


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
        part.save()
        serializer = PartsSerializer(part)
        return Response(serializer.data)


@api_view(['GET'])
def parts_by_category(request, category):
    queryset = Part.objects.filter(category=category)
    # if queryset.exists():
    serializer = PartsSerializer(queryset, many=True)
    return Response(serializer.data, status=200)
    # return Response({'massage': 'category does not exist'}, status=404)