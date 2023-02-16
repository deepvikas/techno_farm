from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from users.views import Authenticate
from users.models import FarmUser
from .models import Farm, Crop, Season
from .serialiers import FarmSerializer, CropSerializer, SeasonSerializer

import logging
_logger = logging.getLogger(__name__)

# Create your views here.

class AddFarmView(APIView):
    def post(self, request):
        auth = Authenticate()
        res = auth.check_authentication(request)
        if not res.get('status'):
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)
        payload = res.get('result')
        user = FarmUser.objects.get(id=payload['id'])
        try:
            serializer = FarmSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            farm = Farm.objects.get(id=serializer.data['id'])
            farm.farmer_id = user
            if request.data.get('season_id'):
                season = Season.objects.get(id=request.data.get('season_id'))
                farm.season_id = season
            farm.save()
            data = {
                'status': True,
                'message': 'Farm Added Successfully',
                'farm_id': serializer.data['id']
            }
            _logger.error("po45 2")
            code = status.HTTP_201_CREATED
        except Exception as e:
            data = {
                'status': False,
                'message': e
            }
            _logger.error(e)
            code = status.HTTP_400_BAD_REQUEST
        return Response(data, status=code)

class AddCropView(APIView):

    def post(self, request):
        auth = Authenticate()
        res = auth.check_authentication(request)
        if not res.get('status'):
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)
        payload = res.get('result')
        user = FarmUser.objects.get(id=payload['id'])
        res_access = auth.check_admin(user)
        if not res_access.get('status'):
            return Response(res_access, status=status.HTTP_403_FORBIDDEN)

        data = dict()
        try:
            crop = CropSerializer(data=request.data)
            crop.is_valid(raise_exception=True)
            crop.save()
            data = crop.data
            code = status.HTTP_201_CREATED
        except Exception as e:
            data = {
                'status': False,
                'message': e
            }
            code = status.HTTP_400_BAD_REQUEST
        return Response(data, status=code)


class UpdateCropsView(APIView):
    
    def patch(self, request, farm_id):
        auth = Authenticate()
        res = auth.check_authentication(request)
        if not res.get('status'):
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)
        payload = res.get('result')
        user = FarmUser.objects.get(id=payload['id'])
        data = dict()
        if request.data.get('crop_id') and farm_id:
            try:
                farm = Farm.objects.filter(id=int(farm_id)).first()
                if farm and farm.farmer_id.id == user.id:
                    crop = Crop.objects.get(id=int(request.data.get('crop_id')))
                    if crop:
                        farm.crop_id = crop
                        farm.save()
                        code = status.HTTP_200_OK
                        data['status']=True
                        data['message'] = 'Crop Updated Successfully'
                    else:
                        data['False']=False
                        data['message'] = 'Invalid crop_id'
                        code = status.HTTP_400_BAD_REQUEST
                else:
                    data['False']=False
                    data['message'] = 'Invalid farm_id'
                    code = status.HTTP_400_BAD_REQUEST
            except Exception as e:
                data = {
                    'status': False,
                    'message': e
                }
                code = status.HTTP_400_BAD_REQUEST
        else:
            data['statu'] = False
            data['message'] = 'Invalid or Missing crop_id or farm_id'
            code = status.HTTP_400_BAD_REQUEST
        return Response(data, status=code)

class UpdateFarmView(APIView):
    def patch(self, request, farm_id):
        auth = Authenticate()
        res = auth.check_authentication(request)
        if not res.get('status'):
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)
        payload = res.get('result')
        user = FarmUser.objects.get(id=payload['id'])
        data = dict()
        try:
            farm = Farm.objects.filter(id=int(farm_id)).first()
            if farm.farmer_id.id == user.id:
                farm_serializer = FarmSerializer(farm, data=request.data, partial=True)
                farm_serializer.is_valid(raise_exception=True)
                farm_serializer.save()
                if request.data.get('season_id'):
                    season = Season.objects.get(id=int(request.data.get('season_id')))
                    farm.season_id = season
                if request.data.get('crop_id'):
                    crop = Crop.objects.get(id=int(request.data.get('crop_id')))
                    farm.crop_id = crop
                farm.save()
                data['status'] = True
                data['message'] = 'Farm Details Updated Successfully'
                code = status.HTTP_200_OK
            else:
                data['False']=False
                data['message'] = 'Invalid farm_id'
                code = status.HTTP_400_BAD_REQUEST
        except Exception as e:
            data = {
                'status': False,
                'message': e
            }
            code = status.HTTP_400_BAD_REQUEST
        return Response(data, status=code)

class AvailableCropsView(APIView):
    def get(self, request):
        auth = Authenticate()
        res = auth.check_authentication(request)
        if not res.get('status'):
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)
        crops = Crop.objects.all()
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(crops, request)
        serializer = CropSerializer(result_page, many=True, context={'request':request})        
        response = Response(serializer.data, status=status.HTTP_200_OK)
        return response

class GetAllFarmsDetails(APIView):

    def get(self, request):
        auth = Authenticate()
        res = auth.check_authentication(request)
        if not res.get('status'):
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)
        payload = res.get('result')
        user = FarmUser.objects.get(id=payload['id'])
        farms = Farm.objects.all().filter(farmer_id=user.id)
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(farms, request)
        serializer = FarmSerializer(result_page, many=True, context={'request':request})
        response = Response(serializer.data, status=status.HTTP_200_OK)
        return response

class GetFarm(APIView):

    def get(self, request, farm_id):
        data = dict()
        if farm_id:
            auth = Authenticate()
            res = auth.check_authentication(request)
            if not res.get('status'):
                return Response(res, status=status.HTTP_401_UNAUTHORIZED)
            payload = res.get('result')
            user = FarmUser.objects.get(id=payload['id'])
            farm = Farm.objects.get(id=int(farm_id))
            if farm.farmer_id.id == user.id:
                serializer = FarmSerializer(farm)
                data = serializer.data
                code = status.HTTP_200_OK
            else:
                data['False']=False
                data['message'] = 'Invalid farm_id'
                code = status.HTTP_400_BAD_REQUEST
        else:
            data['False']=False
            data['message'] = 'Missing farm_id'
            code = status.HTTP_400_BAD_REQUEST
        return Response(data, status=code)

class AllSeasonsView(APIView):
    def get(self, request):
        auth = Authenticate()
        res = auth.check_authentication(request)
        if not res.get('status'):
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)
        season = Season.objects.all()
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(season, request)
        serializer = SeasonSerializer(result_page, many=True, context={'request':request})
        response = Response(serializer.data, status=status.HTTP_200_OK)
        return response

class AddSeasonView(APIView):

    def post(self, request):
        auth = Authenticate()
        res = auth.check_authentication(request)
        if not res.get('status'):
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)
        payload = res.get('result')
        user = FarmUser.objects.get(id=payload['id'])
        res_access = auth.check_admin(user)
        if not res_access.get('status'):
            return Response(res_access, status=status.HTTP_403_FORBIDDEN)

        data = dict()
        try:
            season = SeasonSerializer(data=request.data)
            season.is_valid(raise_exception=True)
            season.save()
            data = season.data
            code = status.HTTP_201_CREATED
        except Exception as e:
            data = {
                'status': False,
                'message': e
            }
            code = status.HTTP_400_BAD_REQUEST
        return Response(data, status=code)
