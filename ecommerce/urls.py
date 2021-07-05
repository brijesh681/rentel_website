from django.urls import path, include
from .views import *

app_name = 'ecommerce'

urlpatterns = [

   # Bag related APIs

    path('additem_buy/',AddtoBuyBagView.as_view()),      # add item for buy in bag

    path('additem_rent/',AddtoRentBagView.as_view()),    # add item for rent in bag

    path('bag_view/', BagView.as_view()),                # view bag

    path('bag_view/<int:id>/', BagUpdateView.as_view()), #  bag update or delete item


    # Product Related APIs

    path('product/',AllProductView.as_view()),           # view all product 

    path('product_create/', ProductCreate.as_view()),    # create product here

    path('productDetail/<int:id>/',ProductDetailAPI.as_view()), # view product detail

    path('product/<int:id>/',ProductUpdateAPI.as_view()),  # product update or delete

    # Review Related API

    path('review/',ReviewAPIView.as_view()),  # Review create or list

    # Wishlist Related API

    path('addwishlist/',WishlistAPIView.as_view()),  # Review create or list

    path('delete_wishlit_item/<int:id>/',MyWishlistAPIView.as_view()),  # Review create or list

    # Delievery related API

    path('create_delevery_pincode/',CreateDeliveryPincodeAPIView.as_view()),  # Create delievery pincode 

    path('check_delevery_pincode/',CheckDeliveryPincodeAPIView.as_view()),  # Check delievery pincode 

    # Offer related APIs

    path('add_offer/',AddOfferAPIView.as_view()),  # Add offers api

    path('offer_details/',OfferDetailAPIView.as_view()),  # Check offer details 

    path('offer_deals_of_the_day/',ViewAllDealsOfTheDayAPIView.as_view()),  # offer deals of the day api 

    path('offer_festive_special/',ViewAllFestiveSpecialAPIView.as_view()),  # offer festive spacial

    path('offer_summer_collection/',ViewAllSummerCollectionAPIView.as_view()),  # offer summer collection

    path('offer_winter_collection/',ViewAllWinterCollectionAPIView.as_view()),  # offer winter collection

    # Category 

    path('add_category/',CategoryAPIView.as_view()),  # Category list or create api view

    path('add_category/<int:id>/',CategoryUpdateAPIView.as_view()),  # Categoryupdate delete retrieve
    
    # Brand

    path('add_brand/',BrandAPIView.as_view()), # Brand list or create api view

    path('add_brand/<int:id>/',BrandUpdateAPIView.as_view()),  # Brand update delete retrieve


    #order

    path('order_payment/',ConfirmPaymentAPIView.as_view()), # order create or payment













    

]
