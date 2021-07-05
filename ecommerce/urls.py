from django.urls import path, include
from rest_framework import routers
from ecommerce import views

app_name = 'ecommerce'

router = routers.DefaultRouter()

router.register('add-view-category', views.CategoryViewSet, basename='addviewcategory')
router.register('add-view-brand', views.BrandViewSet, basename='addviewbrand')

# ADD PRODUCT
router.register('admin-add-view-product', views.ProductViewSet, basename='addviewproduct')
# View ALL PRODUCT
router.register('home-view-all-product', views.ViewAllProductViewSet, basename='homeviewallproduct')
# PRODUCT DETAIL
router.register('view-product-detail', views.ProductDetailViewSet, basename='viewproductdetail')

# ADD OFFER
router.register('admin-add-view-offer', views.AddOfferViewSet, basename='addviewoffer')
router.register('view-offer-detail', views.OfferDetailViewSet, basename='viewofferdetail')

# DEALS OF THE DAY
router.register('home-view-all-deals-of-day', views.ViewAllDealsOfTheDayViewSet, basename='homeviewalldealsofday')
# FESTIVE SPECIAL
router.register('home-view-all-festive-special', views.ViewAllFestiveSpecialViewSet, basename='homeviewallfestivespecial')
# SUMMER COLLECTION
router.register('home-view-all-summer-collection', views.ViewAllSummerCollectionViewSet, basename='homeviewallsummercollection')
# WINTER COLLECTION
router.register('home-view-all-winter-collection', views.ViewAllWinterCollectionViewSet, basename='homeviewallwintercollection')
# AS SEEN YOUR FAVOURITE
router.register('home-view-all-favourite', views.ViewAllFavouriteViewSet, basename='homeviewallfavourite')
# SUBSCRIBED USER PRODUCTS
router.register('home-view-all-subscribed-user-product', views.ViewAllSubscribedUserProductViewSet, basename='homeviewallsubscribeduserproduct')
# ACCESSORIES
router.register('admin-add-view-accessories', views.AddAccessoriesViewSet, basename='addviewaccessories')
router.register('home-view-all-accessories', views.ViewAllAccessoriesViewSet, basename='homeviewallaccessories')
router.register('view-accessories-detail', views.AccessoriesDetailViewSet, basename='viewaccessoriesdetail')

# CHECK DELIVERY PIN CODE
router.register('check-delivery-pincode', views.CheckDeliveryPincodeViewSet, basename='checkdeliverypincode')

# WISHLIST
router.register('view-add-to-wishlist', views.WishlistViewSet, basename='addviewwishlist')
# REVIEW
router.register('add-review', views.ReviewViewSet, basename='addviewreview')

# ADD TO BAG
router.register('view-add-to-bag', views.AddToBagViewSet, basename='addtobag')
router.register('edit-bag', views.EditBagViewSet, basename='editbag')

urlpatterns = [
    path('', include(router.urls)),
    

]
