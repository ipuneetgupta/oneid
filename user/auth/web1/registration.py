from user.models import User,UserProfile
from decouple import config
API_ENDPOINT = config('API_ENDPOINT')


def register(body):
    try:
        #user already exist
        if User.objects.filter(email=body['email']).exists() or \
                User.objects.filter(username=body['username']).exists():
            return 'user already exist'
        #create new user
        user_profile = body['profile']
        del body['profile']
        user = User(
            **body
        )
    except KeyError:
        return 'body invalid'

        user.set_password(body['password'])
        user.save()
        user_profile = UserProfile.objects.create(
            **user_profile,user=user
        )
        return {
                'status':True,
                'message':'user created !',
                'data': {
                    'user_id':user.id,
                    'name':user.first_name,
                    'email_id':user.email
                }
            }