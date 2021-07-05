from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import viewsets, permissions, generics
from rest_framework.views import exception_handler
from rest_framework.response import Response
from .serializers import *
from core.permissions import *
from .filter import ProductFilter
from core.models import User
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime, timedelta
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
User = get_user_model()
import razorpay

# from .filter import *



class ProductPagination(PageNumberPagination):       
       page_size = 10

class AllProductView(ListAPIView):

    queryset = Product.objects.filter(is_active=True)
    search_fields = ["name"]
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['name','category','color','rental_mrp','product_mrp',]
    filterset_class = ProductFilter
    serializer_class = ProductDisplaySerializer
    lookup_field='id'
    pagination_class = ProductPagination
    

class ProductCreate(CreateAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self,request):

        if not(request.user.is_admin==True):
                return Response({"error": "Access Denied"}, status=401)

        request.data['is_active']=True
        request.data['is_stock'] = True
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)


class ProductDetailAPI(RetrieveAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def retrieve(self,request,*args,**kwargs):
        if not(request.user.active==True):
                return Response({"error": "Access Denied"}, status=401)
        try:
            instance = self.queryset.get(id=kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"error":"Does not exist"},status=404)
        serializer = self.get_serializer(instance)
        return Response(serializer.data,status=200)


class ProductUpdateAPI(RetrieveUpdateDestroyAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def retrieve(self,request,*args,**kwargs):
        if not(request.user.active==True):
                return Response({"error": "Access Denied"}, status=401)
        try:
            instance = self.queryset.get(id=kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"error":"Does not exist"},status=404)
        serializer = self.get_serializer(instance)
        return Response(serializer.data,status=200)

    def partial_update(self, request, *args, **kwargs):
        if not(request.user.is_admin==True):
                return Response({"error": "Access Denied"}, status=401)
        try:
            instance = self.queryset.get(id=kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"error": "Does not exist"}, status=404)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def destroy(self, request, *args, **kwargs):
        if not(request.user.active==True):
                return Response({"error": "Access Denied"}, status=401)
        try:
            instance = self.queryset.get(id=kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"error": "Does not exist"}, status=404)
        instance.is_active=False
        instance.save()
        return Response({"Message": "Successfully Deleted"}, status=200)


class BagView(ListAPIView):
    queryset = Bag.objects.all()
    serializer_class =ViewMyBagSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    def list(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=request.user.id)
        except ObjectDoesNotExist:
            return Response({"DOES_NOT_EXIST": "User Does not exist"}, status=400)

        queryset = self.queryset.filter(user=user,ordered=False)

        if queryset.exists():
            serializer = ViewMyBagSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data, status=200)
        else:
            return Response("Cart is Empty", status=400)
class BagUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = Bag.objects.all()
    serializer_class =BagSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    lookup_field='id'

    def retrieve(self,request,*args,**kwargs):
        if not(request.user.active==True):
                return Response({"error": "Access Denied"}, status=401)
        try:
            instance = self.queryset.get(id=kwargs["id"])
            print(instance.item.quantity)
        except ObjectDoesNotExist:
            return Response({"error": "Cart Does not exist"},status=404)
        serializer = self.get_serializer(instance)
        return Response(serializer.data,status=200)
    def put(self, request, *args, **kwargs):

        if not (request.user.active==True):
            return Response({"error": "User is not a merchant"}, status=401)
        instance = self.queryset.get(id=kwargs["id"])
        item=instance.item
        if not item.is_stock:
            return Response("Out Of Stock", status=404)
        if item.quantity-int(request.data["quantity"])<0:
            return Response({"code": "Out_Of_Stock","error": "You Cannot Buy This Much Quantity"}, status=404)
        
        item.quantity=item.quantity-int(request.data['quantity'])
        item.save()
        #if cart item for rent
        if instance.rent==True:
            # if product in offer 
            if Offer.objects.filter(product=item).exists():
                offer_product = Offer.objects.get(product=item)             
                product_rental_mrp = offer_product.today_rental_mrp
                product_security_deposite = item.security_deposit
                amount = (product_rental_mrp + product_security_deposite)*int(request.data['quantity'])
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(price=amount,rent=True)
                return Response(serializer.data, status=200)
            # IF PRODUCT NOT IN OFFER
            else:
                amount = item.rental_mrp + item.security_deposit
                amount = amount*int(request.data['quantity'])
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(price=amount,rent=True)
                return Response(serializer.data, status=200)   
        # if cart item for buy        
        else:  
            # if product in offer       
            if Offer.objects.filter(product=item).exists():
                offer_product = Offer.objects.get(product=item)             
                product_mrp = offer_product.today_product_mrp
                amount = product_mrp*int(request.data['quantity'])
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(price=amount)
                return Response(serializer.data, status=200)
            # IF PRODUCT NOT IN OFFER
            else:
                amount = item.product_mrp 
                amount = amount*int(request.data['quantity'])
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(price=amount)
                return Response(serializer.data, status=200)
    def destroy(self, request, *args, **kwargs):
        if not(request.user.active==True):
                return Response({"error": "Access Denied"}, status=401)
        try:
            instance = self.queryset.get(id=kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"error": "Does not exist"}, status=404)
        instance.delete()
        return Response({"Message": "Successfully Deleted"}, status=200)

class ReviewAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def create(self, request, *args, **kwargs):
        if Review.objects.filter(product=request.data.get('product'), user=self.request.user).exists():
            return Response({"ALREADY_EXIST": "Already have a review"}, status=400)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer.save(user=request.user))
        return Response(serializer.data, status=200)

class WishlistAPIView(ListCreateAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def list(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=request.user.id)
        except ObjectDoesNotExist:
            return Response({"DOES_NOT_EXIST": "User Does not exist"}, status=400)

        queryset = self.queryset.filter(user=user)
        if queryset.exists():
            serializer = MyWishlistSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data, status=200)
        else:
            return Response({"NO_ITEM": "Empty Bag"}, status=400)

    def create(self, request, *args, **kwargs):
        if Wishlist.objects.filter(product=request.data.get('product'), user=request.user).exists():
            return Response({"ALREADY_EXIST": "Item Already Exists in Wishlist"}, status=400)


        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer.save())
        return Response(serializer.data, status=200)


class MyWishlistAPIView(RetrieveDestroyAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = MyWishlistSerializer
    permission_classes = [permissions.IsAuthenticated,IsOwner]
    lookup_field = 'id'

class CreateDeliveryPincodeAPIView(ListCreateAPIView):
    queryset = DeliveryPincode.objects.all()
    serializer_class = PincodeSerializer
    permission_classes = [permissions.IsAuthenticated,IsAdmin]

    def create(self, request, *args, **kwargs):
        if DeliveryPincode.objects.filter(pincode=request.data.get('pincode'), available=True).exists():
            return Response({"ALREADY_EXIST": "Pincode Already Exists"}, status=200)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer.save())
        return Response(serializer.data, status=200)


class CheckDeliveryPincodeAPIView(ListCreateAPIView):
    queryset = DeliveryPincode.objects.all()
    serializer_class = CheckDeliveryPincodeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if DeliveryPincode.objects.filter(pincode=request.data.get('pincode'), available=True).exists():
            return Response({"DELIVERY_AVAILABLE": "Delivery Available"}, status=200)
        else:
            return Response({"DELIVERY_NOT_AVAILABLE": "Delivery Not Available"}, status=400)

class AddOfferAPIView(ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = AddOfferSerializer
    pagination_class = ProductPagination
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def create(self, request, *args, **kwargs):
        if Offer.objects.filter(product=self.request.data.get('product')).exists():
            return Response({"ALREADY_EXIST": "Product Already Exists in Offer "}, status=400)

        discount_percent = self.request.data.get('discount_percent')
        if float(discount_percent) > 100:
            return Response({"INCORRECT_VALUE": "Discount value s not more then 100"}, status=400)

        try:
            product = Product.objects.get(id=self.request.data.get('product'))
        except ObjectDoesNotExist:
            return Response({"DOES_NOT_EXIST": "Product Does not exist"}, status=400)

        current_rental_mrp = product.rental_mrp
        total_dis = (float(current_rental_mrp) * float(discount_percent)/100)
        total_rental_selling_mrp = (float(current_rental_mrp) - float(total_dis))

        current_product_mrp = product.product_mrp
        total_disc = (float(current_product_mrp) * float(discount_percent)/100)
        total_product_selling_mrp = (float(current_product_mrp) - float(total_disc))
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(
            serializer.save(today_rental_mrp=total_rental_selling_mrp,today_product_mrp=total_product_selling_mrp)
        )
        return Response(serializer.data, status=200)


class OfferDetailAPIView(ListAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ViewAllDealsOfTheDayAPIView(ListAPIView):
    queryset = Offer.objects.filter(offer_type="Deals Of The Day").order_by('-date')
    serializer_class = ViewAllOfferSerializer
    # pagination_class = ProductPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ViewAllFestiveSpecialAPIView(ListAPIView):
    queryset = Offer.objects.filter(offer_type="Festive Special").order_by('-date')
    serializer_class = ViewAllOfferSerializer
    pagination_class = ProductPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ViewAllSummerCollectionAPIView(ListAPIView):
    queryset = Offer.objects.filter(offer_type="Summer Collection").order_by('-date')
    serializer_class = ViewAllOfferSerializer
    pagination_class = ProductPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ViewAllWinterCollectionAPIView(ListAPIView):
    queryset = Offer.objects.filter(offer_type="Winter Collection").order_by('-date')
    serializer_class = ViewAllOfferSerializer
    pagination_class = ProductPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ViewAllFavouriteAPIView(ListAPIView):
    queryset = Offer.objects.filter(offer_type="As Seen Your Favourite").order_by('-date')
    serializer_class = ViewAllOfferSerializer
    pagination_class = ProductPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ViewAllSubscribedUserProductAPIView(ListAPIView):
    queryset = Product.objects.filter(subscription_plan=True).order_by('-date')
    serializer_class = ProductDisplaySerializer
    # pagination_class = ProductPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]








class CategoryAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def create(self, request, *args, **kwargs):
        if Category.objects.filter(category_name=self.request.data.get('category_name')).exists():
            return Response({"ALREADY_EXIST": "Category Already Exists"}, status=400)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer.save())
        return Response(serializer.data, status=200)


class CategoryUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated,IsAdmin]
    lookup_field = 'id'

    def retrieve(self,request,*args,**kwargs):
        if not(request.user.active==True):
                return Response({"error": "Access Denied"}, status=401)
        try:
            instance = self.queryset.get(id=kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"error":"Does not exist"},status=404)
        serializer = self.get_serializer(instance)
        return Response(serializer.data,status=200)

    def partial_update(self, request, *args, **kwargs):
        if not(request.user.is_admin==True):
                return Response({"error": "Access Denied"}, status=401)
        try:
            instance = self.queryset.get(id=kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"error": "Does not exist"}, status=404)
 
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def destroy(self, request, *args, **kwargs):
        if not(request.user.active==True):
                return Response({"error": "Access Denied"}, status=401)
        try:
            instance = self.queryset.get(id=kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"error": "Does not exist"}, status=404)
        instance.is_active=False
        instance.save()
        return Response({"Message": "Successfully Deleted"}, status=200)

class BrandAPIView(ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def create(self, request, *args, **kwargs):
        if Brand.objects.filter(brand_name=self.request.data.get('brand_name')).exists():
            return Response({"ALREADY_EXIST": "Brand Already Exists"}, status=400)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer.save())
        
        return Response(serializer.data, status=200)


class BrandUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAuthenticated,IsAdmin]
    lookup_field = 'id'

    def retrieve(self,request,*args,**kwargs):
        if not(request.user.active==True):
                return Response({"error": "Access Denied"}, status=401)
        try:
            instance = self.queryset.get(id=kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"error":"Does not exist"},status=404)
        serializer = self.get_serializer(instance)
        return Response(serializer.data,status=200)

    def partial_update(self, request, *args, **kwargs):
        if not(request.user.is_admin==True):
                return Response({"error": "Access Denied"}, status=401)
        try:
            instance = self.queryset.get(id=kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"error": "Does not exist"}, status=404)
 
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def destroy(self, request, *args, **kwargs):
        if not(request.user.active==True):
                return Response({"error": "Access Denied"}, status=401)
        try:
            instance = self.queryset.get(id=kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"error": "Does not exist"}, status=404)
        instance.is_active=False
        instance.save()
        return Response({"Message": "Successfully Deleted"}, status=200)



#________________________________________________________________________________________________________________

class AddtoRentBagView(ListCreateAPIView):
    queryset = Bag.objects.all()
    serializer_class = AddToBagSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def list(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=request.user.id)
        except ObjectDoesNotExist:
            return Response({"DOES_NOT_EXIST": "User Does not exist"}, status=400)

        queryset = self.queryset.filter(user=user,ordered=False)
        if queryset.exists():
            serializer = ViewMyBagSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data, status=200)
        else:
            return Response({"NO_ITEM": "Empty Bag"}, status=400)

    def create(self, request, *args, **kwargs):
        # CHECK PRODUCT
        try:
            item = Product.objects.get(id=self.request.data.get('item'))

        except ObjectDoesNotExist:
            return Response({"DOES_NOT_EXIST": "Product Does not exist"}, status=400)
        # CHECK ITEM NOT ALREADY EXISTS
        if Bag.objects.filter(item=item, user=request.user).exists():
            return Response({"ALREADY_EXIST": "Item Already Exists in Bag"}, status=400)
        if not item.is_stock:
            return Response("Out Of Stock", status=404)
        if item.quantity-int(request.data["quantity"])<0:
            return Response({"code": "Out_Of_Stock","error": "You Cannot Buy This Much Quantity"}, status=404)
        
        item.quantity=item.quantity-int(request.data['quantity'])
        item.save()


        if Offer.objects.filter(product=item).exists():
            
            offer_product = Offer.objects.get(product=request.data.get('item'))             
            product_rental_mrp = offer_product.today_rental_mrp
            product_security_deposite = item.security_deposit
            amount = (product_rental_mrp + product_security_deposite)*int(request.data['quantity'])
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer.save(price=amount,rent=True))
            return Response(serializer.data, status=200)
        # IF PRODUCT NOT IN OFFER
        else:
            amount = item.rental_mrp + item.security_deposit
            amount = amount*int(request.data['quantity'])
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer.save(price=amount,rent=True))
            return Response(serializer.data, status=200)



class AddtoBuyBagView(ListCreateAPIView):
    queryset = Bag.objects.all()
    serializer_class = AddToBagSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def list(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=request.user.id)
        except ObjectDoesNotExist:
            return Response({"DOES_NOT_EXIST": "User Does not exist"}, status=400)

        queryset = self.queryset.filter(user=user,ordered=False)
        if queryset.exists():
            serializer = ViewMyBagSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data, status=200)
        else:
            return Response({"NO_ITEM": "Empty Bag"}, status=400)

    def create(self, request, *args, **kwargs):
        # CHECK PRODUCT
        try:
            item = Product.objects.get(id=self.request.data.get('item'))

        except ObjectDoesNotExist:
            return Response({"DOES_NOT_EXIST": "Product Does not exist"}, status=400)
        # CHECK ITEM NOT ALREADY EXISTS
        if Bag.objects.filter(item=item, user=request.user).exists():
            return Response({"ALREADY_EXIST": "Item Already Exists in Bag"}, status=400)
        if not item.is_stock:
            return Response("Out Of Stock", status=404)
        if item.quantity-int(request.data["quantity"])<0:
            return Response({"code": "Out_Of_Stock","error": "You Cannot Buy This Much Quantity"}, status=404)
        
        item.quantity=item.quantity-int(request.data['quantity'])
        item.save()

        if Offer.objects.filter(product=item).exists():
            
            offer_product = Offer.objects.get(product=request.data.get('item'))             
            product_mrp = offer_product.today_product_mrp
            amount = product_mrp*int(request.data['quantity'])
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer.save(price=amount))
            return Response(serializer.data, status=200)
        # IF PRODUCT NOT IN OFFER
        else:
            amount = item.product_mrp 
            amount = amount*int(request.data['quantity'])
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer.save(price=amount))
            return Response(serializer.data, status=200)


class ConfirmPaymentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    def post(self, request, *args, **kwargs):

        if not (request.user.active==True):
            return Response({"error": "User is not a customer"}, status=401)

        razorpay_payment_id = request.data.get('razorpay_payment_id', None)
        razorpay_order_id = request.data.get('razorpay_order_id', None)
        razorpay_signature = request.data.get('razorpay_signature', None)

        params_dict = {
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_order_id': razorpay_order_id,
            'razorpay_signature': razorpay_signature
        }

        try:
            user = User.objects.get(user=request.user)

            bag = Bag.objects.get(user=user, ordered=False)
        except:
            return Response({"message": "No such payment data found."}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user=user, bag=bag)
        order.name = request.data["name"]
        order.email = request.data["email"]
        order.phone = request.data["phone"]
        order.address = request.data["address"]
        order.landmark = request.data["landmark"]
        order.city = request.data["city"]
        order.state = request.data["state"]
        order.pincode = request.data["pincode"]
        order.order_accepted = True
        order.delivery_date=datetime.today() + timedelta(days=7)
        amount=0
        for i in bag:
            amount=amount+i.price
        order.total_amount = amount
        
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        try:
            client.utility.verify_payment_signature(params_dict)
        except:
            raise Exception('Razorpay Signature Verification Failed')

        bag.ordered = True
        bag.payment_id = razorpay_payment_id
        orderid=razorpay_order_id
        bag.save()
        if bag.item.count() != 0:
            for i in bag:
                product = Product.objects.get(id=i.item.id)
                product.quantity = product.quantity - bag.quantity
                if product.quantity == 0:
                    product.is_stock = False
                else:
                    product.is_stock = True
                product.save()
        order.save()
        user_payment = UserPayment.objects.create(user=user, order=order,paid=True,payment_date=order.order_date,amount_paid=order.total_amount)
        user_payment.save()
        user_orderd = OrderedBag.objects.create(user=user, name=order.name,bag=order.bag,phone=order.phone)
        user_orderd.save()
        if bag.item.count() != 0:
            OrderStatus.objects.create(Order=order, ordered=True,
                                        Tracking_Details="HHurrayy!! Your Order is successfully Placed")
        return Response({"message": "Payment Successful.. Your Order is Placed "}, status=status.HTTP_200_OK)