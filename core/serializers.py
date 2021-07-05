from allauth.account.adapter import get_adapter
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers 
from rest_framework.authtoken.models import Token
from core.models import  *
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'mobile', 'password', 'is_customer', 'is_admin', 'notification_token', 'passwordchanged')


class CustomRegisterSerializer(RegisterSerializer):
    is_customer = serializers.BooleanField()
    is_admin = serializers.BooleanField()
    notification_token = serializers.CharField(max_length = 64, allow_blank=True, allow_null=True)
    passwordchanged = serializers.BooleanField()
    mobile = serializers.CharField(max_length=12)

    class Meta:
        model = User
        fields = ('email', 'mobile', 'password', 'is_customer', 'is_admin', 'notification_token','passwordchanged')

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'mobile': self.validated_data.get('mobile', ''),
            'is_customer': self.validated_data.get('is_customer', ''),
            'is_admin': self.validated_data.get('is_admin', ''),
            'notification_token': self.validated_data.get('notification_token', ''),
            'passwordchanged': self.validated_data.get('passwordchanged', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.is_customer = self.cleaned_data.get('is_customer')
        user.mobile = self.cleaned_data.get('mobile')
        user.is_admin = self.cleaned_data.get('is_admin')
        user.notification_token = self.cleaned_data.get('notification_token')
        user.passwordchanged = self.cleaned_data.get('passwordchanged')
        user.save()
        adapter.save_user(request, user, self)
        return user


class TokenSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()
    notification_token = serializers.SerializerMethodField()
    passwordchanged = serializers.SerializerMethodField()

    class Meta:
        model = Token
        fields = ('key', 'user', 'user_type', 'notification_token', 'passwordchanged')

    def get_user_type(self, obj):
        serializer_data = UserSerializer(
            obj.user
        ).data
        is_customer = serializer_data.get('is_customer')
        is_admin = serializer_data.get('is_admin')
        return {
            'is_customer': is_customer,
            'is_admin': is_admin,
        }
    
    def get_notification_token(self, obj):
        serializer_data = UserSerializer(
            obj.user
        ).data
        notification_token = serializer_data.get('notification_token')
        return notification_token

    def get_passwordchanged(self, obj):
        serializer_data = UserSerializer(
            obj.user
        ).data
        passwordchanged = serializer_data.get('passwordchanged')
        return passwordchanged
class SubscriptionPlansSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=SubscriptionPlans
        fields='__all__'


class UserSubscriptionSerializer(serializers.ModelSerializer):
 
    class Meta:
        model= UserSubscription
        exclude=('active','end_date',)


class GetUserSubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSubscription
        fields = '__all__'



class GetUserSubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSubscription
        fields = '__all__'
