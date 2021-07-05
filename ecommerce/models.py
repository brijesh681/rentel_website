from django.db import models
from core.models import *
import datetime

# Create your models here.
MODE_OF_PAYMENT_CHOICES = (
    
    ("Debit/Credit Card","Debit/Credit Card"),
    ("E-Wallet","E-Wallet"),
)
OFFER_TYPE = (
    ("Deals Of The Day", "Deals Of The Day"),
    ("Festive Special", "Festive Special"),
    ("Summer Collection", "Summer Collection"),
    ("Winter Collection", "Winter Collection"),
    ("As Seen Your Favourite", "As Seen Your Favourite"),
)


class Category(models.Model):
    # user = models.ForeignKey('core.User', on_delete=models.PROTECT)
    category_name = models.CharField(max_length=60)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.category_name)

    class Meta:
        verbose_name_plural = 'Add/View Product Category'


class Brand(models.Model):
    # user = models.ForeignKey('core.User', on_delete=models.PROTECT)
    brand_name = models.CharField(max_length=60)
    image = models.FileField(blank=True, upload_to="Ecommerce/Brand", null=True)
    logo_image = models.FileField(blank=True, upload_to="Ecommerce/Brand", null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.brand_name)

    class Meta:
        verbose_name_plural = 'Add/View Brands'


class Product(models.Model):
    #user = models.ForeignKey('core.User', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=80)
    product_image1 = models.FileField(blank=True, upload_to="Ecommerce/Clothes", null=True)
    product_image2 = models.FileField(blank=True, upload_to="Ecommerce/Clothes", null=True)
    product_image3 = models.FileField(blank=True, upload_to="Ecommerce/Clothes", null=True)
    product_image4 = models.FileField(blank=True, upload_to="Ecommerce/Clothes", null=True)
    product_image5 = models.FileField(blank=True, upload_to="Ecommerce/Clothes", null=True)

    product_mrp = models.IntegerField()
    rental_mrp = models.IntegerField()

    security_deposit = models.IntegerField(default=1000)

    color = models.CharField(max_length=20)
    material = models.CharField(max_length=20)
    neck_design = models.CharField(max_length=40)
    category = models.ManyToManyField(Category)
    brand = models.ManyToManyField(Brand)
    description = models.TextField(max_length=200, blank=True)
    designer = models.CharField(max_length=60, blank=True)

    small_size_available = models.BooleanField()
    small_size_length = models.IntegerField(blank=True, null=True)
    small_size_bust = models.IntegerField(blank=True, null=True)
    small_size_waist = models.IntegerField(blank=True, null=True)
    small_size_quantity = models.IntegerField(blank=True, null=True)

    medium_size_available = models.BooleanField(blank=True, null=True)
    medium_size_length = models.IntegerField(blank=True, null=True)
    medium_size_bust = models.IntegerField(blank=True, null=True)
    medium_size_waist = models.IntegerField(blank=True, null=True)
    medium_size_quantity = models.IntegerField(blank=True, null=True)

    large_size_available = models.BooleanField()
    large_size_length = models.IntegerField(blank=True, null=True)
    large_size_bust = models.IntegerField(blank=True, null=True)
    large_size_waist = models.IntegerField(blank=True, null=True)
    large_size_quantity = models.IntegerField(blank=True, null=True)

    extra_large_size_available = models.BooleanField()
    extra_large_size_length = models.IntegerField(blank=True, null=True)
    extra_large_size_bust = models.IntegerField(blank=True, null=True)
    extra_large_size_waist = models.IntegerField(blank=True, null=True)
    extra_large_size_quantity = models.IntegerField(blank=True, null=True)

    sleeves = models.BooleanField()
    in_stock = models.BooleanField()
    is_available_for_rent = models.BooleanField()
    is_available_for_sale = models.BooleanField()
    only_for_subscribed_user = models.BooleanField()
    date = models.DateField(auto_now_add=True)
    quantity = models.IntegerField(default=0)

    subscription_plan = models.ManyToManyField("core.SubscriptionPlans",null=True, blank=True,)

    def __str__(self):
        return str(self.product_name)

    class Meta:
        verbose_name_plural = 'Add/View Products'


class Accessories(models.Model):
    #user = models.ForeignKey('core.User', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=80)
    product_image1 = models.FileField(blank=True, upload_to="Ecommerce/Accessories", null=True)
    product_image2 = models.FileField(blank=True, upload_to="Ecommerce/Accessories", null=True)
    product_image3 = models.FileField(blank=True, upload_to="Ecommerce/Accessories", null=True)
    product_image4 = models.FileField(blank=True, upload_to="Ecommerce/Accessories", null=True)
    product_image5 = models.FileField(blank=True, upload_to="Ecommerce/Accessories", null=True)

    product_mrp = models.IntegerField()
    rental_mrp = models.IntegerField()
    security_deposit = models.IntegerField(default=1000)

    color = models.CharField(max_length=20)
    material = models.CharField(max_length=20, blank=True)
    neck_design = models.CharField(max_length=40, blank=True)
    free_size_length = models.IntegerField()
    free_size_weight = models.IntegerField()
    category = models.ManyToManyField(Category)
    brand = models.ManyToManyField(Brand)
    description = models.TextField(max_length=200, blank=True)
    designer = models.CharField(max_length=60, blank=True)
    in_stock = models.BooleanField()
    is_available_for_rent = models.BooleanField()
    is_available_for_sale = models.BooleanField()
    only_for_subscribed_user = models.BooleanField()
    date = models.DateField(auto_now_add=True)
    quantity = models.IntegerField(default=0)

    subscription_plan = models.ManyToManyField("core.SubscriptionPlans",null=True, blank=True,)

    def __str__(self):
        return str(self.product_name)

    class Meta:
        verbose_name_plural = 'Add/View Accessories'


class Wishlist(models.Model):
    user = models.ForeignKey('core.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True, blank=True)
    accessories = models.ForeignKey(Accessories, on_delete=models.CASCADE,null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class Review(models.Model):
    user = models.ForeignKey('core.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True, blank=True)
    accessories = models.ForeignKey(Accessories, on_delete=models.CASCADE,null=True, blank=True)
    image1 = models.FileField(blank=True, upload_to="Ecommerce/Review", null=True)
    image2 = models.FileField(blank=True, upload_to="Ecommerce/Review", null=True)
    image3 = models.FileField(blank=True, upload_to="Ecommerce/Review", null=True)
    image4 = models.FileField(blank=True, upload_to="Ecommerce/Review", null=True)
    image5 = models.FileField(blank=True, upload_to="Ecommerce/Review", null=True)
    image6 = models.FileField(blank=True, upload_to="Ecommerce/Review", null=True)
    review = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


SIZE = (
    ("S", "Small"),
    ("M", "Medium"),
    ("L", "Large"),
    ("XL", "Extra Large"),
)


class Bag(models.Model):
    user = models.ForeignKey('core.User', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)
    total_bill = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True, blank=True)
    accessories = models.ForeignKey(Accessories, on_delete=models.CASCADE,null=True, blank=True)
    total_cost = models.IntegerField(default=0)
    promocode = models.CharField(max_length=126,null=True)
    orderid = models.CharField(max_length=126,blank=True)
    ordered=models.BooleanField(default=False)
    payment_id = models.CharField(max_length=126,null=True,blank=True)
    single_product = models.BooleanField(default=False,null=True,blank=True)
    order_accepted = models.BooleanField(default=False)
    reorder = models.BooleanField(default=False)
    size = models.CharField(max_length=5, choices=SIZE, null=True, blank=True)
    quantity = models.IntegerField(default=1)




    def __str__(self):
        return str(self.user)

 

class DeliveryPincode(models.Model):
    pincode = models.IntegerField()
    available = models.BooleanField()


class Offer(models.Model):
    offer_type = models.CharField(max_length=25, choices=OFFER_TYPE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    accessories = models.ForeignKey(Accessories, on_delete=models.CASCADE,null=True, blank=True)
    today_rental_mrp = models.IntegerField()
    discount_percent = models.FloatField()
    only_for_subscribed_user = models.BooleanField()
    date = models.DateField(auto_now_add=True)



class Order(models.Model):

    user = models.ForeignKey('core.User',on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=34)
    phone = models.CharField(max_length = 13)
    country = models.CharField(max_length = 13) 
    state = models.CharField(max_length=25)
    city = models.CharField(max_length=25)
    pincode = models.CharField(max_length=25)
    address = models.CharField(max_length=50)
    landmark = models.CharField(max_length=50)
    mode = models.CharField(max_length=200, default="")
    received_by = models.CharField(max_length=200, default="",null=True,blank=True)
    delivery_time = models.TimeField(null=True,blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    order_date = models.DateTimeField(auto_now=True)
    bag = models.ForeignKey('Bag', on_delete=models.CASCADE, null=True)
    paid = models.BooleanField(default=False)
    price = models.IntegerField(default=0)
    MOP = models.CharField(max_length=200, null=True,blank=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.name) + "ordered" + str(self.Bag.id)

    

    """def user_item_removed(self,user):
        if Bag.objects.filter(user=user, active=True):
            bag = Bag.objects.get(user=user)
            order_instance = Order.objects.filter(
                user=User.objects.get(user=user).id)
            total = 0
            for i in order_instance:
                total = total + i.price
            bag.total_cost = total
            tax = 0.18 * bag.total_cost
            bag.total_bill = bag.total_cost + tax 
            bag.save()

    def user_cancel_order(self, user):
        if Bag.objects.filter(user=user, active=False):
            bag = Bag.objects.get(user=user)
            order_instance = Bag.objects.filter(
                user=User.objects.get(user=user).id)
            total = 0
            for i in order_instance:
                total = total + i.price
            bag.total_cost = total
            tax = 0.18 * bag.total_cost
            bag.total_bill = bag.total_cost + tax
            bag.save()"""
           
        


class OrderStatus(models.Model):
    
    Order=models.OneToOneField('Order',on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    packed = models.BooleanField(default=False)
    dispatched = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    Tracking_Details = models.TextField(default="",null=True)
    def __str__(self):
        return str(self.Order.id) + "status"




class UserPayment(models.Model):

    user=models.ForeignKey('core.User', on_delete=models.CASCADE)
    mode_of_payment=models.CharField(choices=MODE_OF_PAYMENT_CHOICES,max_length=50,default=" ",blank=True)
    amount_paid=models.IntegerField(default=0)
    payment_date=models.DateField(null=True,blank=True)
    invoice=models.FileField(upload_to='user/payment/invoice',null=True,blank=True)
    date=models.DateField(auto_now_add=True)
    paid=models.BooleanField(default=False)


    def __str__(self):
        return str(self.user.id) + " " +  self.user.fullname
        
    class Meta:
        verbose_name_plural = 'User Payment'





class OrderedBag(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('core.User', on_delete=models.CASCADE, null=True, blank=True)
    bag = models.ForeignKey(Bag, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=20,blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.bag)