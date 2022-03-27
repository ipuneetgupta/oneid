from urllib import response
from rest_framework.views import APIView
from rest_framework.response import Response
from library.hydra import create_hydra
import requests
from django.shortcuts import render,get_object_or_404,redirect
from decouple import config
from rest_framework import viewsets, status
from user.auth.web1.login import login
from user.auth.web1.registration import register

AUTH_CLIENT_ID = config('AUTH_CLIENT_ID')
AUTH_CLIENT_SECRET = config('AUTH_CLIENT_SECRET')
hydra = create_hydra()


def login_page(request):
    login_challenge = request.GET['login_challenge']
    return render(
        request,
        'login.html',
        {'login_challenge':login_challenge}
    )

def login_request(request,pk):
    login_challenge = pk
    if request.method == 'POST':
        body = {
            "email":request.POST.get('username'),
            "password":request.POST.get('password')
                }
        res = login(body)
        if type(res) is not dict:
            return render(request,'res.html',{"response":res})

        login_request_body = hydra.get_login_request(login_challenge)
        accepted_request = hydra.accept_login_request(login_challenge, accept_login_config={
            "subject": "ut ",
            "acr": "labo",
            "context": "<object>",
            "force_subject_identifier": "ex fugiat aliquip amet dolore",
            "remember": True,
            "remember_for": 3600
        })
        login_request_body['consent_url'] = accepted_request
        return redirect("http://127.0.0.1:4444/oauth2/auth?audience=&max_age=0&nonce=cbcvurctcddwfhzsnltwyz343&prompt=&redirect_uri=http://127.0.0.1:8000/api/token&response_type=code&scope=openid+offline&state=dsfssfsfsfsfslmksmf&client_id=videowiki")



class UserRegistrationView(APIView):

    def post(self, request):
        response = register(request.data)

        if response == "user already exist":
            return Response({
                'status': False,
                'message': 'user already exist please user different email and username!',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        elif response == "body invalid":
            return Response({
                'status': False,
                'message': 'request body is invalid!',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response(response, status=status.HTTP_200_OK)



class LoginRequest(APIView):
    def post(self, request):
        response = login(request.data)
        if response == "user doesn't exist":
            return Response({
                'status': False,
                'message': "user doesn't exist , register yourself",
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        elif response == "wrong password":
            return Response({
                'status': False,
                'message': 'invalid Password!',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        elif response == "body invalid":
            return Response({
                'status': False,
                'message': 'request body is invalid!',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        login_challenge = request.GET.get('login_challenge')
        login_request_body = hydra.get_login_request(login_challenge)
        accepted_request = hydra.accept_login_request(login_challenge, accept_login_config={
            "subject": "ut ",
            "acr": "labo",
            "context": "<object>",
            "force_subject_identifier": "ex fugiat aliquip amet dolore",
            "remember": True,
            "remember_for": 3600
        })
        login_request_body['consent_url'] = accepted_request
        # return redirect(accepted_request['redirect_to'])
        return Response(accepted_request)


class AcceptConsentRequest(APIView):
    def get(self, request):
        consent_challenge = request.GET.get('consent_challenge')
        accepted_request = hydra.accept_consent_request(consent_challenge, accept_consent_config={
            "grant_access_token_audience": [],
            "grant_scope": [
                "openid",
                "offline",
                "offline_access",
                "profile"
            ],
            "handled_at": "2019-04-16T04:45:05.685Z",
            "remember": True,
            "remember_for": -72766940,
            "session": {
                "access_token": {},
                "id_token": {}
            }
        })
        return redirect(accepted_request['redirect_to'])
        # return Response(accepted_request)


class GetAccessToken(APIView):
    def get(self, request):
        url = "http://127.0.0.1:4444/oauth2/token"
        code = request.GET.get('code')
        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': 'http://127.0.0.1:8000/api/token',
            'client_id': AUTH_CLIENT_ID,
            'client_secret': AUTH_CLIENT_SECRET
        }

        response = requests.request("POST", url, data=payload)

        return Response(response.json())
