from django.urls import path,include
from .views import *



urlpatterns = [
    path('usersubscription/',UserSubscriptionAPIView.as_view()),
    path('subscription/<int:id>/',GetUserSubscriptionAPIView.as_view()),

    path('subscriptionplan_update/<int:id>/',SubscriptionPlanUpdateAPIView.as_view()),
    path('usersubscription/<int:id>/renew/', RenewSubscription.as_view()),
    path('checkrenew/<int:id>/',CheckRenewSubscription.as_view()),

]