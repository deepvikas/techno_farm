from rest_framework import serializers

from . models import FarmUser

class FarmUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = FarmUser
        fields = ['username', 'password', 'user_type', 'first_name', 'last_name', 'email', 'address_line', 'city', 'zip_code', 'mobile', 'latitude', 'longitude']
