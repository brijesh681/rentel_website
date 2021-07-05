from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import viewsets, permissions, generics
from rest_framework.views import exception_handler
from rest_framework.response import Response
from .serializers import *
from core.permissions import *
from core.models import User
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
import  datetime
# from .filter import *


class ProductPagination(PageNumberPagination):
    page_size = 7


class CategoryViewSet(viewsets.ModelViewSet):
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


class BrandViewSet(viewsets.ModelViewSet):
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


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    http_method_names = ['post', 'options', 'head']

    def create(self, request, *args, **kwargs):
        if Product.objects.filter(product_name=self.request.data.get('product_name'), user=self.request.user).exists():
            return Response({"ALREADY_EXIST": "Product Already Exists"}, status=400)

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(
            serializer.save()
        )
        return Response(serializer.data, status=200)


class ViewAllProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().order_by('-date')
    serializer_class = ViewAllProductSerializer
    pagination_class = ProductPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductDetailViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AddOfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = AddOfferSerializer
    pagination_class = ProductPagination
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    http_method_names = ['post', 'options', 'head']

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

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(
            serializer.save(today_rental_mrp=total_rental_selling_mrp)
        )
        return Response(serializer.data, status=200)


class OfferDetailViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ViewAllDealsOfTheDayViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Offer.objects.filter(offer_type="Deals Of The Day").order_by('-date')
    serializer_class = ViewAllOfferSerializer
    # pagination_class = ProductPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ViewAllFestiveSpecialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Offer.objects.filter(offer_type="Festive Special").order_by('-date')
    serializer_class = ViewAllOfferSerializer
    pagination_class = ProductPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ViewAllSummerCollectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Offer.objects.filter(offer_type="Summer Collection").order_by('-date')
    serializer_class = ViewAllOfferSerializer
    pagination_class = ProductPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ViewAllWinterCollectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Offer.objects.filter(offer_type="Winter Collection").order_by('-date')
    serializer_class = ViewAllOfferSerializer
    pagination_class = ProductPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ViewAllFavouriteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Offer.objects.filter(offer_type="As Seen Your Favourite").order_by('-date')
    serializer_class = ViewAllOfferSerializer
    pagination_class = ProductPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ViewAllSubscribedUserProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(only_for_subscribed_user=True).order_by('-date')
    serializer_class = ViewAllProductSerializer
    # pagination_class = ProductPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AddAccessoriesViewSet(viewsets.ModelViewSet):
    queryset = Accessories.objects.all()
    serializer_class = AddAccessoriesSerializer
    pagination_class = ProductPagination
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    http_method_names = ['post', 'options', 'head']

    def create(self, request, *args, **kwargs):
        if Accessories.objects.filter(product_name=self.request.data.get('product_name')).exists():
            return Response({"ALREADY_EXIST": "Product Already Exists"}, status=400)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer.save())
        return Response(serializer.data, status=200)


class ViewAllAccessoriesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Accessories.objects.all()
    serializer_class = ViewAllAccessoriesSerializer
    pagination_class = ProductPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AccessoriesDetailViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Accessories.objects.all()
    serializer_class = AccessoriesDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class WishlistViewSet(viewsets.ModelViewSet):
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
            serializer = ViewMyWishlistSerializer(queryset, many=True, context={'request': request})
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


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    http_method_names = ['post', 'head', 'options']

    def create(self, request, *args, **kwargs):
        if Review.objects.filter(product=request.data.get('product'), user=self.request.user).exists():
            return Response({"ALREADY_EXIST": "Already have a review"}, status=400)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer.save(user=request.user))
        return Response(serializer.data, status=200)


class CheckDeliveryPincodeViewSet(viewsets.ModelViewSet):
    queryset = DeliveryPincode.objects.all()
    serializer_class = CheckDeliveryPincodeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if DeliveryPincode.objects.filter(pincode=request.data.get('pincode'), available=True).exists():
            return Response({"DELIVERY_AVAILABLE": "Delivery Available"}, status=200)
        else:
            return Response({"DELIVERY_NOT_AVAILABLE": "Delivery Not Available"}, status=400)


class AddToBagViewSet(viewsets.ModelViewSet):
    queryset = Bag.objects.all()
    serializer_class = AddToBagSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def list(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=request.user.id)
        except ObjectDoesNotExist:
            return Response({"DOES_NOT_EXIST": "User Does not exist"}, status=400)

        queryset = self.queryset.filter(user=user)
        if queryset.exists():
            serializer = ViewMyBagSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data, status=200)
        else:
            return Response({"NO_ITEM": "Empty Bag"}, status=400)

    def create(self, request, *args, **kwargs):
        # CHECK PRODUCT
        try:
            product = Product.objects.get(id=request.data.get('product'))
        except ObjectDoesNotExist:
            return Response({"DOES_NOT_EXIST": "Product Does not exist"}, status=400)
        # CHECK ITEM NOT ALREADY EXISTS
        if Bag.objects.filter(product=product, user=request.user).exists():
            return Response({"ALREADY_EXIST": "Item Already Exists in Bag"}, status=400)

        # IF PRODUCT IN OFFER
        if Offer.objects.filter(product=product).exists():
            offer_product = Offer.objects.get(product=product)
            product_rental_mrp = offer_product.today_rental_mrp
            product_security_deposite = product.security_deposit
            total_amount = product_rental_mrp + product_security_deposite

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer.save(total_amount=total_amount))
            return Response(serializer.data, status=200)
        # IF PRODUCT NOT IN OFFER
        else:
            total_amount = product.rental_mrp + product.security_deposit
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer.save(total_amount=total_amount))
            return Response(serializer.data, status=200)


class EditBagViewSet(viewsets.ModelViewSet):
    queryset = Bag.objects.all()
    serializer_class = EditBagSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]


