from typing import OrderedDict
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
from ..users.views import *

class DashboardViewSet(viewsets.ModelViewSet):
    serializer_class = CardsSerializers
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Cards.objects.all()

    @action(detail=False, methods=['post'], name="homepage", url_path='home')
    def homepage(self, request):
        try:
            # print ("request : ", request.user)
            user_info = get_user_details_for_username(str(request.user))
            user_id = int(user_info.get("user_id", 0)) 
            user_card_details = []
            user_card_dict = OrderedDict()
            all_cards = Cards.objects.filter(is_deleted=False, public_visibility=True).values()
            for ob in all_cards:
                if user_id != (ob.get("user_id", 0)):
                    ob.update({"extra_params": eval(ob.get("extra_params", "{}"))})
                    user_full_name = get_user_details_for_user_id(ob.get("user_id", "")).get("full_name", "")
                    if user_full_name not in user_card_dict.keys():
                        tmp_cards = []
                        tmp_cards.append(ob)
                        user_card_dict.update({
                            user_full_name: {
                                "cards": tmp_cards,
                                "user": user_full_name,
                            }
                        })
                    else:
                        tmp_obj = user_card_dict.get(user_full_name, {})
                        tmp_cards = tmp_obj.get("cards", [])
                        tmp_cards.append(ob)
            
            for k,v in user_card_dict.items(): user_card_details.append(v)
            new_obj = {"username": user_info.get("full_name", str(request.user)), "userCardDetailsList": user_card_details}
            return Response(new_obj, status=status.HTTP_200_OK)
        except Exception as err:
            print ("Exception in hompage function! : %s - %s" % (err, type(err)))
            pass

    @action(detail=False, methods=['get'], name="my_collection", url_path='my-collection')
    def get_my_collection(self, request):
        try:
            print ("request : ", request.user)
            user_info = get_user_details_for_username(str(request.user))
            user_id = int(user_info.get("user_id", 0)) 
            my_card_collections = []
            user_card_dict = OrderedDict()
            all_cards = Cards.objects.filter(is_deleted=False).values()
            for ob in all_cards:
                if user_id == (ob.get("user_id", 0)):
                    ob.update({"extra_params": eval(ob.get("extra_params", "{}"))})
                    user_full_name = get_user_details_for_user_id(ob.get("user_id", "")).get("full_name", "")
                    if user_full_name not in user_card_dict.keys():
                        tmp_cards = []
                        tmp_cards.append(ob)
                        user_card_dict.update({
                            user_full_name: {
                                "cards": tmp_cards,
                                "user": user_full_name,
                            }
                        })
                    else:
                        tmp_obj = user_card_dict.get(user_full_name, {})
                        tmp_cards = tmp_obj.get("cards", [])
                        tmp_cards.append(ob)
            
            for k,v in user_card_dict.items(): my_card_collections.append(v)
            new_obj = {"username": user_info.get("full_name", str(request.user)), "myCardCollection": my_card_collections}
            return Response(new_obj, status=status.HTTP_200_OK)
        except Exception as err:
            print ("Exception in hompage function! : %s - %s" % (err, type(err)))
            pass

    @action(detail=False, methods=['post'], name="add_card", url_path='add-card')
    def save_card(self, request):
        try:
            data_obj = request.data
            acc_obj = Accounts.objects.filter(name=str(request.user))
            if acc_obj and acc_obj!= -1: acc_obj = acc_obj[0]
            card_obj = Cards()
            card_obj.user = acc_obj
            card_obj.name = data_obj.get("cardInfo", {}).get("card_name", "")
            card_obj.description = data_obj.get("cardInfo", {}).get("card_descr", "")
            card_obj.description = data_obj.get("cardInfo", {}).get("card_descr", "")
            card_obj.card_image = data_obj.get("selectedCard", {}).get("default_img", "")
            card_obj.public_visibility = data_obj.get("cardPublicVisibility", True)
            card_obj.extra_params = str(data_obj.get("selectedCard", {}))
            card_obj.last_update_time = int(time.time())
            card_obj.creation_time = int(time.time())
            try:
                card_obj.save()
            except Exception as err:
                print ("Exceprtion 501 : %s - %s " % (err, type(err)))
                return Response({"status": "failed"}, status=status.HTTP_501_NOT_IMPLEMENTED)
            return Response({"status": "success"}, status=status.HTTP_200_OK)
        except Exception as err:
            print ("Exceprtion 500 : %s - %s " % (err, type(err)))
            return Response({"status": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

