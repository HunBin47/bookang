from rest_framework import serializers

from accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Account
        fields = ('email', 'username', 'first_name', 'last_name', 'phone_number')