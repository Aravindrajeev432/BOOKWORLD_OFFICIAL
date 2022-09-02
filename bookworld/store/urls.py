from django.urls import URLPattern, path
from . import views
urlpatterns = [
    # path('',views.product_view,name="productview"),
    
    path('category/<slug:st>/<slug:bname>',views.product_view,name="product_view"),
    path('category/<str:slug>',views.cat_view,name='cat_view'),
    path('category/',views.cate,name='cate_view'),
    path('search/',views.search,name='search'),
    
    
    
]