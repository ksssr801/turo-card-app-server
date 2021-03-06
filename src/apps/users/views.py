from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from .serializers import AccountsSerializers, RegisterSerializer, UserSerializer
from django.contrib.auth.models import User
from .models import Accounts
from django.contrib.auth.hashers import make_password
import time

class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args,  **kwargs):
        try:
            print ("request.data : ", request.data)
            user_data = {}
            data_obj = request.data
            username = request.data.get("email", "")
            password = request.data.get("password", "")
            if password: request.data.update({"password": make_password(password)})
            serializer = self.get_serializer(data=request.data)
            try: serializer.is_valid(raise_exception=True)
            except:
                if username and password: return Response({"message": "Username already exists!"}, status=status.HTTP_208_ALREADY_REPORTED)
                elif username and not password: return Response({"password": "This field is required!"}, status=status.HTTP_400_BAD_REQUEST)
                elif password and not username: return Response({"username": "This field is required!"}, status=status.HTTP_400_BAD_REQUEST)
                else: return Response({"username": "This field is required!", "password": "This field is required!"}, status=status.HTTP_400_BAD_REQUEST)
            full_name = data_obj.get("first_name", '') + " " + data_obj.get("last_name", '')
            acc_info = Accounts()
            acc_info.name = data_obj.get("username", '')
            acc_info.first_name = data_obj.get("first_name", '')
            acc_info.last_name = data_obj.get("last_name", '')
            acc_info.full_name = full_name
            acc_info.email = data_obj.get("email", '')
            acc_info.password = data_obj.get("password", '')
            acc_info.creation_time = int(time.time())
            acc_info.last_update_time = int(time.time())
            try:
                acc_info.save()
                user = serializer.save()
            except Exception as err:
                print ("Coming Here : %s" % err)
                return Response(user_data, status=status.HTTP_501_NOT_IMPLEMENTED)
            user_data = UserSerializer(user, context=self.get_serializer_context()).data
            return Response(user_data, status=status.HTTP_200_OK)
        except:
            return Response(user_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_user_details_for_username(username):
    user_data = Accounts.objects.filter(name=username, is_deleted=False).values()
    if user_data and user_data != -1: user_data = user_data[0]
    return user_data

def get_user_details_for_user_id(user_id):
    user_data = Accounts.objects.filter(user_id=user_id, is_deleted=False).values()
    if user_data and user_data != -1: user_data = user_data[0]
    return user_data
