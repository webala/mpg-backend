import os, secrets, pyrebase, json,requests, base64
from datetime import datetime
from requests.auth import HTTPBasicAuth
from django.conf import settings
from dotenv import load_dotenv
load_dotenv()

firebaseConfig = {
"apiKey": "AIzaSyCRVdQPzXSfQNwm84rtf0fyp29QYHtbDMk",
"authDomain": "mpg-auto.firebaseapp.com",
'projectId': "mpg-auto",
'storageBucket': "mpg-auto.appspot.com",
'messagingSenderId': "369805553352",
'appId': "1:369805553352:web:46bbf59c1d5294a8c0fffd",
'measurementId': "G-6L6Z873EJY",
"databaseURL": "",
}




firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()
auth = firebase.auth()
email = os.getenv('FIREBASE_EMAIL')
password = os.getenv('FIREBASE_PASSWORD')

def upload_image(file):
    random_hex = secrets.token_hex(8)
    print('file', file)
    _, f_ext = os.path.splitext(file.name)
    filename = random_hex + f_ext
    directory = f'parts/{filename}'
    user = auth.sign_in_with_email_and_password(email, password)
    storage.chile(directory).put(file, user['idToken'])
    image_url = get_image_url(filename, user)
    return {'filename': filename, 'image_url': image_url}

def get_image_url(filename, user):
    path = f'parts/{filename}'
    url = storage.child(path).get_url(user["idToken"])
    return url


# Function to generate daraja access token
def get_access_token():
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    response = requests.get(
        settings.DARAJA_AUTH_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret)
    )

    json_res = response.json()
    access_token = json_res["access_token"]
    return access_token


# function to format date time
def format_date_time():
    current_time = datetime.now()
    formated_time = current_time.strftime("%Y%m%d%H%M%S")
    return formated_time


# function to generate password string
def generate_password(dates):
    data_to_encode = (
        str(settings.BUSINESS_SHORT_CODE) + settings.LIPANAMPESA_PASSKEY + dates
    )
    encoded_string = base64.b64encode(data_to_encode.encode())
    decoded_passkey = encoded_string.decode("utf-8")

    return decoded_passkey


# function to initiate stk push for mpesa payment
def initiate_stk_push(phone, amount=1):
    access_token = get_access_token()
    formated_time = format_date_time()
    password = generate_password(formated_time)

    headers = {"Authorization": "Bearer %s" % access_token}

    payload = {
        "BusinessShortCode": settings.BUSINESS_SHORT_CODE,
        "Password": password,
        "Timestamp": formated_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": "174379",
        "PhoneNumber": phone,
        "CallBackURL": "https://b564-41-80-113-61.eu.ngrok.io/api/transaction/mpesa/callback/",
        "AccountReference": "MPG AUTO STORE",
        "TransactionDesc": "Make Payment",
    }

    response = requests.post(settings.API_RESOURCE_URL, headers=headers, json=payload)

    string_response = response.text
    string_object = json.loads(string_response)

    if "errorCode" in string_object:
       return string_object
    else:
        data = {
            "merchant_request_id": string_object["MerchantRequestID"],
            "chechout_request_id": string_object["CheckoutRequestID"],
            "response_code": string_object["ResponseCode"],
            "response_description": string_object["ResponseDescription"],
            "customer_message": string_object["CustomerMessage"],
        }
    return data




#Authentiacate pesapal
def get_pesapal_access_token():
    consumer_key = os.getenv("PESAPAL_CONSUMER_KEY")
    consumer_secret = os.getenv("PESAPAL_CONSUMER_SECRET")

    data = {
        "consumer_key": consumer_key,
        "consumer_secret": consumer_secret
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.post(
        settings.PESAPAL_AUTH_URL, json=data, headers=headers
    )

    json_res = response.json()
    token = json_res['token']
    return token


def register_ipn_url(callback_url, token):

    headers = {
        "Authorization": "Bearer {}".format(token),
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    data = {
        "url": callback_url,
        "ipn_notification_type": "POST"
    }

    response = requests.post(
        settings.PESAPAL_IPN_REGISTRATION_URL, headers=headers, json=data
    )

    response = response.json()
    return response

def get_registered_ipns(token):
   
    headers = {
        "Authorization": "Bearer {}".format(token),
    }

    response = requests.get(
        settings.REGISTERED_IPNS_URL, headers=headers
    )

    ipns = response.json()

    if not ipns:
        ipn = register_ipn_url("https://7be2-41-80-113-56.eu.ngrok.io/api/transaction/pesapal/ipn/", token)
    else:
        ipn = ipns[0]
    
    return ipn

def initiate_pesapal_transaction():
    token = get_pesapal_access_token()
    ipn_data = get_registered_ipns(token)
    print('ipn data: ', ipn_data)
    notification_id = ipn_data["ipn_id"]

    headers = {
        "Authorization": "Bearer {}".format(token),
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    unique_id = secrets.token_hex(8)
    
    data = {
        "id": unique_id,
	    "currency": "KES",
        "amount": 100.00,
        "description": "Payment description goes here",
        "callback_url": "https://7be2-41-80-113-56.eu.ngrok.io/api/transaction/pesapal/callback/",
        "notification_id": notification_id,
        "billing_address": {
            "email_address": "john.doe@example.com",
            "phone_number": "0723xxxxxx",
	        "country_code": "KE",
	    }
    }

    response = requests.post(
        settings.PESAPAL_ORDER_REQUEST_URL, headers=headers, json=data
    )

    print('order request res: ', response)

    json_res = response.json()
    return json_res