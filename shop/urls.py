from django.urls import path
from .views import *
 
urlpatterns = [
    path('cars/', Cars.as_view(), name='cars'),
    path('parts/', Parts.as_view(), name='parts'),
    path('part/<int:pk>', PartDetail.as_view(), name='part'),
    path('part/imageupload', upload_part_image, name='part-image-upload'),
    path('parts/<str:category>', parts_by_category, name='parts-by-category'),
    path('orders/', OrdersView.as_view(), name='orders'),
    path('order/<pk>', OrderDetail.as_view(), name='order'),
    path('payment/mpesa', ProcessMpesaPayment.as_view(), name='mpesa-payment'),
    path('transaction/mpesa/<pk>', MpesaTransactionDetail.as_view(), name='mpesa-payment'),
    path('transaction/mpesa/callback', MpesaCallback.as_view(), name='mpesa-callback'),
    path('payment/pesapal', ProcessPesapalPayment.as_view(), name='pesapal-payment'),
    path('transaction/pesapal/ipn', pesapal_ipn, name='pesapal-ipn'),
    path('transaction/pesapal/callback', pesapal_callback, name='pesapal-callback'),
    path('user/vehicles/add', add_user_vehicle, name='add-user-vehicle'),
    path('user/vehicles/<str:username>', user_vehicles_list, name='user-vehicles-list')
]