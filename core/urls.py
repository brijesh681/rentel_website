from django.urls import path,include
from .views import *



urlpatterns = [

    # user related API


    path('userlist/',UserListAPIView.as_view()),  # to view list of all users 

    path('userupdate/<int:id>/',UserUpdateAPIView.as_view()),  # update users or delete user 




    # subscription related API

    path('usersubscription/',UserSubscriptionAPIView.as_view()),  # to do user subscription

    path('list_of_usersubscriptions/',UserSubscriptionListAPIView.as_view()),  # to view user subscriptions list

    path('usersubscription_update/<int:id>/',UserSubscriptionUpdate.as_view()), # user subscription  update or delete

    path('checkusersubscription/<int:id>/',CheckUserSubscriptionAPIView.as_view()),  # to check user subscription

    path('usersubscription/<int:id>/renew/', RenewSubscription.as_view()), # to renew user subscription

    path('renew_usersubscription_list/', RenewSubscriptionList.as_view()), # view list of renew subscriptions 

    path('checkrenew/<int:id>/',CheckRenewSubscription.as_view()), # to check renew  subscription 


    

    # plan related API

    path('subscriptionplans_create/',SubscriptionPlansCreate.as_view()),  # to palns create

    path('subscriptionplans_list/',SubscriptionPlansList.as_view()),  # to view list of plans

    path('subscriptionplan_update/<int:id>/',SubscriptionPlanUpdateAPIView.as_view()), # subscription plan update or delete


]