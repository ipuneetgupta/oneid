from rest_framework.views import APIView
from rest_framework.response import Response
from user.models import UserProfile, User
from subprocess import PIPE, Popen
from rest_framework_jwt.settings import api_settings
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER
from django.contrib.auth.models import update_last_login
from coutoEditor.global_variable import BASE_URL
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
import secrets


class VerifySignature(APIView):
    def post(self, request):
        signature = request.data["signature"]
        nonce = request.data["nonce"]
        if nonce == "" or signature == "":
            return Response({
                "message": "signature or nonce missing",
                "status": False
            },
                status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(nonce__iexact=nonce)
        except ObjectDoesNotExist:
            return Response({
                "message": "incorrect nonce",
                "status": False
            }, status.HTTP_400_BAD_REQUEST)

        public_add = user.username

        def cmdline(command):
            process = Popen(
                args=command,
                stdout=PIPE,
                shell=True,
                universal_newlines=False
            )
            return process.communicate()[0]

        output = cmdline("node user/metamask/verify.js {} {} {}".format(signature, public_add, nonce))

        decoded_output = output.decode('utf-8').split('\n')[0]
        if decoded_output == "Verified":
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
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
                'accessToken': jwt_token
            }
            status_code = status.HTTP_200_OK
        else:
            response = {
                "message": decoded_output,
                "status": False
            },
            status_code = status.HTTP_400_BAD_REQUEST
        user_obj = User.objects.get(username=public_add)
        nonce = secrets.token_urlsafe()
        print(nonce)
        user_obj.nonce = nonce
        user_obj.save()
        return Response(response, status_code)



