from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.

class User(AbstractUser):
    username = models.CharField(unique=True, max_length=50,null=True,blank=True)
    email = models.EmailField(unique=True,null=True,blank=True)
    login_mode_type = (
        ("web3", "wallet"),
        ("web2", "social_login"),
        ("web1", "web1"),
        ("otp", "otp"),
        ("invite_link", "invite_link")
    )
    login_mode = models.CharField(max_length=20, choices=login_mode_type, null=True, blank=True)
    nonce = models.CharField(max_length=500,null=True,blank=True)
    count = models.IntegerField(default=0, help_text='Number of otp sent',null=True,blank=True)
    otp = models.CharField(max_length=9, blank=True, null=True)
    validated = models.BooleanField(default=False,null=True,blank=True,
                                    help_text='if it is true, that means user have validate otp correctly in seconds')
    USERNAME_FIELD = 'username'
    def __str__(self):
        return self.email


class UserProfile(models.Model):
    profile_image = models.URLField(blank=True, null=True,default=None)
    phone = models.CharField( max_length=20, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    zip = models.CharField(max_length=15, null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='profile')