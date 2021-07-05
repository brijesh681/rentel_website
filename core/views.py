from django.shortcuts import render
from . import models, serializers
from rest_framework import viewsets, status, permissions, generics
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import *
from rest_framework.response import Response
from core.models import *
#from . import models
from .serializers import *
from datetime import datetime, timedelta,date
from rest_framework.generics import *
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.


class UserSerializerAPIViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated,]
    http_method_names = ['post', 'head','options']

    def get_permissions(self):
        if self.action == 'post':
            permission_classes = [IsAuthenticated]
            # user = self.queryset.get(id=self.request.user.id)
            # if user.isadmin:
            #     permission_classes = [IsAuthenticated]
            # else:
            #     return Response("error",status=401)
        else:
            permission_classes = [IsAdminUser]
            # permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserDataSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def list(self, request, *args, **kwargs ):
        if not(request.user.is_admin == True):
            return Response({"msg": "you have not permission to View list of all user ."}, status=401)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset,many=True)
        return Response(serializer.data, status=200) 


class UserUpdateAPIView(RetrieveUpdateAPIView,DestroyAPIView):

    queryset = User.objects.all()
    serializer_class = UserDataSerializer
    #permission_classes = [permissions.IsAuthenticated, ]
    lookup_field='id'

    '''def retrieve(self,request,*args,**kwargs):

        if not(request.user.is_admin==True):          
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
 
        try:
            instance = self.queryset.get(id=self.kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"DOES_NOT_EXIST":"Does not exist"},status=400)
 
        serializer = self.get_serializer(instance)

        return Response(serializer.data,status=200)

    def patch(self,request,*args,**kwargs):

        if not(request.user.admin==True):
            
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
        try:
            instance = self.queryset.get(id=self.kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"DOES_NOT_EXIST":"Does not exist"},status=400)
        
        serializer = self.get_serializer(instance,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data,status=200)


    def destroy(self,request,*args,**kwargs):

        if not(request.user.is_admin==True):
            
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
        try:
            instance = self.queryset.get(id=self.kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"DOES_NOT_EXIST":"Does not exist"},status=400)
        
        instance.active=False
        instance.releasing_date=datetime.now().date()
        instance.save()
        serializer = self.get_serializer(instance)

        return Response({"SUCCESS": "Successfully Deleted"}, status=200)'''





class CheckUserSubscriptionAPIView(ListAPIView):

    queryset = UserSubscription.objects.all()
    serializer_class = GetUserSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def list(self,request,*args,**kwargs):
        if not(request.user.active==True):
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

        user = User.objects.get(id=kwargs["id"])
        #print(user.username)
        if user.subscribed==False:
            return Response({"ended": "No active Subscription"}, status=200)
        try:
            queryset = self.queryset.get(user=user,active=True)

        except:
            return Response({"ended": "No active Subscription"}, status=200)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=200)

class UserSubscriptionAPIView(CreateAPIView):

    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    http_method_names = ['post']

    def create(self,request,*args,**kwargs):
        
        if not(request.user.is_admin==True):
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
        serializer = UserSubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        start_date=datetime.strptime(request.data["start_date"], '%Y-%m-%d')
        plan=SubscriptionPlans.objects.get(id=request.data["plan"])
        if plan.months==0 and plan.days != 0:
            days=timedelta(days=plan.days)
        elif plan.months != 0 and plan.days != 0:
            day= timedelta(days=plan.days)
            days=timedelta(days=30*plan.months)
            days=days+day
        elif plan.months !=0 and plan.days == 0:
            days=timedelta(days=30*plan.days)
        end_date=start_date + days

        total_amount=plan.amount
        user=User.objects.get(id=request.data["user"])
        user.subscribed=True
        user.save()
        print(user.subscribed)

        serializer.save(end_date=end_date,total_amount=total_amount)

 
        return Response(serializer.data,status=201)


class UserSubscriptionListAPIView(ListAPIView):

    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionListSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    def list(self, request, *args, **kwargs):
        if not (request.user.is_admin == True):
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)


class UserSubscriptionUpdate(RetrieveUpdateAPIView,DestroyAPIView):

    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    lookup_field='id'

    def retrieve(self,request,*args,**kwargs):

        if not(request.user.is_admin==True):          
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
 
        try:
            instance = self.queryset.get(id=self.kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"DOES_NOT_EXIST":"Does not exist"},status=400)
 
        serializer = self.get_serializer(instance)

        return Response(serializer.data,status=200)

    def patch(self,request,*args,**kwargs):

        if not(request.user.active==True):
            
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
        try:
            instance = self.queryset.get(id=self.kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"DOES_NOT_EXIST":"Does not exist"},status=400)
        
        serializer = self.get_serializer(instance,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data,status=200)


    def destroy(self,request,*args,**kwargs):

        if not(request.user.is_admin==True):
            
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
        try:
            instance = self.queryset.get(id=self.kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"DOES_NOT_EXIST":"Does not exist"},status=400)
        
        instance.active=False
        instance.releasing_date=datetime.now().date()
        instance.save()
        serializer = self.get_serializer(instance)

        return Response({"SUCCESS": "Successfully Deleted"}, status=200)



class RenewSubscription(CreateAPIView):
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated, ]


    def create(self, request, *args, **kwargs):

        if not (request.user.active==True):
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

        cust = UserSubscription.objects.filter(user=kwargs['id'], active=True)
        if cust.count() == 0:
            serializer = UserSubscriptionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            start_date = datetime.strptime(request.data["start_date"], '%Y-%m-%d')
            plan = SubscriptionPlans.objects.get(id=request.data["plan"])
            if plan.months==0 and plan.days != 0:
                days=timedelta(days=plan.days)
            elif plan.months != 0 and plan.days != 0:
                day= timedelta(days=plan.days)
                days=timedelta(days=30*plan.months)
                days=days+day
            elif plan.months !=0 and plan.days == 0:
                days=timedelta(days=30*plan.days)
            end_date=start_date + days

            total_amount = plan.amount
            
            serializer.save(end_date=end_date, total_amount=total_amount, plan=plan)
            
            return Response(serializer.data, status=201)
        cust=cust[0]
        #print(cust.id)
        #print(cust.end_date)
        start_date = cust.end_date + timedelta(days=1)

        a = UserSubscription.objects.filter(user=kwargs['id'], active=False,start_date__gte=cust.end_date)
        if a.count() != 0:
            return Response({"Error": "OOPS!! You Already Have One Renewed Plan Pending..."}, status=400)
        serializer = UserSubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan = SubscriptionPlans.objects.get(id=request.data["plan"])
        if plan.months==0 and plan.days != 0:
            days=timedelta(days=plan.days)
        elif plan.months != 0 and plan.days != 0:
            day= timedelta(days=plan.days)
            days=timedelta(days=30*plan.months)
            days=days+day
        elif plan.months !=0 and plan.days == 0:
            days=timedelta(days=30*plan.days)
        end_date=start_date + days
        
        serializer.save(end_date=end_date,start_date = start_date,active=False)
        
        return Response(serializer.data, status=201)

        


class RenewSubscriptionList(ListAPIView):
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def list(self, request, *args, **kwargs):
        if not (request.user.is_admin == True):
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

        queryset= UserSubscription.objects.filter(active=False,start_date__gte=date.today())
        serializer =  UserSubscriptionSerializer(queryset,many=True)
        return Response(serializer.data, status=200)


class CheckRenewSubscription(RetrieveAPIView):
    queryset = UserSubscription.objects.all()
    serializer_class = GetUserSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    looku_field = 'id'

    def get(self, request, *args, **kwargs):

        if not (request.user.active==True):
            return Response({"NO_ACCESS": "Access Denied"}, status=401)

        try:
            cust = UserSubscription.objects.get(user=kwargs['id'], active=True)
        except:
            return Response({"msg":"you have not any subscription"}, status=200)
        #print(cust.user.email)
        a = UserSubscription.objects.filter(user=kwargs['id'], active=False,start_date__gte=cust.end_date)
        if a.count() != 0:
           # print(a)

            serializer =  GetUserSubscriptionSerializer(a,many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"msg" : "you have not any renew subscription"},status=200)




class SubscriptionPlansCreate(CreateAPIView):
    queryset = SubscriptionPlans.objects.all()
    serializer_class = SubscriptionPlansSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def create(self, request, *args, **kwargs ):
        if not(request.user.is_admin == True):
            return Responce({"msg": "you have not permission to create subscription plan"}, status=401)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200) 


class SubscriptionPlansList(ListAPIView):
    queryset = SubscriptionPlans.objects.all()
    serializer_class = SubscriptionPlansSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def list(self, request, *args, **kwargs ):
        if not(request.user.is_admin == True):
            return Responce({"msg": "you have not permission to View list of subscription plan"}, status=401)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset,many=True)
        return Response(serializer.data, status=200) 


class SubscriptionPlanUpdateAPIView(RetrieveUpdateAPIView,DestroyAPIView):

    queryset = SubscriptionPlans.objects.all()
    serializer_class = SubscriptionPlansSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    lookup_field='id'

    def retrieve(self,request,*args,**kwargs):

        if not(request.user.is_admin==True):          
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
 
        try:
            instance = self.queryset.get(id=self.kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"DOES_NOT_EXIST":"Does not exist"},status=400)
 
        serializer = self.get_serializer(instance)

        return Response(serializer.data,status=200)

    def patch(self,request,*args,**kwargs):

        if not(request.user.admin==True):
            
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
        try:
            instance = self.queryset.get(id=self.kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"DOES_NOT_EXIST":"Does not exist"},status=400)
        
        serializer = self.get_serializer(instance,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data,status=200)


    def destroy(self,request,*args,**kwargs):

        if not(request.user.is_admin==True):
            
            return Response({"NO_ACCESS": "Access Denied"}, status=401)
        try:
            instance = self.queryset.get(id=self.kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"DOES_NOT_EXIST":"Does not exist"},status=400)
        
        instance.active=False
        instance.releasing_date=datetime.now().date()
        instance.save()
        serializer = self.get_serializer(instance)

        return Response({"SUCCESS": "Successfully Deleted"}, status=200)