from django.shortcuts import render
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import User

from common.authentication import JWTAuthentication
from .serializers import UserSerializer


class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data
        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Passwords do not match!')

        data['is_manager'] = 'api/manager' in request.path  # check if exist in request path
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginAPIView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Incorrect Password!')

        scope = 'manager' if 'api/manager' in request.path else 'admin'

        if user.is_manager and scope == 'admin':
             raise exceptions.AuthenticationFailed('Unauthorized')

        token = JWTAuthentication.generate_jwt(user.id, scope)
        # return Response(UserSerializer(user).data)
        response = Response()
        response.set_cookie(key='jwt', value=token,
                            httponly=True)  # if we add this flag frontend can't access this cookie
        response.data = {
            'message': 'success'
        }
        return response


class UserAPIView(APIView):  # this would return our authenticated user
    authentication_classes = [JWTAuthentication]  # try to authenticate user
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = UserSerializer(request.user).data

        if 'api/manager' in request.path:
            data['revenue'] = user.revenue  # show revenue for this type of user

        return Response(data)


class LogoutAPIView(APIView):  # this would logout our authenticated user
    authentication_classes = [JWTAuthentication]  # try to authenticate user
    permission_classes = [IsAuthenticated]

    def post(self, _):  # we dont use request here
        response = Response()
        response.delete_cookie(key='jwt')  # to logout we need to delete cookie

        response.data = {
            'message': 'success'
        }
        return response


class ProfileInfoAPIView(APIView):
    authentication_classes = [JWTAuthentication]  # try to authenticate user
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        user = request.user
        serializer = UserSerializer(user, data=request.data,
                                    partial=True)  # partial lets us update only important fields
        serializer.is_valid(raise_exception=True)
        serializer.save()  # save changes
        return Response(serializer.data)


class ProfilePasswordAPIView(APIView):
    authentication_classes = [JWTAuthentication]  # try to authenticate user
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        user = request.user
        data = request.data

        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Passwords do not match!')

        user.set_password(data['password'])
        user.save()
        return Response(UserSerializer(user).data)
