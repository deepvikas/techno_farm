from rest_framework import serializers

from . models import Farm, Crop, Season
from users.serializers import FarmUserSerializer
from users.models import FarmUser

class SeasonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Season
        fields = ['name', 'start_time', 'end_time', 'id']

class CropSerializer(serializers.ModelSerializer):

    class Meta:
        model = Crop
        fields = ['name', 'variety', 'id']

class FarmSerializer(serializers.ModelSerializer):
    crop_id = serializers.PrimaryKeyRelatedField(allow_null=True, read_only=True)
    farmer_id = serializers.PrimaryKeyRelatedField(allow_null=True, read_only=True)
    season_id = serializers.PrimaryKeyRelatedField(allow_null=True, read_only=True)
    class Meta:
        model = Farm
        fields = ['name', 'address_line', 'city', 'zip_code', 'crop_id', 'farmer_id', 'longitude', 'latitude', 'season_id', 'id']

