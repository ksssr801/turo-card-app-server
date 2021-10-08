from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Accounts
from django.contrib.auth.hashers import make_password

# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','password','first_name', 'last_name')
        extra_kwargs = {
            'password':{'write_only': True},
        }
        def create(self, validated_data):
            # print ("validated_data  :", validated_data)
            # user = User.objects.create_user(username=validated_data['username'], password=make_password(validated_data['password']),first_name=validated_data['first_name'],last_name=validated_data['last_name'])
            return {}

# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class AccountsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = '__all__'

def validate_password(self, value: str) -> str:
    """
    Hash value passed by user.

    :param value: password of a user
    :return: a hashed version of the password
    """
    return make_password(value)