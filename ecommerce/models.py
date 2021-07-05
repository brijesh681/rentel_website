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
PRODUCT_SIZE_CHOICES = (
    ("S","S"),
    ("M","M"),
    ("L","L"),
)

class Category(models.Model):
    # user = models.ForeignKey('core.User', on_delete=models.PROTECT)
    category_name = models.CharField(max_length=60)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.category_name)

    class Meta:
        verbose_name_plural = 'Category'


class Brand(models.Model):
    # user = models.ForeignKey('core.User', on_delete=models.PROTECT)
    brand_name = models.CharField(max_length=60)
    image = models.FileField(blank=True, upload_to="Ecommerce/Brand", null=True)
    logo_image = models.FileField(blank=True, upload_to="Ecommerce/Brand", null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.brand_name)

    class Meta:
        verbose_name_plural = 'Brands'


class Product(models.Model):
    #user = models.ForeignKey('core.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    product_image1 = models.FileField(blank=True, upload_to="Ecommerce/images/", )
    product_image2 = models.FileField(blank=True, upload_to="Ecommerce/images/", )
    product_image3 = models.FileField(blank=True, upload_to="Ecommerce/images/", )
    product_image4 = models.FileField(blank=True, upload_to="Ecommerce/images/", )
    product_image5 = models.FileField(blank=True, upload_to="Ecommerce/images", )
    product_mrp = models.IntegerField()
    rental_mrp = models.IntegerField()
    security_deposit = models.IntegerField(default=1000)
    color = models.CharField(max_length=20)
    material = models.CharField(max_length=20)
    neck_design = models.CharField(max_length=40)
    category = models.ManyToManyField("Category",blank=True)
    brand = models.ManyToManyField("Brand",blank=True,)
    description = models.TextField(max_length=200, blank=True)
    designer = models.CharField(max_length=60, blank=True)
    sleeves = models.BooleanField(default=False)
    is_stock = models.BooleanField(default=True)
    is_available_for_rent = models.BooleanField()
    is_active = models.BooleanField(default=False)
    is_available_for_sale = models.BooleanField()
    only_for_subscribed_user = models.BooleanField()
    date = models.DateField(auto_now_add=True)
    quantity = models.IntegerField(default=0)
   # rent = models.BooleanField(default=False)
    size = models.CharField(max_length=255, choices=PRODUCT_SIZE_CHOICES, null=True, blank=True)

    subscription_plan = models.ManyToManyField("core.SubscriptionPlans",blank=True,)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = 'Products'





class Wishlist(models.Model):
    user = models.ForeignKey('core.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class Review(models.Model):
    user = models.ForeignKey('core.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True, blank=True)
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
    item = models.ForeignKey('ecommerce.Product', on_delete=models.CASCADE,null=True, blank=True)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)
    rent = models.BooleanField(default=False)
    ordered=models.BooleanField(default=False)
    orderid = models.CharField(max_length=126,blank=True)
    ordered=models.BooleanField(default=False)
    payment_id = models.CharField(max_length=126,null=True,blank=True)
    #active = models.BooleanField(default=True)



    def __str__(self):
        return str(self.id)+"  "+str(self.user)


 

class DeliveryPincode(models.Model):
    pincode = models.IntegerField()
    available = models.BooleanField()


class Offer(models.Model):
    offer_type = models.CharField(max_length=25, choices=OFFER_TYPE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    today_rental_mrp = models.IntegerField()
    today_product_mrp = models.IntegerField()
    discount_percent = models.FloatField()
    only_for_subscribed_user = models.BooleanField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.offer_type)+" "+str(self.id)

class Order(models.Model):

    user = models.ForeignKey('core.User',on_delete=models.CASCADE)
    name = models.CharField(max_length=50,null=True,blank=True)
    email = models.EmailField(max_length=34,null=True,blank=True)
    phone = models.CharField(max_length = 13,null=True,blank=True)
    state = models.CharField(max_length=25,null=True,blank=True)
    city = models.CharField(max_length=25,null=True,blank=True)
    pincode = models.CharField(max_length=25,null=True,blank=True)
    address = models.CharField(max_length=50,null=True,blank=True)
    landmark = models.CharField(max_length=50,null=True,blank=True)
    quantity = models.IntegerField(default=1)
    total_amount = models.IntegerField(default=0)
    order_cancel = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    bag = models.ForeignKey('ecommerce.Bag',on_delete=models.CASCADE,null=True,blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    order_date = models.DateTimeField(auto_now=True)
    order_accepted = models.BooleanField(default=False)
    def __str__(self):
        return str(self.name) + "ordered" + str(self.Bag.id)

    

           
        


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
    amount_paid=models.IntegerField(default=0)
    payment_date=models.DateField(null=True,blank=True)
    invoice=models.FileField(upload_to='user/payment/invoice',null=True,blank=True)
    date=models.DateField(auto_now_add=True)
    paid=models.BooleanField(default=False)
    order =models.ManyToManyField("Order") 

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