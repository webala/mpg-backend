from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework import generics
from .models import Car, Part, Client, ShippingAddress, Order, OrderItem, MpesaTransaction, PesapalTransaction, UserVehicle
from .serializers import CarSerializer, PartsSerializer, OrderSerializer, OrderDetailSerializer, MpesaPaymentSerializer, MpesaTransactionSerializer, PesapalPaymentSerializer, UserVehicleSerializer
from .utils import initiate_stk_push, initiate_pesapal_transaction
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
import json

class Cars(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class Parts(generics.ListCreateAPIView):
    queryset = Part.objects.all()
    serializer_class = PartsSerializer


class PartDetail(generics.RetrieveAPIView):
    model = Part
    serializer_class = PartsSerializer
    queryset = Part.objects.all()

class OrderDetail(generics.RetrieveAPIView):
    model = Order
    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()
    context_object_name = 'order'

    def get_serializer_context(self, **kwargs):
        context = super(OrderDetail, self).get_serializer_context(**kwargs)
        print('context: ', context)
        order = super().get_object()
        print('order: ', order)
        order_items = order.orderitem_set.all()
        print('order items: ', order_items)
        context.update({'order_items': order_items})
        return context

class OrdersView(APIView):
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            
            shipping_address_data = data.get('shipping_address')
            client_data = shipping_address_data.get('client')
            order_items_data = data.get('order_items')

            client = Client.objects.create(
                first_name=client_data.get('first_name'),
                last_name=client_data.get('last_name'),
                phone_number=client_data.get('phone_number'),
                email=client_data.get('email')
            )

            shipping_address = ShippingAddress.objects.create(
                location=shipping_address_data.get('location'),
                building=shipping_address_data.get('building'),
                house_number=shipping_address_data.get('house_number'),
                description=shipping_address_data.get('description'),
                client=client
            )

            order = Order.objects.create(shipping_address=shipping_address)
            for item in order_items_data:
                part_id = item.get('part_id')
                quantity = item.get('quantity')
                part = Part.objects.get(id=part_id)
                OrderItem.objects.create(
                    part=part,
                    order=order,
                    quantity=quantity
                )

            return Response({"message": "success", "order_id": order.id}, status=201)

@api_view(['GET'])
def parts_by_category(request, category):
    queryset = Part.objects.filter(category=category)
    serializer = PartsSerializer(queryset, many=True)
    return Response(serializer.data, status=200)


class ProcessMpesaPayment(APIView):
    def post(self, request):
        serializer = MpesaPaymentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number = serializer.validated_data.get('phone_number')
            order_id = serializer.validated_data.get('order_id')
            order = Order.objects.get(id=order_id)
            amount = order.cart_total
            transaction_data = initiate_stk_push(phone_number)
            if "errorCode" in transaction_data:
                return Response({
                    "errorCode": transaction_data['errorCode'],
                    "errorMesssage": transaction_data['errorMessage']
                }, status=405)
            else:
                transaction = MpesaTransaction.objects.create(
                    request_id=transaction_data['chechout_request_id'],
                    order=order
                )

                return Response({'message': 'success', 'transaction_id': transaction.id}, status=201)

class MpesaCallback(APIView):
    def post(self, request):
        request_data = json.loads(request.body)
        body = request_data.get("Body")
        result_code = body.get("stkCallback").get("ResultCode")

        if result_code == 0:
            print("Payment successful")
            request_id = body.get("stkCallback").get("CheckoutRequestID")
            metadata = body.get("stkCallback").get("CallbackMetadata").get("Item")

            for data in metadata:
                if data.get("Name") == "MpesaReceiptNumber":
                    receipt_number = data.get("Value")
                elif data.get("Name") == "Amount":
                    amount = data.get("Value")
                elif data.get("Name") == "PhoneNumber":
                    phone_number = data.get("Value")
            print("receipt:", receipt_number)
            print("amouont: ", amount)
            print("request_id: ", request_id)
            transaction = MpesaTransaction.objects.get(request_id=request_id)
            transaction.receipt_number = receipt_number
            transaction.amount = amount
            transaction.phone_number = str(phone_number)
            transaction.is_complete = True
            transaction.save()
            return HttpResponse("Ok")

class MpesaTransactionDetail(generics.RetrieveAPIView):
    model = MpesaTransaction
    serializer_class = MpesaTransactionSerializer
    queryset = MpesaTransaction.objects.all()


class ProcessPesapalPayment(APIView):
    def post(self, request):
        serializer = PesapalPaymentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            response = initiate_pesapal_transaction()
            order_id = serializer.validated_data.get('order_id')
            order = Order.objects.get(id=order_id)
            order_tracking_id = response.get('order_tracking_id')
            transaction = PesapalTransaction.objects.create(
                order=order,
                order_tracking_id=order_tracking_id
            )
            print('pesapal response: ', response)
            return Response(response, status=200)

def pesapal_ipn(request):
    data = json.loads(request.body)
    print('ipn url called', data)


def pesapal_callback(request):
    data = json.loads(request.body)
    print('callback called: ', data)

@api_view(['POST'])
def add_user_vehicle(request):
    serializer = UserVehicleSerializer(data = request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        username = data.get('username')
        car_id = data.get('car_id')

        user = User.objects.get(username=username)
        car = Car.objects.get(id=car_id)

        user_vehicles_queryset = UserVehicle.objects.filter(user=user)
        if user_vehicles_queryset.exists():
            user_vehicles = user_vehicles_queryset.first()
            user_vehicles.cars.add(car)
            user_vehicles.save()      
        else:
            user_vehicles = UserVehicle.objects.create(user=user)
            user_vehicles.cars.add(car)
            user_vehicles.save()
        
        return Response({'message': 'Vehicle added for user {}'.format(user.username)}, status=200)