from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager
import datetime


# Create your models here.


GENDER = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other"),
)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=30, null=True)
    mobile = models.CharField(max_length=13, null=True)
    address1 = models.TextField(max_length=200, null=True)
    address2 = models.TextField(max_length=100, null=True)
    state = models.TextField(max_length=20, null=True)
    country = models.CharField(max_length=20, null=True)
    pincode = models.IntegerField(null=True)
    land_mark = models.CharField(max_length=80, blank=True)
    gender = models.CharField(max_length=12, choices=GENDER)
    is_customer = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    active=models.BooleanField(default=True)
    notification_token = models.CharField(max_length=64, blank=True, null=True)
    passwordchanged = models.BooleanField(default=False)
    subscribed = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return str(self.id) + " " + str(self.email)
class SubscriptionPlans(models.Model):
    name=models.CharField(max_length=50,null=True,blank=True)
    months=models.IntegerField(default=0)
    days = models.IntegerField(default=0)
    amount=models.IntegerField(default=0)
    active=models.BooleanField(default=True)
    details=models.TextField(default="")
    quantity_product = models.IntegerField(default = 0)
    quantity_accesserios = models.IntegerField(default = 0)

    def __str__(self):
        return self.name + " " + str(self.amount)
        
    class Meta:
        verbose_name_plural = 'Subscription Plans'

class UserSubscription(models.Model):
    
    user=models.ForeignKey('core.User', on_delete=models.CASCADE)
    plan=models.ForeignKey("core.SubscriptionPlans",on_delete=models.CASCADE)
    start_date=models.DateField(null=True,blank=True)
    end_date=models.DateField(null=True,blank=True)
    total_amount=models.IntegerField(default=0)
    active=models.BooleanField(default=True)
    created_date=models.DateField(auto_now=True)  
    tax=models.IntegerField(default=0)
    freezedate = models.DateField(null=True,blank=True)
    freezestatus = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.id) + " " + str(self.user.fullname) 
        
    class Meta:
        verbose_name_plural = 'User Subscription'
