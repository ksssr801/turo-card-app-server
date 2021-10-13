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
                card_likes = len(eval(ob.get('likes', '[]')))
                ob.update({'likes_count': card_likes})
                liked_by_current_user = [x for x in eval(ob.get('likes', '[]')) if x == user_id]
                if len(liked_by_current_user): ob.update({'isLiked': True})
                else: ob.update({'isLiked': False})
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

    @action(detail=False, methods=['post'], name="like_card", url_path='like-card')
    def like_the_card(self, request):
        try:
            data_obj = request.data
            card_id = int(data_obj.get('cardId', 0))
            acc_obj = Accounts.objects.filter(name=str(request.user)).values()
            if acc_obj and acc_obj!= -1: acc_obj = acc_obj[0]
            card_obj = Cards.objects.get(card_id=card_id)
            user_id = int(acc_obj.get("user_id", 0))
            likes_obj = eval(card_obj.likes)
            if user_id not in likes_obj: likes_obj.append(user_id)
            card_obj.likes = likes_obj            
            try:
                card_obj.save()
            except Exception as err:
                print ("Exceprtion 501 : %s - %s " % (err, type(err)))
                return Response({"status": "failed"}, status=status.HTTP_501_NOT_IMPLEMENTED)
            return Response({"status": "success"}, status=status.HTTP_200_OK)
        except Exception as err:
            print ("Exceprtion 500 : %s - %s " % (err, type(err)))
            return Response({"status": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'], name="dislike_card", url_path='dislike-card')
    def dislike_the_card(self, request):
        try:
            data_obj = request.data
            card_id = int(data_obj.get('cardId', 0))
            acc_obj = Accounts.objects.filter(name=str(request.user)).values()
            if acc_obj and acc_obj!= -1: acc_obj = acc_obj[0]
            card_obj = Cards.objects.get(card_id=card_id)
            user_id = int(acc_obj.get("user_id", 0))
            likes_obj = eval(card_obj.likes)
            if user_id in likes_obj: likes_obj.remove(user_id)
            card_obj.likes = likes_obj            
            try:
                card_obj.save()
            except Exception as err:
                print ("Exceprtion 501 : %s - %s " % (err, type(err)))
                return Response({"status": "failed"}, status=status.HTTP_501_NOT_IMPLEMENTED)
            return Response({"status": "success"}, status=status.HTTP_200_OK)
        except Exception as err:
            print ("Exceprtion 500 : %s - %s " % (err, type(err)))
            return Response({"status": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'], name="comment_on_card", url_path='comment-on-card')
    def comment_on_card(self, request):
        try:
            data_obj = request.data
            user_info = get_user_details_for_username(str(request.user))
            card_id = int(data_obj.get('cardId', 0))
            comment = str(data_obj.get('comment', ''))
            acc_obj = Accounts.objects.filter(name=str(request.user)).values()
            if acc_obj and acc_obj!= -1: acc_obj = acc_obj[0]
            card_obj = Cards.objects.get(card_id=card_id)
            user_id = int(acc_obj.get("user_id", 0))
            comments_obj = eval(card_obj.comments)
            user_comment_obj = {
                'comment': comment,
                'user': user_info.get('full_name', ''),
                'time': int(time.time()),
                'card_id': card_id
            }
            # print ("data : ", user_id, comments_obj)
            if user_id in comments_obj.keys():
                user_comment_list = comments_obj.get(user_id, [])
                print ("user_comment_list :", user_comment_list)
                user_comment_list.append(user_comment_obj)
                comments_obj.update({user_id: user_comment_list})
            else:
                user_comment_list = []
                user_comment_list.append(user_comment_obj)
                comments_obj.update({user_id: user_comment_list})
            card_obj.comments = comments_obj
            try: card_obj.save()
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

