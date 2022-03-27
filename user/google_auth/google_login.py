from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from user.models import UserProfile
from django.contrib.auth import get_user_model
from coutoEditor.global_variable import BASE_URL
from rest_framework import status


class GoogleView(APIView):
    def post(self, request):
        User = get_user_model()
        token =  request.data["access_token"] # validate the token
        url = "https://www.googleapis.com/oauth2/v2/userinfo"

        payload = {}
        headers = {
            'Authorization': 'Bearer {}'.format(token)
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        data = json.loads(response.text)

        if 'error' in data:
            content = {'message': 'wrong google token / this google token is already expired.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


        # create user if not exist
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            user = User()
            user.username = data['email']
            # provider random default password
            user.password = make_password(BaseUserManager().make_random_password())
            user.email = data['email']
            user.save()
            UserProfile.objects.create(user=user, active=True)

        token = RefreshToken.for_user(user)  # generate token without username & password
        # response = {}
        # response['username'] = user.username
        # response['access_token'] = str(token.access_token)
        # response['refresh_token'] = str(token)
        try:
            photo_url_obj = UserProfile.objects.get(
                user=user
            ).profile_image.url
            photo_url = BASE_URL[:-1] + photo_url_obj
        except:
            photo_url_obj = ""
            photo_url = photo_url_obj
        response = {
            'usersData': {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "profile_image": photo_url},
            'message': 'User logged in successfully',
            'status': True,
            'accessToken': str(token.access_token)
        }
        status_code = status.HTTP_200_OK
        return Response(response)