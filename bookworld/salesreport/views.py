from cgi import print_arguments
from datetime import date
from multiprocessing import context
from unicodedata import category
from django.shortcuts import render,redirect
from orders.models import Payment
from orders.models import Order
from store.models import Product,Coupon
from orders .models import OrderProduct
from django.db.models import Sum,Count
from datetime import datetime
from django.views.decorators.cache import cache_control
# Create your views here.
# def salespage(request,*args, **kwargs):
#     if 'admin' not in request.session:
#         return redirect('home')
       
#     # print(kwargs)
#     sales= OrderProduct.objects.annotate(qty=Sum('quantity')).order_by('product_id')
#     salesobj= OrderProduct.objects.filter().annotate(qty=Sum('quantity'))
#     print(sales)
    
#     print("---------")
#     # for i in sales:
#     #     print(i)
#     print(salesobj)
#     print("-----------")
#     # for i in salesobj:
#     #     print("------")
#     #     print(i.product_id)
#     #     print(i.product.book_name)
#     #     print(i.qty)
#     # products=[]
#     # pro={}
#     # for i in sales:
#     #     # print(i['product_id'])
#     #     pid=i['product_id']
#     #     k=Product.objects.get(id=pid)
#     #     print(k.category.category_name)
#     #     # print(k.book_name)
        
#     #     pro={'id':pid,'book_name':k.book_name,'price':k.price,'category':k.category.category_name}
#     #     # print(pro)
#     #     products.append(pro)
#     # # products= Product.objects.all()
#     # print(products)
#     # # for i in products:
#     # #     print(i['id'])
    
#     #order_cat_graph = OrderProduct.objects.filter().values('product_id').order_by('quantity').annotate(count=Count('product_id'))
#     context= {
#         'sales':sales,
#         # 'product_details':products,
#     }
#     return render(request,'admin/sales_report.html',context)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def salespage(request,*args, **kwargs):
    print("createpdf page")
    
    if 'admin' not in request.session:
        return redirect('home')
    
    # test_pay= Payment.objects.aggregate(Sum(float('amount_paid')))
    # print(test_pay)
    
    
    products = Product.objects.all()
    

        #order_cat_graph = OrderProduct.objects.filter().values('product_id').order_by('quantity').annotate(count=Count('product_id'))
    dates_date =OrderProduct.objects.values('created_at__date').distinct().order_by('created_at__date')
    
   
    dates=[]
    for dd in dates_date:
        
       
        dates.append(dd['created_at__date'].strftime("%Y-%m-%d"))
    
    try:
            
        dates_max=dates[-1]
        salesdate=dates[-1]
    except:
        dates_max=''
        salesdate=''
    current_date =dates_max
    dates_len =len(dates)
    print("********")
    dates_len-=dates_len
    print(dates_len)
    # last_date_day = OrderProduct.objects.latest('created_at')
    # d=last_date_day.created_at
    # print(d.year)
    print("dddddddd")
    try:
        sales = OrderProduct.objects.filter(created_at__date=dates[-1]).values('product_id').annotate(qty=Sum('quantity'))
        grandtotalfind=OrderProduct.objects.filter(created_at__date=dates[-1]).all()
        print(grandtotalfind)
        total_without_discount=0
        print("discount")
        total_after_coupon_discount=0
        total_after_coupon=Order.objects.filter(created_at__date=dates[-1]).all()
        for t_a_c in total_after_coupon:
                
                try:
                    total_after_coupon_discount+=t_a_c.coupon.discount
                    
                except:
                    pass
        print(total_after_coupon)
        for t in grandtotalfind:
            total_without_discount+=(t.product.price)*(t.quantity)
            print(t.product.price)
     
            
    except:
        sales=[]
    # get total money earned in day qty*productprice
        try:
            total_earn= Payment.objects.filter(created_at=dates[-1]).aggregate(Sum('amount_paid'))
        except:
            pass
    try:
                
              total_earn= Payment.objects.filter(created_at=salesdate).all()
              total=0
              for t in total_earn:
                total+=float(t.amount_paid)
              print("total")
              print(total)
    except:
            total="calculating"
    if request.method=="POST":
        try:
            salesdate =request.POST['salesdate']
            print("Ssssss")
            print(salesdate)
        
            # sales= OrderProduct.objects.annotate(qty=Sum('quantity')).order_by('product_id')
            sales = OrderProduct.objects.filter(created_at__date=salesdate).values('product_id').annotate(qty=Sum('quantity'))
            grandtotalfind=OrderProduct.objects.filter(created_at__date=salesdate).all()
            print(grandtotalfind)
            total_without_discount=0
            total_after_coupon_discount=0
            total_after_coupon=Order.objects.filter(created_at__date=salesdate).all()
            for t_a_c in total_after_coupon:
                
                try:
                    total_after_coupon_discount+=t_a_c.coupon.discount
                    
                except:
                    pass
            print(total_after_coupon)
            for t in grandtotalfind:
                total_without_discount+=(t.product.price)*(t.quantity)
                print(t.product.price)
            
            
            print(sales)
            for s in sales:
                    pass
            current_date=salesdate
        except KeyError:
            pass
            salesdate=dates_max
      
        try:
              total_earn= Payment.objects.filter(created_at=salesdate).all()
              total=0
              for t in total_earn:
                total+=float(t.amount_paid)
              print("total")
              print(total)
        except:
            total="calculating"
    context= {
      'dates':dates,
      'dates_max':dates_max,
      'current_date':current_date,
      'sales':sales,
        'products':products,
        'salesdate':salesdate,
        'total':total,
        'total_without_discount':total_without_discount,
        'total_after_coupon_discount':total_after_coupon_discount,

    }
    return render(request,'admin/sales_report.html',context)