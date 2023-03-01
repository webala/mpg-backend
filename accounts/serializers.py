from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import Group
#Used to access and refresh tokens


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        #Add custom claims
        
        token['username'] = user.username
        token['email'] = user.email
        token['groups'] = [group.name for group in list(user.groups.all())]
        token['id'] = user.id

        return token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class NewUserSerializer(serializers.ModelSerializer):
   email = serializers.EmailField(
      required=True,
      validators = [UniqueValidator(queryset=User.objects.all())]
      )

   password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
   password2 = serializers.CharField(write_only=True, required=True)
  


   class Meta:
      model = User
      fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name')
      extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
      }

   def validate(self, attrs):
      if attrs['password1'] != attrs['password2']:
         raise serializers.ValidationError({'password', 'Password fields do not match'})
      
      return attrs

    
   def create(self, validated_data):
      user = User.objects.create(
         username = validated_data['username'],
         email = validated_data['email'],
         first_name = validated_data['first_name'],
         last_name = validated_data['last_name'],
      )
      
      customer_group = Group.objects.get(name='customer')
      user.groups.add(customer_group)
      user.set_password(validated_data['password1'])
      user.save()
      return user