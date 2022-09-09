"""bookworld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from cgitb import handler
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from bookworld.settings import MEDIA_ROOT
from django.conf.urls import handler404
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('home',views.index,name="home"),
    path('account/',include('accounts.urls')),
    # path('homepage',views.homepage,name="home"),
    path('admins/',include('admins.urls')),
    path('product/',include('store.urls')),
    path('cart/',include('carts.urls')),
    path('orders/',include('orders.urls')),
    path('profile/<int:id>',views.profile,name='profile'),
    path('editprofile/<int:id>',views.editprofile,name='editprofile'),
    path('add_address/<int:id>',views.add_address,name='add_address'),
    path('sales_report/',include('salesreport.urls')),
    path('wishlist',views.wishlist,name="wishlist"),
    path('addwishlist/<int:pid>',views.addwishlist,name="addwishlist"),
    path('removewishlist/<int:pid>',views.removewishlist,name="removewishlist")
    

]+static(settings.MEDIA_URL,document_root=MEDIA_ROOT)

handler404='notfoundhandler.views.error_404'