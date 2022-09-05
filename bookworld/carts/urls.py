from django.urls import URLPattern, path
from . import views 
urlpatterns = [
    
    path('',views.cart,name="cart"),
    path('add_cart/<int:product_id>',views.add_cart,name='add_cart'),
    path('add_cart_from_cart/<int:product_id>',views.add_cart_from_cart,name="add_cart_from_cart"),
    path('remove_cart/<int:product_id>/',views.remove_cart,name='remove_cart'),
    path('remove_cart_from_cart/<int:product_id>',views.remove_cart_from_cart,name="remove_cart_from_cart"),
    path('delete_cart/<int:product_id>/',views.delete_cart,name='delete_cart'),
    path('checkout/',views.checkout,name="checkout"),
    path('cart_total_finder/<int:id>',views.cart_total_finder,name='cart_total_finder'),
    path('couponCheck/<str:coupon>',views.couponCheck,name="couponCheck"),
]