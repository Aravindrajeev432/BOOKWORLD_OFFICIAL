from unicodedata import name
from urllib import request
from django.urls import URLPattern, path
from . import views
urlpatterns = [
    path('login',views.adminlogin,name="adminlogin"),
    path('logout',views.logout,name='adminlogout'),
    
    path('dashboard',views.dashboard,name="dashboard"),
    #product management
    path('products',views.products,name='products'),
    path('addnewbook',views.addnewbook,name="addnewbook"),
    path('addnewbooktest',views.addnewbooktest,name="addnewbooktest"),
    path('edit_book/<int:id>',views.edit_book,name="editbook"),
    path('unblock_book/<int:id>',views.unblock_book,name='unblock_book'),
    path('block_book/<int:id>',views.block_book,name="block_book"),
    path('delete_book/<int:id>',views.delete_book,name="deletebook"),  
    #category management
    path('category_management',views.category_management,name="addnewcategory"),
    path('delete_cat/<int:id>',views.delete_cat,name='delete_cat'),
  
    #user management
    path('users',views.users,name="usersview"),
    path('edit_user/<int:id>',views.edit_user,name='block_unblock'),
    path('block_user/<int:id>',views.block_user,name='block_user'),
    path('unblock_user/<int:id>',views.unblock_user,name='unblock_user'),
    path('delete_user/<int:id>',views.delete_user,name='delete_user'),
    #order management
    path('order_management',views.order_management,name='order_management'),
    path('orders_page/change_order_status/<int:order_number>/<str:status>',views.change_order_status,name="order_status_change"),
    path('orders_page/<int:order_number>',views.orders_page,name='orders_page'),
    path('create-pdf', views.pdf_report_create, name='create-pdf'),
    path('export_excel',views.export_excel,name='export_excel'),
    path('export_excel_year',views.export_excel_year,name='export_excel_year'),    
    path('check-pdf',views.pdf_check,name="pdfcheck"),
    path('invoice/<int:order_number>',views.invoice,name="invoice_admin"),
    #offer management
    path('offer_management',views.offer_management,name='offer_management'),
    path('offer_management_productsview',views.offer_management_productsview,name="offer_management_productsview"),
    path('offer_management_product/<int:bid>',views.offer_management_product,name="offer_management_product"),
    path('offer_management_categoryview',views.offer_management_categoryview,name='offer_management_categoryview'),
    path('offer_management_category/<int:cid>',views.offer_management_category,name='offer_management_category'),
    path('returns',views.returns,name='returns'),
    #opid-orderproductid
    #Return management
    path('return_order_admin/<int:opid>',views.return_order_admin,name='return_order_admin'),
    #coupon management
    path('offer_management_couponview',views.offer_management_couponview,name="offer_management_couponview"),
    path('addnew_coupon',views.addnew_coupon,name="addnew_coupon"),
    path('coupon_view/<int:id>',views.coupon_view,name='coupon_view'),
    #Banner Management
    path('banners',views.banners,name='banners'),
    path('banner_select/<int:id>',views.banner_select,name='banner_select'),
    path('add_banner',views.add_banner,name='add_banner'),
    path('remove_banner/<int:id>',views.remove_banner,name='remove_banner'),

    
    
            ]