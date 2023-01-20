import os, secrets, pyrebase
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