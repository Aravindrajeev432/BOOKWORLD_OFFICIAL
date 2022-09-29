

from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.shortcuts import render,redirect
from django.views.decorators.cache import cache_control
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import Account
from accounts.views import user_login
from orders.models import Payment
from orders.models import Order,OrderProduct,Return_Products,banner
from store.models import Product,Product_Offer,Category_Offer,Coupon
from category.models import Category
from store.forms import ProductForm
# from category.forms import category_form
from django.contrib import auth,messages
# from slugify import slugify
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Sum,Count
from django.template.loader import get_template
from django.http import Http404
from xhtml2pdf import pisa
import xlwt
import datetime

from .forms import BannerForm

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminlogin(request):
    user=request.user
    try:
        if user.is_admin == True:
            return redirect(dashboard)
    except AttributeError :
        pass
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass']
        
        user = authenticate(email=email, password=password,)
        
        print(user)
        if user is None:
            return JsonResponse(
                {'success':False
                },
                safe=False
            )     
            
        if user.is_admin == True:
                print("l succes")
                request.session['admin'] = True
                auth.login(request,user)
                return JsonResponse(
                    {
                        'success':True},

                                safe=False
                            
                            )
        else:
                return JsonResponse(
                {'success':False
                },
                safe=False
            )           
        

    return render(request,'admin/adminlogin.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    auth.logout(request)
    request.session.flush()
    return redirect("/")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    user=request.user
    try:
        
        if user.is_active==True:
            if not user.is_admin==True:
                return redirect('/')
        if 'admin' not in request.session:
            return redirect('adminlogin')
    except AttributeError:
        return redirect(user_login)
    usercount= Account.objects.filter(~Q(is_admin=True)).count()
    p_count = Product.objects.count()
    products = Product.objects.all()
    # order_graph=Order.objects.aggregate(Sum('order_total'))
    # order_graph = OrderProduct.objects.all()
    order_graph =Order.objects.filter(is_ordered=True).values('created_at__date').order_by('-created_at__date').annotate(sum=Sum('order_total'))[9:]
    
    order_status_graph =OrderProduct.objects.filter().values('status').annotate(count=Count('status'))
    order_product_count_graph = OrderProduct.objects.filter().values('quantity').order_by('created_at__date')[:7].annotate(count=Count('quantity'))
    order_cat_graph = OrderProduct.objects.filter().values('product_id').annotate(count=Count('product_id'))

    print("--------")
    cat_count=[]
    for i in order_cat_graph:
        id=i['product_id']
        pcat=Product.objects.get(id=id)
        cat_count.append(pcat.category.category_name)
        
 
    cat_dict={}
    c= Category.objects.all()   
        
    for c_count in c:
    
        cat_dict[c_count.category_name] = cat_count.count(c_count.category_name)
    print(cat_dict)
    # print(order_cat_graph)

    print("-------")

    no_books = Product.objects.aggregate(Sum('book_count'))
    
    no_books = no_books['book_count__sum']
    
    
    pay = Payment.objects.values('amount_paid').all()

    total_sales=0
    for i in pay:
        t=i['amount_paid']
        t=float(t)
        total_sales=total_sales+t
        
    

    pgate = Payment.objects.all()
    amount_cod=0
    amount_paypal=0
    amount_razorpay=0
    for p in pgate:
        if p.payment_method=="COD":
            
            amount_cod+=float(p.amount_paid)
        elif p.payment_method=="Paypal":
            amount_paypal+=float(p.amount_paid)
        elif p.payment_method=="Razorpay":
            amount_razorpay+=float(p.amount_paid)
   
    
    context={'usercount':usercount,
             'p_count':p_count,
             'order_total_graph':order_graph,
             'order_status_graph':order_status_graph,
             'cat_dict':cat_dict,
             'no_books':no_books,
             'total_sales':total_sales,
             'amount_cod':amount_cod,
             'amount_paypal':amount_paypal,
             'amount_razorpay':amount_razorpay,
             }
    return render(request, 'admin/dashboard.html',context)

@login_required(login_url='adminlogin')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def products(request):
    user=request.user
    if user.is_active==True:
        if not user.is_admin==True:
            return redirect('/')
    if 'admin' not in request.session:
        return redirect('login')
    book_selled_count = OrderProduct.objects.filter(status='Deliverd').count()
    new_orders = OrderProduct.objects.filter(status='Processing').count()
    p_count = Product.objects.count()
    outofstock = Product.objects.filter(book_count=0).count()
    product = Product.objects.all().order_by('book_name')
    if request.method == 'POST':
        s = request.POST['search']
        product = Product.objects.filter(book_name__icontains=s)
    
    p = Paginator(product,6)
    page = request.GET.get('page',1)
    pro = p.get_page(page)
    
    cat = Category.objects.all()
    return render(request,'admin/productmanagement.html',{'product':product,'cat':cat,'p_count':p_count,'outofstock':outofstock,'pro':pro,'book_selled_count':book_selled_count,'new_orders':new_orders})

@login_required(login_url='adminlogin')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_book(request, id):
    user=request.user
    if user.is_active==True:
        if not user.is_admin==True:
            return redirect('/')
    if request.method == 'POST':
        bookedit = Product.objects.get(id=id)
        bookedit.book_name = request.POST.get('book_name')
        bookedit.author = request.POST.get('author_name')
        bookedit.description = request.POST.get('description')
        bookedit.price = request.POST.get('price')
        
        
        bookedit.category_id = request.POST.get('category')
        bookedit.book_count = request.POST.get('stock')
        if len(request.FILES) != 0:
            bookedit.image = request.FILES.get('image')
        bookedit.save()
        messages.success(request, 'Profile details updated.')
    book_details = Product.objects.get(id=id)
    category = Category.objects.all()
    return render(request,'admin/edit_book.html',{'book_details':book_details,'category':category})



@login_required(login_url='adminlogin')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def unblock_book(request, id):
    user=request.user
    if user.is_active==True:
        if not user.is_admin==True:
            return redirect('/')
    if 'admin' not in request.session:
        return redirect('adminlogin')
    bookun = Product.objects.get(id=id)
 
    bookun.is_active=True
    bookun.save()
    return redirect(products)
@login_required(login_url='adminlogin')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def block_book(request, id):
    user=request.user
    if user.is_active==True:
        if not user.is_admin==True:
            return redirect('/')
    if 'admin' not in request.session:
        return redirect('adminlogin')
    bookbl = Product.objects.get(id=id)
    re= request.GET.get('page')
    print(re)
    bookbl.is_active=False
    bookbl.save()
    return redirect(products)
@login_required(login_url='adminlogin')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_book(request, id):
    user=request.user
    if user.is_active==True:
        if not user.is_admin==True:
            return redirect('/')
    if 'admin' not in request.session:
        return redirect('adminlogin')
    bookdel= Product.objects.get(id=id)
    bookdel.delete()
    return redirect(products)

@login_required(login_url='adminlogin')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addnewbook(request):
    user=request.user
    if user.is_active==True:
        if not user.is_admin==True:
            return redirect('/')
    if 'admin' not in request.session:
        return redirect('adminlogin')
    form = ProductForm()
    # if request.method == 'POST':
    #     print(f)
    if request.method == "POST":
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
          
            form.save() 
            form = ProductForm() 
            messages.error(request,'Successfuly Added')
    cat = Category.objects.only('category_name')
    return render(request,'admin/addnewbook.html',{'cat':cat,'form':form})

@login_required(login_url='adminlogin')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addnewbooktest(request):
    user=request.user
    if user.is_active==True:
        if not user.is_admin==True:
            return redirect('/')
    if 'admin' not in request.session:
        return redirect('adminlogin')
    form = ProductForm()
    # if request.method == 'POST':
    #     print(f)
    if request.method == "POST":
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():

            form.save() 
            form = ProductForm() 
            messages.error(request,'Successfuly Added')
    cat = Category.objects.only('category_name')
    return render(request,'admin/addnewbooktest.html',{'cat':cat,'form':form})






@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletebook(request):
    pass
def editbook(request):
    pass

@login_required(login_url='adminlogin')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def category_management(request):
    user=request.user
    if user.is_active==True:
        if not user.is_admin==True:
            return redirect('/')
    if 'admin' not in request.session:
        return redirect('adminlogin')
    category = Category.objects.all()
    print(category)
    if request.method == 'POST':
        
        category_name = request.POST['category_name']
        if not Category.objects.filter(category_name__iexact=category_name).exists():
        
            cat = Category(category_name=category_name)
            cat.save()
        else:
            messages.error(request,'This category already exists')
    
    return render(request,'admin/addnewcategory.html',{'category':category})

@login_required(login_url='adminlogin')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_cat(request,id):
    print(id)
    user=request.user
    if user.is_active==True:
        if not user.is_admin==True:
            return redirect('/')
    if 'admin' not in request.session:
        return redirect('adminlogin')
    pass
    del_cat = Category.objects.get(id=id)
    del_cat.delete()
    return HttpResponse()

@login_required(login_url='adminlogin')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def users(request):
    user=request.user
    if user.is_active==True:
        if not user.is_admin==True:
            return redirect('/')
    if 'admin' not in request.session:
        return redirect('adminlogin')
    
    no_books_buyed = OrderProduct.objects.values('user_id').annotate(sum=Sum('quantity'))
    print("###########")
    print(no_books_buyed)
    no_books_buyed=list(no_books_buyed)
    
    print("###########")
    total_money_spent = Order.objects.values('user_id').annotate(sum=Sum('order_total'))
    total_money_spent = list(total_money_spent)
    print(total_money_spent)
    account = Account.objects.filter(~Q(is_admin=True))

    usercount= Account.objects.filter(~Q(is_admin=True)).count()

    try:
        
        blocked_users_count = Account.objects.filter(is_blocked=True).count()
    except:
        blocked_users_count=0
    active_users_count = usercount - blocked_users_count
    paginator = Paginator(account,6)
    page = request.GET.get('page')
    accounts =paginator.get_page(page)
    if request.method == 'POST':
        s = request.POST['search']
        account = Account.objects.filter(first_name__startswith=s)
        print(account)
        paginator = Paginator(account,6)
        page = request.GET.get('page')
        accounts =paginator.get_page(page)
        return render(request,'admin/usersview.html',{'account':accounts,'usercount':usercount,'blocked_users_count':blocked_users_count,'active_users_count':active_users_count,'no_books_buyed':no_books_buyed,'total_money_spent':total_money_spent})
    
    return render(request,'admin/usersview.html',{'account':accounts,'usercount':usercount,'blocked_users_count':blocked_users_count,'active_users_count':active_users_count,'no_books_buyed':no_books_buyed,'total_money_spent':total_money_spent})


@login_required(login_url='adminlogin')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_user(request, id):
    user=request.user
    if user.is_active==True:
        if not user.is_admin==True:
            return redirect('/')
    if 'admin' not in request.session:
        return redirect('adminlogin')
    if request.method == 'POST':
        useredit = Account.objects.get(id=id)
        useredit.first_name = request.POST.get('first_name')
        useredit.last_name = request.POST.get('last_name')
        useredit.email = request.POST.get('email')
        useredit.Phone_number = request.POST.get('phone')

        useredit.save()
        messages.success(request, 'Profile details updated.')
        

    user = Account.objects.get(id=id)   
    return render(request,'admin/edituser.html',{'user':user})

@login_required(login_url='adminlogin')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def block_user(request, id):
    user=request.user
    if user.is_active==True:
        if not user.is_admin==True:
            return redirect('/')
    if 'admin' not in request.session:
        return redirect('adminlogin')
    print("***************")
    b_user = Account.objects.get(id=id)
    print(b_user.is_blocked)
    b_user.is_blocked=True
    b_user.save()
    print(b_user.is_blocked)
    return JsonResponse(
                    {
                        'success':True},

                                safe=False
                            
                            )
    return redirect(users)
@login_required(login_url='adminlogin')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def unblock_user(request, id):
    user=request.user
    if user.is_active==True:
        if not user.is_admin==True:
            return redirect('/')
    if 'admin' not in request.session:
        return redirect('adminlogin')
    ub_user = Account.objects.get(id=id)
    ub_user.is_blocked=False
    ub_user.save()
    return redirect(users)


@login_required(login_url='adminlogin')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_user(request, id):
    user=request.user
    if user.is_active==True:
        if not user.is_admin==True:
            return redirect('/')
    if 'admin' not in request.session:
        return redirect('adminlogin')
    del_user = Account.objects.get(id=id)
    del_user.delete()
    return JsonResponse(
                    {
                        'success':True},

                                safe=False
                            
                            )
    return redirect(users)
# def sortbyfname(request):
    
#     return redirect(users)
@login_required(login_url='adminlogin')
def order_management(request):
    user=request.user
    if user.is_active==True:
        if not user.is_admin==True:
            return redirect('/')
        
    request.session['ordernumber_search'] =""
    new_orders=Return_Products.objects.filter(returnstatus="Waiting").count()
    print(new_orders)
    print("***")
    
    
    
    if 'search' in request.GET:
        request.session['ordernumber_search'] =""
        keyword = request.GET['search']
        print("paged")
        if keyword:
            pass
            print(keyword)
            if keyword=="SelectAll":
                order_details =Order.objects.all().filter(~Q(is_ordered=False)).order_by('-created_at')
                p = Paginator(order_details,5)
                page = request.GET.get('page',1)
                order_details_paginated = p.get_page(page)
                total_orders_count= OrderProduct.objects.all().count()
                
                orders_pending = OrderProduct.objects.filter(status__contains='Processing').count()
                orders_deliverd = OrderProduct.objects.filter(status__contains='Deliverd').count()
                # print(orders_pending)
                context={
                'order_details':order_details_paginated,
                'total_orders_count': total_orders_count,
                'orders_pending' : orders_pending,
                'orders_deliverd' : orders_deliverd,
                'new_orders':new_orders,
                }
                return render(request,'admin/ordermanagement.html',context)
            else:
                order_details =Order.objects.all().filter(~Q(is_ordered=False)& Q(payment__payment_method__contains=keyword) ).order_by('-created_at')
                p = Paginator(order_details,5)
                page = request.GET.get('page',1)
                order_details_paginated = p.get_page(page)
                total_orders_count= OrderProduct.objects.all().count()
                
                orders_pending = OrderProduct.objects.filter(status__contains='Processing').count()
                orders_deliverd = OrderProduct.objects.filter(status__contains='Deliverd').count()
                # print(orders_pending)
                context={
                'order_details':order_details_paginated,
                'total_orders_count': total_orders_count,
                'orders_pending' : orders_pending,
                'orders_deliverd' : orders_deliverd,
                'new_orders':new_orders,
                }
                return render(request,'admin/ordermanagement.html',context)
            
    elif 'ordernum' in request.GET:
        
        ordernum = request.GET['ordernum']
        request.session['ordernumber_search'] = ordernum
        order_details = Order.objects.all().filter(order_number__contains=ordernum)        
        p = Paginator(order_details,5)
        page = request.GET.get('page',1)
        order_details_paginated = p.get_page(page)
        total_orders_count= OrderProduct.objects.all().count()
        
        orders_pending = OrderProduct.objects.filter(status__contains='Processing').count()
        orders_deliverd = OrderProduct.objects.filter(status__contains='Deliverd').count()
        # print(orders_pending)
        context={
            'order_details':order_details_paginated,
            'total_orders_count': total_orders_count,
            'orders_pending' : orders_pending,
            'orders_deliverd' : orders_deliverd,
            'new_orders':new_orders,
        }
        return render(request,'admin/ordermanagement.html',context)
    else:
        
    
        # order_details = OrderProduct.objects.all().order_by('-created_at')
        order_details =Order.objects.all().filter(~Q(is_ordered=False)).order_by('-created_at')
        p = Paginator(order_details,5)
        page = request.GET.get('page',1)
        order_details_paginated = p.get_page(page)
        total_orders_count= OrderProduct.objects.all().count()
        
        orders_pending = OrderProduct.objects.filter(status__contains='Processing').count()
        orders_deliverd = OrderProduct.objects.filter(status__contains='Deliverd').count()
        # print(orders_pending)
        context={
            'order_details':order_details_paginated,
            'total_orders_count': total_orders_count,
            'orders_pending' : orders_pending,
            'orders_deliverd' : orders_deliverd,
            'new_orders':new_orders,
        }
        return render(request,'admin/ordermanagement.html',context)
    
    
@login_required(login_url='adminlogin')
def change_order_status(request,order_number,status):
    user=request.user
    if user.is_active==True:
        if not user.is_admin==True:
            return redirect('/')
    print(order_number)
    print(status)
    if status == "Delivered":
        print("CAncelled")
        checkdelivery=Order.objects.get(order_number=order_number)
        if checkdelivery.status=="Cancelled":
            status="Cancelled"
    order_product_details = Order.objects.get(order_number=order_number)
    print(order_product_details)
    # order_details = Order.objects.get(order_product_details.)
    order_product_details.status = status
    order_product_details.save()
    x = datetime.datetime.now()
    if status == "Cancelled":
        print("CAncelled")
    print(order_product_details.id)
    #Entry.objects.filter(pub_date__year=2007).update(headline='Everything is the same')
    OrderProduct.objects.filter(order_id=order_product_details.id).update(status=status,updated_at=x)
   


    return redirect(orders_page, order_number)
    
@login_required(login_url='adminlogin')
def orders_page(request,order_number):
    user=request.user
    if user.is_active==True:
        if not user.is_admin==True:
            return redirect('/')
    try:
        order_details=Order.objects.get(order_number=order_number)
    except:
        return redirect(order_management)
        
    print(order_details.id)
    order_id = order_details.id
    order_product_details=OrderProduct.objects.filter(order_id=order_id)
    print(order_product_details)

    
    context={
        'order_id':order_number,
        'order_details':order_details,
        'order_product_details':order_product_details,
   
    }
    return render(request,'admin/orders_page.html',context)


@login_required(login_url='adminlogin')
def invoice(request,order_number):
    user=request.user
    if user.is_active==True:
        if not user.is_admin==True:
            return redirect('/')
    print(order_number)
    order_details=Order.objects.get(order_number=order_number)
    print(order_details.id)
    order_id = order_details.id
    order_product_details=OrderProduct.objects.filter(order_id=order_id)
    net_qty= OrderProduct.objects.filter(order_id=order_id).aggregate(Sum('quantity'))
    print(net_qty)
    print(order_product_details)
    
    context={
        'order_id':order_number,
        'order_details':order_details,
        'order_product_details':order_product_details,
        'net_qty':net_qty,
    }
    template_path = 'pdf/invoice.html'



    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="invoice.pdf"'

    template = get_template(template_path)

    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response




def pdf_report_create(request):
    print("creted pdf called")
    products = Product.objects.all()
    

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

    print("dddddddd")
    try:
        sales = OrderProduct.objects.filter(created_at__date=dates[-1]).values('product_id').annotate(qty=Sum('quantity'))
    except:
        sales=[]
    # get total money earned in day qty*productprice
        try:
            total_earn= Payment.objects.filter(created_at=dates[-1]).aggregate(Sum('amount_paid'))
        except:
            pass
    try:
              total_earn= Payment.objects.filter(created_at__date=salesdate).all()
              total=0
              for t in total_earn:
                total+=float(t.amount_paid)
              print("total")
              print(total)
    except:
            total="calculating"
    if request.method=="POST":
        try:
            salesdate =request.POST['salesdate_pdf_id']
            print("Ssssss")
            print(salesdate)
        
            # sales= OrderProduct.objects.annotate(qty=Sum('quantity')).order_by('product_id')
            sales = OrderProduct.objects.filter(created_at__date=salesdate).values('product_id').annotate(qty=Sum('quantity')) 
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
    
        try:
            grand_total_after_discount = Payment.objects.filter(created_at=salesdate).aggregate(Sum('amount_paid'))
        except:
            grand_total_after_discount="calculating"
    
    
    
    
    print(grand_total_after_discount)

    template_path = 'pdf/sales_report.html'

    context= {
      'dates':dates,
     
      'current_date':current_date,
      'sales':sales,
        'products':products,
        'salesdate':salesdate,
        'total':total,
        'grand_total_after_discount':grand_total_after_discount,

    }

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





@login_required(login_url='adminlogin')
def export_excel(request):
    if request.method=='POST':
        salesdate=request.POST['salesdate_excel']
    response = HttpResponse(content_type = 'application/ms-excel')
    response['Content-Disposition'] = 'attachement; filename=SalesReport' +str(datetime.datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding = 'utf-8')
    ws = wb.add_sheet('SalesReport')
    row_num = 0
    font_style =xlwt.XFStyle()
    font_style.font.bold =True

    columns = ['order number','name ','amount  ','date']

    for col_num in range(len(columns)):
        ws.write(row_num,col_num, columns[col_num],font_style)
    
    font_style= xlwt.XFStyle()

    rows = Order.objects.filter(Q(created_at__date=salesdate) & Q(is_ordered=True)).values_list('order_number','first_name','order_total','created_at__date')

    for row in rows:
        row_num+=1

        for col_num in range(len(row)):
            ws.write(row_num,col_num, str(row[col_num]),font_style)

    wb.save(response)

    return response


@login_required(login_url='adminlogin')
def export_excel_year(request):
    if request.method=='POST':
        salesdate=request.POST['salesdate_excel']
        print(salesdate)
    else:
        print("3044")
    sales_year_month=salesdate.split('/')
    y=sales_year_month[0]
    m=sales_year_month[1]
    print(y)
    print(m)    
    response = HttpResponse(content_type = 'application/ms-excel')
    response['Content-Disposition'] = 'attachement; filename=SalesReport' +str(datetime.datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding = 'utf-8')
    ws = wb.add_sheet('SalesReport')
    row_num = 0
    font_style =xlwt.XFStyle()
    font_style.font.bold =True

    columns = ['order number','name ','amount  ','date']

    for col_num in range(len(columns)):
        ws.write(row_num,col_num, columns[col_num],font_style)
    
    font_style= xlwt.XFStyle()

    rows = Order.objects.filter(Q(created_at__year=y) &Q(created_at__month=m) & Q(is_ordered=True)).values_list('order_number','first_name','order_total','created_at__date')

    for row in rows:
        row_num+=1

        for col_num in range(len(row)):
            ws.write(row_num,col_num, str(row[col_num]),font_style)

    wb.save(response)

    return response



def pdf_check(request):
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

    print("dddddddd")
    try:
        sales = OrderProduct.objects.filter(created_at__date=dates[-1]).values('product_id').annotate(qty=Sum('quantity'))
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
    
    
    
    
    
    
    

    template_path = 'pdf/sales_report.html'

    context= {
      'dates':dates,
      'dates_max':dates_max,
      'current_date':current_date,
      'sales':sales,
        'products':products,
        'salesdate':salesdate,
        'total':total,

    }

    
    
    
    return render(request,'pdf/sales_report.html',context)

@login_required(login_url='adminlogin')
def offer_management(request):
    user=request.user
    if user.is_active==True:
        if not user.is_admin==True:
            return redirect('/')
    return render(request,'admin/offer_management.html')

@login_required(login_url='adminlogin')
def offer_management_productsview(request):
    user=request.user
    print(880)
    print(user)
    if not user.is_admin==True:
        return redirect('index')
    offerset=Product.objects.raw('select * from store_product LEFT JOIN store_product_offer on store_product.id=store_product_offer.product_id;')
    print(offerset)
    for of in offerset:
        print(of.book_name)
        print(of.discount)
    

    if 'page' in request.GET:
        keyword = request.GET['page']
        print(keyword)
        request.session['backtopage'] = keyword
    else:
        request.session['backtopage'] = 1
    p = Paginator(offerset,6)
    page = request.GET.get('page',1)
    pro = p.get_page(page)

  
    context={
        'products':pro,
    }
    
    
    return render(request,'admin/offers/offer_management_productsview.html',context)

@login_required(login_url='adminlogin')
def offer_management_product(request,bid):
    user=request.user
    if user.is_active==True:
        if not user.is_admin==True:
            return redirect('/')
    print(bid)
    book_details=Product.objects.get(id=bid)

    try:
        offer_details=Product_Offer.objects.get(product=bid)
    except:
        offer_details=[]
    print(offer_details)
    print(book_details.book_name)
    
        
    
    if request.method=="POST":
        discount_rate=request.POST['discount_rate']
        offer_active=request.POST['offer_active']
        print(discount_rate)
        print(type(offer_active))
        try:
            offer_p=Product_Offer.objects.get(product=bid)
            offer_p.product=book_details
            offer_p.discount=discount_rate
            if offer_active=="true":
                offer_p.active=True
            else:
                offer_p.active=False
            offer_p.save()
            return JsonResponse(
                        {
                            'success':True},

                                    safe=False
                                
                                )
            
        except:
        
            if offer_active=="true":
                offerproduct = Product_Offer(product=book_details,discount=discount_rate,active=True)
                offerproduct.save()
            else:
                offerproduct = Product_Offer(product=book_details,discount=discount_rate,active=False)
                offerproduct.save()
            return JsonResponse(
                        {
                            'success':True},

                                    safe=False
                                
                                )
    context={
            'book_details':book_details,
            'offer_details':offer_details,
        }
    return render(request,'admin/offers/offer_management_product.html',context)

@login_required(login_url='adminlogin')
def offer_management_categoryview(request):
    user=request.user
    if user.is_active==True:
        if not user.is_admin==True:
            return redirect('/')
    offerset=Category.objects.raw('SELECT * from category_category LEFT join store_category_offer ON store_category_offer.category_id = category_category.id')
    category=Category.objects.all()
    context={
        'category':offerset,
    }
    return render(request,'admin/offers/offer_management_categoryview.html',context)

@login_required(login_url='adminlogin')
def offer_management_category(request,cid):
    user=request.user
    if user.is_active==True:
        if not user.is_admin==True:
            return redirect('/')
    cat_details=Category.objects.get(id=cid)
    try:
        offer_details=Category_Offer.objects.get(category=cid)
    except:
        print("892")
        offer_details=[]
    if request.method=='POST':
        discount_rate=request.POST['discount_rate']
        offer_active=request.POST['offer_active']
        try:
            offer_details=Category_Offer.objects.get(category=cid)
            
            offer_details.discount=discount_rate
            if offer_active=="true":
                offer_details.active=True
            else:
                offer_details.active=False
            offer_details.save()
            return JsonResponse(
                        {
                            'success':True},

                                    safe=False
                                
                                )
        except:
        
        
            if offer_active=="true":
                offerproduct = Category_Offer(category=cat_details,discount=discount_rate,active=True)
                offerproduct.save()
            else:
                offerproduct = Category_Offer(category=cat_details,discount=discount_rate,active=False)
                offerproduct.save()
    context={
        'cat_details':cat_details,
        'offer_details':offer_details,
    }
    return render(request,'admin/offers/offer_management_category.html',context)

@login_required(login_url='adminlogin')
def returns(request):
    user=request.user
    if user.is_active==True:
        if not user.is_admin==True:
            return redirect('/')
    #offerset=Category.objects.raw('SELECT * from category_category LEFT join store_category_offer ON store_category_offer.category_id = category_category.id')
    returnproduct=OrderProduct.objects.raw('SELECT *,orders_return_products.id AS returnid FROM orders_orderproduct  join orders_return_products ON orders_return_products.return_product_id = orders_orderproduct.id')
    print(returnproduct)
    for i in returnproduct:
        print(i)
    p = Paginator(returnproduct,6)
    page = request.GET.get('page',1)
    return_product_pag = p.get_page(page)
    
    context={
        'returnproduct':return_product_pag,
    }
    return render(request,'admin/returns.html',context)

@login_required(login_url='adminlogin')
def return_order_admin(request,opid):
    user=request.user
    if user.is_active==True:
        if not user.is_admin==True:
            return redirect('/')
    return_product_details=Return_Products.objects.get(id=opid)
    print(return_product_details.return_product.order.first_name)
    
    if request.method=='POST':
        change_order_product_status=OrderProduct.objects.get(id=return_product_details.return_product_id)
        change_order_product_status.status="Returned"
        change_order_product_status.save()
        returnstatus=request.POST['returnstatus']
        print(returnstatus)
        return_product_details.returnstatus=returnstatus
        return_product_details.save()
        
        return JsonResponse(
                        {
                            'success':True},

                                    safe=False
                                
                                )
    
    context={
        'return_product_details':return_product_details
    }
    return render(request,'admin/return_order.html',context)

def offer_management_couponview(request):
    coupons=Coupon.objects.all()
    context={
        'coupons':coupons
    }
    return render(request,'admin/offers/offer_management_couponview.html',context)


@login_required(login_url='adminlogin')
def addnew_coupon(request):
    user=request.user
    if user.is_active==True:
        if not user.is_admin==True:
            return redirect('/')
    if request.method=="POST":
        coupon_code=request.POST['coupon_code']
        discount=request.POST['discount']
        valid_from=request.POST['valid_from']
        valid_to=request.POST['valid_to']
        is_active=request.POST['is_active']
        try:
            id=request.POST['id']
        except:
            id=""
        print(coupon_code)
        print(discount)
        print(is_active)
        print(valid_from)
        print(valid_to)
        try:
            coupon_details=Coupon.objects.get(id=id)
            coupon_details.coupon_code=coupon_code
            coupon_details.valid_from=valid_from
            coupon_details.valid_to=valid_to
            coupon_details.discount=discount
            if is_active=="true":
                coupon_details.active=True
            else:
                coupon_details.active=False
            coupon_details.save()
            return JsonResponse(
                        {
                            'success':True},

                                    safe=False
                                
                                )
        except:
            if is_active=="true":
                    coupon= Coupon(coupon_code=coupon_code,discount=discount,valid_from=valid_from,valid_to=valid_to,active=True)
                    coupon.save()
            else :
                coupon=Coupon(coupon_code=coupon_code,discount=discount,valid_from=valid_from,valid_to=valid_to,active=False)
                coupon.save()
            return JsonResponse(
                                {
                                    'success':True},

                                            safe=False
                                        
                                        )
    return render(request,'admin/offers/offer_management_coupon.html')


@login_required(login_url='adminlogin')
def coupon_view(request,id):
    user=request.user
    if user.is_active==True:
        if not user.is_admin==True:
            return redirect('/')
    coupons_details=Coupon.objects.get(id=id)
    context={
        'coupons_details':coupons_details,
    }
    return render(request,'admin/offers/offer_management_coupon_details.html',context)

@login_required(login_url='adminlogin')
def banners(request):
    user=request.user
    if user.is_active==True:
        if not user.is_admin==True:
            return redirect('/')
    bannr = banner.objects.all()
    return render(request,'admin/add_banner.html',{'bannr':bannr})


@login_required(login_url='adminlogin')
def banner_select(request,id):
    user=request.user
    if user.is_active==True:
        if not user.is_admin==True:
            return redirect('/')
    bannr = banner.objects.all()
    bannr.update(is_selected = False )
    banners = banner.objects.filter(id = id)
    banners.update(is_selected = True)
    return HttpResponse(True)




@login_required(login_url='adminlogin')
def add_banner(request):
    user=request.user
    if user.is_active==True:
        if not user.is_admin==True:
            return redirect('/')
    form = BannerForm(request.POST, request.FILES)
    bannr = banner.objects.all().order_by('id')
    if request.method == "POST":
        
        if form.is_valid():

            form.save()
            messages.success(request, 'New Banner added')
            
    
    context = {'form':form,
                   'bannr':bannr
                   }
    return render(request,'admin/add_banner.html',context)



@login_required(login_url='adminlogin')
def remove_banner(request , id):
    user=request.user
    if user.is_active==True:
        if not user.is_admin==True:
            return redirect('/')
    bannr = banner.objects.filter(id= id)
    bannr.delete()
    return redirect(banners)