from django.db import models
from django.db.models.deletion import CASCADE
from ..users.models import Accounts

class Cards(models.Model):
    card_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Accounts, db_column='user_id', related_name='user_card_mapping', on_delete=CASCADE)
    name = models.CharField(max_length=254)
    description = models.CharField(max_length=254)
    card_image = models.CharField(max_length=254)
    last_update_time = models.IntegerField(null=True)
    creation_time = models.IntegerField(null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'tbl_cards'

class CardSwapRequestInfo(models.Model):
    main_id = models.AutoField(primary_key=True)
    src_user = models.ForeignKey(Accounts, related_name='src_user_mapping', on_delete=CASCADE)
    dest_user = models.ForeignKey(Accounts, related_name='dest_user_mapping', on_delete=CASCADE)
    src_card = models.ForeignKey(Cards, related_name='src_card_mapping', on_delete=CASCADE)
    dest_card = models.ForeignKey(Cards, related_name='dest_card_mapping', on_delete=CASCADE)
    status = models.CharField(max_length=254)
    last_update_time = models.IntegerField(null=True)
    creation_time = models.IntegerField(null=True)

    class Meta:
        db_table = 'tbl_card_swap_request_info'