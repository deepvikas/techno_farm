import logging
_logger = logging.getLogger(__name__)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
import jwt, datetime
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import render
from .serializers import FarmUserSerializer
from .models import FarmUser


class Authenticate():
    def check_authentication(self, request):
        response = {
            'status': True,
            'message': 'Success',
        }
        token = request.COOKIES.get('jwt')
        if not token:
            response['status'] = False
            response['message'] = 'Authentication Required'
            return response
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            response['status'] = False
            response['message'] = 'Authentication Required'
            return response
        response['result'] = payload
        return response

    def check_admin(self, user):
        response = {
            'status': True,
            'message': 'Success'
        }
        if user.user_type != 'admin':
            response['status'] = False
            response['message'] = 'Access Denied! Un Authorised Operation'

        return response


class SignupView(APIView):

    def post(self, request):
        response = {
            'status': True,
            'message': 'Successfully Signup !',
            'login_ur': '/login'
        }
        serializer = FarmUserSerializer(data=request.data)
        if request.data['user_type'] == 'admin':
            admin = FarmUser.objects.filter(user_type='admin')
            if admin:
                response['status'] = False
                response['message'] = 'Admin already exist!, Please Login'
                return Response(response, status=status.HTTP_409_CONFLICT)
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(response, status=status.HTTP_201_CREATED)


class LoginView(APIView):

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        user = FarmUser.objects.filter(username=username).first()
        if not user:
            return Response({'message': 'Incorrect Username !'},
                            status=status.HTTP_401_UNAUTHORIZED)
        if not user.password == password:
            return Response({'message': 'Incorrect password !'},
            status=status.HTTP_401_UNAUTHORIZED)

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256').decode("utf-8")
        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'status': True,
            'message': 'Login Successfull for {}'.format(user.username)
        }
        response.status = status.HTTP_200_OK
        return response

class LogoutView(APIView):

    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'status': True,
            'message': 'Logout successfully !'
        }
        response.status = status.HTTP_200_OK
        return response

class AddFarmerView(APIView):

    def post(self, request):
        if request.data['user_type'] == 'admin':
            return Response({'message': 'Not a farmer'}, status=status.HTTP_400_BAD_REQUEST)
        auth = Authenticate()
        res = auth.check_authentication(request)
        if not res.get('status'):
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)
        payload = res.get('result')
        user = FarmUser.objects.get(id=payload['id'])
        res_access = auth.check_admin(user)
        if not res_access.get('status'):
            return Response(res_access, status=status.HTTP_403_FORBIDDEN)
        try:
            farmer = FarmUserSerializer(data=request.data)
            farmer.is_valid(raise_exception=True)
            farmer.save()
            data = farmer.data
            code = status.HTTP_201_CREATED
        except Exception as e:
            data = {
                'status' : False,
                'message': e
            }
            code = status.HTTP_400_BAD_REQUEST
        return Response(data, status=code)

class UpdateFarmerView(APIView):
    
    def patch(self, request):
        auth = Authenticate()
        res = auth.check_authentication(request)
        if not res.get('status'):
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)
        payload = res.get('result')
        user = FarmUser.objects.filter(id=payload['id']).first()
        data = dict()
        try:
            if (request.data.get('user_type') and user.user_type == request.data.get('user_type')) or (not request.data.get('user_type')):
                user = FarmUserSerializer(user, data=request.data, partial=True)
                user.is_valid(raise_exception=True)
                user.save()
                data['status'] = True
                data['message'] = 'User Updated Successfully'
                code = status.HTTP_200_OK
            else:
                data['status'] = False
                data['message'] = 'Invalid User type'
                code = status.HTTP_401_UNAUTHORIZED
        except Exception as e:
            data = {
                'status' : False,
                'message': e
            }
            code = status.HTTP_400_BAD_REQUEST
        return Response(data, status=code)

class SearchFarmerView(APIView):

    def get(self, request):
        auth = Authenticate()
        res = auth.check_authentication(request)
        if not res.get('status'):
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)
        payload = res.get('result')
        user = FarmUser.objects.get(id=payload['id'])
        res_access = auth.check_admin(user)
        if not res_access.get('status'):
            return Response(res_access, status=status.HTTP_403_FORBIDDEN)
        farmer = None
        FarmUser.objects.get(id=payload['id'])
        keys = request.query_params.keys()
        farmer = FarmUser.objects
        found = False
        for key in keys:
            if not key in ['limit', 'offset']:
                if key == 'first_name':
                    farmer = farmer.filter(first_name=request.query_params[key])
                    found = True
                elif key == 'last_name':
                    farmer = farmer.filter(last_name=request.query_params[key])
                    found = True
                elif key == 'city':
                    farmer = farmer.filter(city=request.query_params[key])
                    found = True
                elif key == 'latitude':
                    farmer = farmer.filter(latitude=request.query_params[key])
                    found = True
                elif key == 'longitude':
                    farmer = farmer.filter(longitude=request.query_params[key])
                    found = True
                elif key == 'address_line':
                    farmer = farmer.filter(address_line=request.query_params[key])
                    found = True
                elif key == 'crop_id':
                    farmer = farmer.filter(crop_id=int(request.query_params[key]))
                    found = True
        if not keys:
            found = True
            farmer = farmer.all()
        if not found:
            return Response({'message': 'Not Matched Found'},
                            status=status.HTTP_204_NO_CONTENT)
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(farmer, request)
        serializer = FarmUserSerializer(result_page, many=True, context={'request':request})
        response = Response(serializer.data, status=status.HTTP_200_OK)
        return response
    
class MyProfileView(APIView):
    def get(self, request):
        auth = Authenticate()
        res = auth.check_authentication(request)
        if not res.get('status'):
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)
        payload = res.get('result')
        user = FarmUser.objects.get(id=payload['id'])
        serializer = FarmUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DeleteFarmerView(APIView):

    def delete(self, request, farmer_id):
        data = dict()
        auth = Authenticate()
        res = auth.check_authentication(request)
        if not res.get('status'):
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)
        payload = res.get('result')
        user = FarmUser.objects.get(id=payload['id'])
        res_access = auth.check_admin(user)
        if not res_access.get('status'):
            return Response(res_access, status=status.HTTP_403_FORBIDDEN)
        if farmer_id:
            farmer = FarmUser.objects.filter(id=int(farmer_id)).first()
            if farmer:
                if farmer.user_type != 'admin':
                    farmer.delete()
                    data['status'] = True
                    data['message'] = 'Farmer Deleted successfully'
                    code = status.HTTP_200_OK
                else:
                    data['False']=False
                    data['message'] = "Can't delete admin"
                    code = status.HTTP_409_CONFLICT    
            else:
                data['False']=False
                data['message'] = 'Invalid farmer_id'
                code = status.HTTP_400_BAD_REQUEST
        else:
            data['False']=False
            data['message'] = 'Missing farmer_id'
            code = status.HTTP_400_BAD_REQUEST
        return Response(data, status=code)
