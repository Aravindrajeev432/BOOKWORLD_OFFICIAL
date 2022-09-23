from django.urls import path
from . import views
urlpatterns = [
    # path('',views.product_view,name="productview"),
    
    path('place_order/',views.place_order,name='place_order'),
    path('review_checkout/',views.review_checkout,name='review_checkout'),
    path('payment/<int:order_number>/<int:order_id>/<int:total>',views.payment,name='payment'),
    path('payment_paypal',views.payment_paypal,name='payment_paypal'),
    path('payment_razorpay',views.payment_razorpay,name='payment_razorpay'),
    path('place_order/paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('checkout_success',views.checkout_success,name="checkout_success"),
    # path('place_order/<str:pay>',views.payment,name='payments'),
    path("checkout_fail", views.checkout_fail, name="checkout_fail"),
    path('order_history',views.order_history,name="order_history"),
    path('cancel_order/<int:oid>',views.cancel_order,name='cancel_order'),
    path('return_order/<int:oid>',views.return_order,name='return_order'),
    path('order_success',views.order_succes,name='order_success'),
    path('order_history/orders_page/<int:order_number>',views.orders_page,name="orders_page_user"),
    path('invoice_user/<int:order_number>',views.invoice,name="invoice_user"),
]