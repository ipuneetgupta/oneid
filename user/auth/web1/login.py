from user.models import User, UserProfile
from decouple import config
from django.contrib.auth import authenticate

# API_ENDPOINT = config('API_ENDPOINT')


def login(body):
    # user doesn't exist
    if 'email' not in body.keys() or 'password' not in body.keys():
        return 'body invalid'
    if not User.objects.filter(email=body['email']).exists():
        return "user doesn't exist"
    # authenticate new user
    user = User.objects.get(email=body['email'])
    username = user.username
    user_obj = authenticate(
        username=username,
        password=body['password']
    )
    if user_obj is None:
        return 'wrong password!'
    return {
        'status': True,
        'message': 'user authenticate !',
        'data': {
            'user_id': user.id,
            'name': user.first_name,
            'email_id': user.email
        }
    }
