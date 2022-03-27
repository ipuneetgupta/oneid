from rest_framework.views import APIView
from rest_framework.response import Response
from user.models import UserProfile, User
import secrets
from rest_framework import status


class AddUser(APIView):
    def post(self, request):
        public_address = request.data["public_add"]

        if public_address == "":
            return Response({
                "message": "please provide public address",
                "status": False
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=public_address)
        except User.DoesNotExist:
            user = User()
            user.username = public_address
            user.save()
            UserProfile.objects.create(user=user, active=True)

        user_obj = User.objects.get(username=public_address)
        nonce = secrets.token_urlsafe()
        print(nonce)
        user_obj.nonce = nonce
        user_obj.save()
        return Response({
            "status": True,
            "nonce": nonce
        })


