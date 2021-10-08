from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import CardSwapRequestInfoSerializers, CardsSerializers
from .models import Cards, CardSwapRequestInfo
from rest_framework.permissions import IsAuthenticated
import time
from ..users.models import Accounts
from ..users.serializers import AccountsSerializers
from django.db.models import Q

class DashboardViewSet(viewsets.ModelViewSet):
    serializer_class = CardsSerializers
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Cards.objects.all()

    @action(detail=False, methods=['post'], name="homepage", url_path='home')
    def homepage(self, request):
        try:
            print ("request : ", request.user)
            data_obj = request.data
            new_obj = {"username": str(request.user)}
            return Response(new_obj, status=status.HTTP_200_OK)
        except:
            print ("Exception in hompage function!")
            pass

    def object_mapper(self):
        try:
            mapped_objs = {}
            user_data = Accounts.objects.filter(is_deleted=False)
            user_data = AccountsSerializers(user_data, many=True).data
            card_data = Cards.objects.filter(is_deleted=False)
            card_data = CardsSerializers(card_data, many=True).data
            user_obj = {emp.get("user_id", None): emp for emp in user_data}
            user_name_obj = {emp.get("name", None): emp for emp in user_data}
            card_obj = {prof.get("id", None): prof for prof in card_data}
            mapped_objs.update({
                "user_obj": user_obj,
                "user_name_obj": user_name_obj,
                "card_obj": card_obj,
            })
            return mapped_objs
        except:
            pass

