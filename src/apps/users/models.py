from django.db import models

class Accounts(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=254)
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    full_name = models.CharField(max_length=254, default="")
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=254)
    is_active = models.BooleanField(default=False)
    last_update_time = models.IntegerField(null=True)
    creation_time = models.IntegerField(null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'tbl_accounts'
