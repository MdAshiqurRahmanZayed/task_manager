from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['first_name','last_name','email','is_staff','groups','user_permissions']
        