

from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.cache import cache_control
from accounts.models import Account
from carts.models import Cart
from carts.models import CartItem
from .models import Product, WishlistItem
from category.models import Category
from store.forms import ProductForm
from orders.models import banner
# from category.forms import category_form
from django.contrib import auth,messages
# from slugify import slugify
from django.utils.text import slugify
from django.core.paginator import Paginator
from carts.views import _cart_id
from django.db.models import Q 
from django.views.decorators.cache import cache_control
from django.http import Http404
# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def product_view(request,st,bname):
    user=request.user
    print(user.id)
    bookname=bname.replace('-',' ')
    cat =Category.objects.all()
    product_detail = Product.objects.filter(book_name__iexact=bookname).all()
    for i in product_detail:
        p_id =i.id
    
    try:
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product_id =p_id).exists()
    except:
        raise Http404()
    if not in_cart:
        try:
            in_cart = CartItem.objects.filter(Q(product_id=p_id)&Q(user=user)).exists()
        except:
            in_cart=False
    print(in_cart)
    try:
        if WishlistItem.objects.filter(user=request.user,product_id=p_id).exists():
            wish = True
        else:
            wish = False
    except:
        wish = False
    return render(request,'store/productview.html',{'product_detail': product_detail,'cat':cat,'in_cart':in_cart,'wish':wish,'pid':p_id})
def cat_view(request,slug):
  
    # cat =Category.objects.raw('SELECT id FROM category_category where category_name= %s',[slug])
    cat_active = Category.objects.values().filter(category_name__iexact=slug)
    
    print(cat_active)
    for i in cat_active:
        cat_id=i['id']
    product = Product.objects.filter(category_id=cat_id,is_active=True).all()
    cat = Category.objects.all()
    paginator = Paginator(product,6)
    page = request.GET.get('page')
    paged_products =paginator.get_page(page)
    try:
        bannerimg=banner.objects.get(is_selected=True)
    except:
        bannerimg=""
    return render(request,'landing.html',{'category':cat,'pro':paged_products,'cat_active':cat_active,'bannerimg':bannerimg,})
def cate(request):
    pass
def search(request):
    cat = Category.objects.all()
    if 'page' in request.GET:
        pa= request.GET['search']
        print(pa)
    else:
        print("not found")
    if 'search' in request.GET:
        keyword = request.GET['search']
        print("paged")
        if not keyword:
            keyword="xyz"
        if keyword:
            try:
                bannerimg=banner.objects.get(is_selected=True)
            except:
                bannerimg=""
            pro = Product.objects.order_by('book_name').filter(Q(book_name__icontains=keyword) |Q(author__icontains=keyword) ,is_active=True).order_by('id')
            """Quer splitted for use OR if you you , it is AND"""
            """{% if 'search in request.path %}"""
            for p in pro:
                print(p.is_active)
            paginator = Paginator(pro,6)
            page = request.GET.get('page')
            paged_products =paginator.get_page(page)
            messages.add_message(request, messages.INFO, 'searched')
            
    return render(request,'landing.html',{'pro':paged_products,'category':cat,'bannerimg':bannerimg,})

