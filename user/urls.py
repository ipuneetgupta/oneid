from django.urls import path
from user.views import LoginRequest, \
AcceptConsentRequest,GetAccessToken,UserRegistrationView,login_page,login_request

urlpatterns = [
    #login
    path('login/', LoginRequest.as_view()),
    path('consent/', AcceptConsentRequest.as_view()),
    path('token/', GetAccessToken.as_view()),
    path('login/page', login_page, name='login_page'),
    path('login/request/(?P<pk>\d+)/', login_request, name='login_request'),
    path('user/register/', UserRegistrationView.as_view()),

]
