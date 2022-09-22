
from calendar import month
from datetime import date
from operator import concat

from django.shortcuts import render,redirect
from admins.views import dashboard
from orders.models import Payment
from orders.models import Order
from store.models import Product,Coupon
from orders .models import OrderProduct
from django.db.models import Sum,Count
from datetime import datetime
from django.views.decorators.cache import cache_control
from django.db.models import Q
from django.http import HttpResponse

from django.template.loader import get_template
from django.http import Http404
from xhtml2pdf import pisa


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
    available_years=OrderProduct.objects.values('created_at__year').distinct().order_by('created_at__year')
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
        'available_years':available_years,

    }
    return render(request,'admin/sales_report.html',context)

def salesreportbyyearmonth(request):
    if 'admin' not in request.session:
        return redirect('home')
    products = Product.objects.all()
    if 'year' in request.GET:
        y = request.GET['year']
        print(y)
        available_years=OrderProduct.objects.values('created_at__year').distinct().order_by('created_at__year')
        for year in available_years:
            print(year)
        
        if 'month' in request.GET:
            m = request.GET['month']
            print(type(m))
            print("m")
            try:
                if m == "0":
                    
                    sales=OrderProduct.objects.filter(Q(created_at__year=y)&Q(ordered=True)).values('product_id').annotate(qty=Sum('quantity'))
                    try:
                        total_earn= Payment.objects.filter(created_at__year=y).all()
                        total=0
                        for t in total_earn:
                            total+=float(t.amount_paid)
                        
                    except:
                        total="calculating"
                    grandtotalfind=OrderProduct.objects.filter(created_at__year=y).all()

                    total_without_discount=0
                    total_after_coupon_discount=0
                    total_after_coupon=Order.objects.filter(created_at__year=y).all()
                    for t_a_c in total_after_coupon:
                
                        try:
                            total_after_coupon_discount+=t_a_c.coupon.discount
                    
                        except:
                            pass
                    for t in grandtotalfind:
                        total_without_discount+=(t.product.price)*(t.quantity)
                        
                else:
                    
                    sales=OrderProduct.objects.filter(Q(created_at__year=y)& Q(ordered=True) & Q(created_at__month=m) ).values('product_id').annotate(qty=Sum('quantity'))
                    try:
                        total_earn= Payment.objects.filter(Q(created_at__year=y)& Q(created_at__month=m)).all()
                        total=0
                        for t in total_earn:
                            total+=float(t.amount_paid)
                        print("total")
                        print(total)
                    except:
                        total="calculating"
                    grandtotalfind=OrderProduct.objects.filter(Q(created_at__year=y)& Q(created_at__month=m)).all()
                    total_without_discount=0
                    total_after_coupon_discount=0
                    total_after_coupon=Order.objects.filter(Q(created_at__year=y)&Q(created_at__month=m)).all()
                    for t_a_c in total_after_coupon:
                
                        try:
                            total_after_coupon_discount+=t_a_c.coupon.discount
                    
                        except:
                            pass
                    for t in grandtotalfind:
                        total_without_discount+=(t.product.price)*(t.quantity)
                        print(t.product.price)
            
            except:
                sales=[]
        if m=="0":
            mon="(1-12)"
        else:
            mon=m
        salesdate= y + "-" + mon 

        context={
            'available_years':available_years,
            'products':products,
            'sales':sales,
            'salesdate':salesdate,
            'total':total,
            'total_without_discount':total_without_discount,
            'total_after_coupon_discount':total_after_coupon_discount,
            'year':y,
            'month':m,
            
        }
        
        return render(request,'admin/sales_report_year.html',context)

    return redirect(dashboard)


def create_pdf_year(request):
    if 'admin' not in request.session:
        return redirect('home')
    products = Product.objects.all()
    if request.method=='POST':
        salesdate =request.POST['salesdate_pdf_id']
        print("sales")
        print(salesdate)
    else:
        print("3044")
    sales_year_month=salesdate.split('/')
    y=sales_year_month[0]
    m=sales_year_month[1]
    print(y)
    print(m)
    # return HttpResponse("<h1>test</>")
    
 
    if y is not None:
        
        print(y)
        available_years=OrderProduct.objects.values('created_at__year').distinct().order_by('created_at__year')
        for year in available_years:
            print(year)
        
        if m is not None:
            
            print(type(m))
            print("m")
            try:
                if m == "0":
                    
                    sales=OrderProduct.objects.filter(Q(created_at__year=y)).values('product_id').annotate(qty=Sum('quantity'))
                    try:
                        total_earn= Payment.objects.filter(created_at__year=y).all()
                        total=0
                        for t in total_earn:
                            total+=float(t.amount_paid)
                        print("total")
                        print(total)
                    except:
                        total="calculating"
                    grandtotalfind=OrderProduct.objects.filter(created_at__year=y).all()

                    total_without_discount=0
                    total_after_coupon_discount=0
                    total_after_coupon=Order.objects.filter(created_at__year=y).all()
                    for t_a_c in total_after_coupon:
                
                        try:
                            total_after_coupon_discount+=t_a_c.coupon.discount
                    
                        except:
                            pass
                    for t in grandtotalfind:
                        total_without_discount+=(t.product.price)*(t.quantity)
                        print(t.product.price)
                else:
                    
                    sales=OrderProduct.objects.filter(Q(created_at__year=y)& Q(created_at__month=m) ).values('product_id').annotate(qty=Sum('quantity'))
                    try:
                        total_earn= Payment.objects.filter(Q(created_at__year=y)&Q(created_at__month=m)).all()
                        total=0
                        for t in total_earn:
                            total+=float(t.amount_paid)
                        print("total")
                        print(total)
                    except:
                        total="calculating"
                    grandtotalfind=OrderProduct.objects.filter(Q(created_at__year=y)&Q(created_at__month=m)).all()
                    total_without_discount=0
                    total_after_coupon_discount=0
                    total_after_coupon=Order.objects.filter(Q(created_at__year=y)&Q(created_at__month=m)).all()
                    for t_a_c in total_after_coupon:
                
                        try:
                            total_after_coupon_discount+=t_a_c.coupon.discount
                    
                        except:
                            pass
                    for t in grandtotalfind:
                        total_without_discount+=(t.product.price)*(t.quantity)
                        print(t.product.price)
            
            except:
                sales=[]
        salesdate= y + "-" + m 

        context={
            'available_years':available_years,
            'products':products,
            'sales':sales,
            'salesdate':salesdate,
            'total':total,
            'total_without_discount':total_without_discount,
            'total_after_coupon_discount':total_after_coupon_discount,
            'year':y,
            'month':m,
            
        }
        
        
    template_path = 'pdf/sales_report.html'
    
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'

    template = get_template(template_path)

    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response