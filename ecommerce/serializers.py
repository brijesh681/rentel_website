from rest_framework import serializers
from .models import *
from core.models import User
from django.core.exceptions import ObjectDoesNotExist


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = '__all__'


class CategoryNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['category_name']


class BrandNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ['brand_name']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    # user = serializers.ReadOnlyField(source='user.email')
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    url = serializers.HyperlinkedIdentityField(view_name="ecommerce:addviewproduct-detail")
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all(), many=True)

    class Meta:
        model = Product
        fields = '__all__'


class ViewAllProductSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    brand = BrandNameSerializer(read_only=True, many=True)
    url = serializers.HyperlinkedIdentityField(view_name="ecommerce:viewproductdetail-detail")

    class Meta:
        model = Product
        fields = ['id', 'url', 'product_name', 'product_image1', 'brand', 'rental_mrp', 'product_mrp']


class ProductDetailSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    category = CategoryNameSerializer(read_only=True, many=True)
    brand = BrandNameSerializer(read_only=True, many=True)
    small_size_available = serializers.SerializerMethodField(read_only=True)
    small_size_length = serializers.SerializerMethodField(read_only=True)
    small_size_bust = serializers.SerializerMethodField(read_only=True)
    small_size_waist = serializers.SerializerMethodField(read_only=True)
    medium_size_available = serializers.SerializerMethodField(read_only=True)
    medium_size_length = serializers.SerializerMethodField(read_only=True)
    medium_size_bust = serializers.SerializerMethodField(read_only=True)
    medium_size_waist = serializers.SerializerMethodField(read_only=True)
    large_size_available = serializers.SerializerMethodField(read_only=True)
    large_size_length = serializers.SerializerMethodField(read_only=True)
    large_size_bust = serializers.SerializerMethodField(read_only=True)
    large_size_waist = serializers.SerializerMethodField(read_only=True)
    extra_large_size_available = serializers.SerializerMethodField(read_only=True)
    extra_large_size_length = serializers.SerializerMethodField(read_only=True)
    extra_large_size_bust = serializers.SerializerMethodField(read_only=True)
    extra_large_size_waist = serializers.SerializerMethodField(read_only=True)
    in_stock = serializers.SerializerMethodField(read_only=True)
    is_available_for_rent = serializers.SerializerMethodField(read_only=True)
    is_available_for_sale = serializers.SerializerMethodField(read_only=True)
    review = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def get_small_size_available(self, obj):
        if not obj.small_size_available:
            return 'Size Not Available'
        return True

    def get_small_size_length(self, obj):
        if obj.small_size_available:
            return obj.small_size_length
        return 'Size Not Available'

    def get_small_size_bust(self, obj):
        if obj.small_size_available:
            return obj.small_size_bust
        return 'Size Not Available'

    def get_small_size_waist(self, obj):
        if obj.small_size_available:
            return obj.small_size_waist
        return 'Size Not Available'

    def get_medium_size_available(self, obj):
        if not obj.medium_size_available:
            return 'Size Not Available'
        return True

    def get_medium_size_length(self, obj):
        if obj.medium_size_available:
            return obj.medium_size_length
        return 'Size Not Available'

    def get_medium_size_bust(self, obj):
        if obj.medium_size_available:
            return obj.medium_size_bust
        return 'Size Not Available'

    def get_medium_size_waist(self, obj):
        if obj.medium_size_available:
            return obj.medium_size_waist
        return 'Size Not Available'

    def get_large_size_available(self, obj):
        if not obj.large_size_available:
            return 'Size Not Available'
        return True

    def get_large_size_length(self, obj):
        if obj.large_size_available:
            return obj.large_size_length
        return 'Size Not Available'

    def get_large_size_bust(self, obj):
        if obj.large_size_available:
            return obj.large_size_bust
        return 'Size Not Available'

    def get_large_size_waist(self, obj):
        if obj.large_size_available:
            return obj.large_size_waist
        return 'Size Not Available'

    def get_extra_large_size_available(self, obj):
        if not obj.extra_large_size_available:
            return 'Size Not Available'
        return True

    def get_extra_large_size_length(self, obj):
        if obj.extra_large_size_available:
            return obj.extra_large_size_length
        return 'Size Not Available'

    def get_extra_large_size_bust(self, obj):
        if obj.extra_large_size_available:
            return obj.extra_large_size_bust
        return 'Size Not Available'

    def get_extra_large_size_waist(self, obj):
        if obj.extra_large_size_available:
            return obj.extra_large_size_waist
        return 'Size Not Available'

    def get_in_stock(self, obj):
        if obj.in_stock:
            return True
        return 'Out of Stock'

    def get_is_available_for_rent(self, obj):
        if obj.is_available_for_rent:
            return True
        return 'This item is not available for rent'

    def get_is_available_for_sale(self, obj):
        if obj.is_available_for_rent:
            return True
        return 'This item is not available for sale'

    def get_review(self, obj):
        try:
            detail = Review.objects.filter(product=obj.id)
        except ObjectDoesNotExist:
            return None
        serializer = ReviewSerializer(detail, many=True)
        return serializer.data


class AddOfferSerializer(serializers.ModelSerializer):
    today_rental_mrp = serializers.ReadOnlyField()

    class Meta:
        model = Offer
        fields = '__all__'


class ViewAllOfferSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    product = ViewAllProductSerializer()
    url = serializers.HyperlinkedIdentityField(view_name="ecommerce:viewofferdetail-detail")

    class Meta:
        model = Offer
        fields = '__all__'


class OfferDetailSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    product = ProductDetailSerializer()

    class Meta:
        model = Offer
        fields = '__all__'


class AddAccessoriesSerializer(serializers.ModelSerializer):
    # # user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Accessories
        fields = '__all__'


class ViewAllAccessoriesSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    brand = BrandNameSerializer(read_only=True, many=True)
    url = serializers.HyperlinkedIdentityField(view_name="ecommerce:viewaccessoriesdetail-detail")

    class Meta:
        model = Accessories
        fields = ['id', 'url', 'product_name', 'product_image1', 'brand', 'rental_mrp', 'product_mrp']


class AccessoriesDetailSerializer(serializers.ModelSerializer):
    category = CategoryNameSerializer(read_only=True, many=True)
    brand = BrandNameSerializer(read_only=True, many=True)
    in_stock = serializers.SerializerMethodField(read_only=True)
    is_available_for_rent = serializers.SerializerMethodField(read_only=True)
    is_available_for_sale = serializers.SerializerMethodField(read_only=True)
    review = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Accessories
        fields = '__all__'

    def get_in_stock(self, obj):
        if obj.in_stock:
            return True
        return 'Out of Stock'

    def get_is_available_for_rent(self, obj):
        if obj.is_available_for_rent:
            return True
        return 'This item is not available for rent'

    def get_is_available_for_sale(self, obj):
        if obj.is_available_for_rent:
            return True
        return 'This item is not available for sale'

    def get_review(self, obj):
        try:
            detail = Review.objects.filter(product=obj.id)
        except ObjectDoesNotExist:
            return None
        serializer = ReviewSerializer(detail, many=True)
        return serializer.data


class CheckDeliveryPincodeSerializer(serializers.ModelSerializer):
    available = serializers.ReadOnlyField()

    class Meta:
        model = DeliveryPincode
        fields = '__all__'


class WishlistSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    # # user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Wishlist
        fields = '__all__'


class ViewMyWishlistSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    user = serializers.ReadOnlyField(source='user.email')
    product = ViewAllProductSerializer()

    class Meta:
        model = Wishlist
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Review
        fields = '__all__'


class BagProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['product_name', 'product_image1', 'product_mrp', 'rental_mrp', 'security_deposit']


class AddToBagSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    # # user = serializers.ReadOnlyField(source='user.username')
    total_amount = serializers.ReadOnlyField()

    class Meta:
        model = Bag
        fields = '__all__'


class ViewMyBagSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    url = serializers.HyperlinkedIdentityField(view_name="ecommerce:editbag-detail")
    user = serializers.ReadOnlyField(source='user.email')
    product = BagProductSerializer(read_only=True)

    class Meta:
        model = Bag
        fields = '__all__'


class EditBagSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    product = BagProductSerializer(read_only=True)
    total_amount = serializers.ReadOnlyField()
    size = serializers.ReadOnlyField()

    class Meta:
        model = Bag
        fields = '__all__'




