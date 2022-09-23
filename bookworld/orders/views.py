import json
from logging import exception
from django.shortcuts import render,redirect
from store.models import Coupon
from carts.models import Cart, CartItem
from store.models import Product
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import cache_control
from carts.views import _cart_id
from .forms import OrderForm
from .models import Order,Payment,OrderProduct,Return_Products
import datetime
import json
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponseBadRequest
from datetime import date
from django.db.models import Q,F
from openexchangerate import OpenExchangeRates
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required
# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)   
def place_order(request,total = 0 ,quantity= 0, cart_items = None):
    
    print("In place Order")
    uid = request.session['uid']
    
    try :
        if 'uid' in request.session:
            uid = request.session['uid']
            cart_items = CartItem.objects.filter(user_id=uid, is_active=True)
            cart_count = cart_items.count()
            if cart_count<= 0:
                return redirect('home')
        else:
            cart =Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            
        for cart_item in cart_items:
            total +=(cart_item.total_after_discount )
            quantity += cart_item.quantity
        try:
            coupon_discount=request.session['coupon_discount']
            print(coupon_discount)
            print("***")
            if coupon_discount==0:
                discount=0
                total_after_coupon=total
                coupon_details=None
            else:
                id=request.session['coupon_id']
                coupon_details=Coupon.objects.get(id=id)
                discount=request.session['coupon_discount']
                total_after_coupon=total-discount
                print(total_after_coupon)
                print("##")
        except:
            discount=0
            total_after_coupon=total
            coupon_details=None
    except ObjectDoesNotExist:
        pass
    context = {
        'total' : total,
        'quantity' :quantity,
        'cart_items' : cart_items,
        'total_after_coupon':total_after_coupon,
      
    }
    
    shipping_charge= 0
    
    if request.method == 'POST':
        payment_method=request.POST['payment_method']
        print(payment_method)      
        if payment_method=="Paypal":
            print("paypalworked")
            form = OrderForm(request.POST)
        
            if form.is_valid():
                print("form worked")
                data  = Order()
                data.user_id = uid
                data.first_name = form.cleaned_data['first_name']
                data.last_name = form.cleaned_data['last_name']
                data.phone = form.cleaned_data['phone']
                data.email = form.cleaned_data['email']
                data.address_line_1 = form.cleaned_data['address_line_1']
                data.address_line_2 = form.cleaned_data['address_line_2']
                data.country = form.cleaned_data['country']
                data.state = form.cleaned_data['state']
                data.city = form.cleaned_data['city']
                data.zipcode = form.cleaned_data['zipcode']
                data.order_total = total #just using total not grand total
                data.shipping_charge = shipping_charge
                data.coupon=coupon_details
                data.save()
                # Generate order number
                yr = int(datetime.date.today().strftime('%Y'))
                dt = int(datetime.date.today().strftime('%d'))
                mt = int(datetime.date.today().strftime('%m'))
                d = datetime.date(yr,mt,dt)
                current_date = d.strftime("%Y%m%d") #20210305
                order_number = current_date + str(data.id)
                data.order_number = order_number
                data.save()
                order = Order.objects.get(user_id=uid,is_ordered=False,order_number=order_number)
                
               
                client = OpenExchangeRates(api_key=settings.OPENEXCHANGEKEY)
                openx = list(client.latest())
                openx = openx[0]
                openxrupee = openx['INR']
                grand_dollar = round(total_after_coupon / openxrupee,2)
                    
                    
                
                
                # is_orderd is is_ordered because of its in model by mistake
                context = {
                    'order' : order,
                    'cart_items':cart_items,
                    'shipping_charge': shipping_charge,
                    'total':total,
                    'grand_total':total,
                    'order_number':order_number,
                    'payment_method':payment_method,
                    
                    'total_after_coupon':total_after_coupon,
                    'grand_dollar':grand_dollar,
                }
                
                
                return render(request,'store/review_checkout_paypal.html',context)
            
                
                
                
        elif payment_method == "Cod":
            print("codworked")  
            form = OrderForm(request.POST)
        
            if form.is_valid():
                print("form worked")
                data  = Order()
                data.user_id = uid
                data.first_name = form.cleaned_data['first_name']
                data.last_name = form.cleaned_data['last_name']
                data.phone = form.cleaned_data['phone']
                data.email = form.cleaned_data['email']
                data.address_line_1 = form.cleaned_data['address_line_1']
                data.address_line_2 = form.cleaned_data['address_line_2']
                data.country = form.cleaned_data['country']
                data.state = form.cleaned_data['state']
                data.city = form.cleaned_data['city']
                data.zipcode = form.cleaned_data['zipcode']
                data.order_total = total #just using total not grand total
                data.coupon=coupon_details
                data.shipping_charge = shipping_charge
                data.save()
                # Generate order number
                yr = int(datetime.date.today().strftime('%Y'))
                dt = int(datetime.date.today().strftime('%d'))
                mt = int(datetime.date.today().strftime('%m'))
                d = datetime.date(yr,mt,dt)
                current_date = d.strftime("%Y%m%d") #20210305
                order_number = current_date + str(data.id)
                data.order_number = order_number
                data.save()
                order = Order.objects.get(user_id=uid,is_ordered=False,order_number=order_number)
                
                # is_orderd is is_ordered because of its in model by mistake
                context = {
                    'order' : order,
                    'cart_items':cart_items,
                    'shipping_charge': shipping_charge,
                    'total':total,
                    'grand_total':total,
                    'order_number':order_number,
                    'payment_method':payment_method,
                    'total_after_coupon':total_after_coupon,
                }
                
            
                
                return render(request,'store/review_checkout_cod.html',context)
        elif payment_method == "Razorpay":
            print("razorpayworked")  
            form = OrderForm(request.POST)
        
            if form.is_valid():
                print("form worked")
                data  = Order()
                data.user_id = uid
                data.first_name = form.cleaned_data['first_name']
                data.last_name = form.cleaned_data['last_name']
                data.phone = form.cleaned_data['phone']
                data.email = form.cleaned_data['email']
                data.address_line_1 = form.cleaned_data['address_line_1']
                data.address_line_2 = form.cleaned_data['address_line_2']
                data.country = form.cleaned_data['country']
                data.state = form.cleaned_data['state']
                data.city = form.cleaned_data['city']
                data.zipcode = form.cleaned_data['zipcode']
                data.order_total = total #just using total not grand total
                data.coupon=coupon_details
                data.shipping_charge = shipping_charge
                data.save()
                # Generate order number
                yr = int(datetime.date.today().strftime('%Y'))
                dt = int(datetime.date.today().strftime('%d'))
                mt = int(datetime.date.today().strftime('%m'))
                d = datetime.date(yr,mt,dt)
                current_date = d.strftime("%Y%m%d") #20210305
                order_number = current_date + str(data.id)
                data.order_number = order_number
                request.session['order_number'] = order_number
                data.save()
                order = Order.objects.get(user_id=uid,is_ordered=False,order_number=order_number)
                
                # is_orderd is is_ordered because of its in model by mistake
                
                currency = 'INR'
                amount = total_after_coupon*100  # Rs. 200
            
                # Create a Razorpay Order
                razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                                currency=currency,
                                                                payment_capture='0'))
            
                # order id of newly created order.
                razorpay_order_id = razorpay_order['id']
                callback_url = 'paymenthandler/'
            
                # we need to pass these details to frontend.
              
                
                
                
                
                context = {
                    'order' : order,
                    'cart_items':cart_items,
                    'shipping_charge': shipping_charge,
                    'total':total,
                    'grand_total':total,
                    'order_number':order_number,
                    'payment_method':payment_method,
                    'total_after_coupon':total_after_coupon,
                    
                    'razorpay_order_id':razorpay_order_id,
                    'razorpay_merchant_key':settings.RAZOR_KEY_ID,
                    'razorpay_amount':amount,
                    'callback_url':callback_url,
                    
                 
                    
                }
               
                
                
                # context = {}
                # context['razorpay_order_id'] = razorpay_order_id
                # context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
                # context['razorpay_amount'] = amount
                # context['currency'] = currency
                # context['callback_url'] = callback_url
                
                
                # context['order']=order,
                # context['cart_items']=cart_item,
                # context['shipping_charge']=shipping_charge,
                # context['total']=total,
                # context['grand_total']=total,
                # context['order_number']=order_number,
                # context['payment_method']=payment_method,
                
                return render(request,'store/review_checkout_razorpay.html',context)    
            
    return redirect('checkout')


def review_checkout(request):
    
    return render(request,'store/review_checkout.html')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def payment(request,order_number,order_id,total):
    #COD payment method
    uid = request.session['uid']
    # body = json.loads(request.body)
    print("payment")
    print(type(order_id))
    try:
        
        order = Order.objects.get(user_id=uid, is_ordered=False, order_number=order_number)
        total=order.order_total
    except:
        return render(request,'store/checkout_fail.html')
    try:
        discount = order.coupon.discount,
    except:
        discount=0
    # Store transaction details inside Payment model
    payment = Payment(
        user_id = uid,
        payment_id = order_id,
        payment_method = "COD",
        amount_paid = total-discount,
        status = "succes",
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move the cart items to Order Product table
    cart_items = CartItem.objects.filter(user_id=uid)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = uid
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.discount= item.discount
        orderproduct.total_after_discount=item.total_after_discount
        orderproduct.save()

       


        # Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.book_count -= item.quantity
        product.save()

    # Clear cart
    CartItem.objects.filter(user_id=uid).delete()

    # Send order recieved email to customer
    context={
        'order_status':"Succes",
    }
    status="Success"
    return HttpResponse(status)
    return render(request,'store/checkout_succes.html',context)

#PAYPALPAYPALPAYPALPAYPALPAYPALPAYPALPAYPALPAYPALPAYPALPAYPALPAYPALPAYPALPAYPALPAYPALPAYPALPAYPAL
def payment_paypal(request):
    uid = request.session['uid']
    body = json.loads(request.body)
    order = Order.objects.get(user_id = uid, is_ordered = False, order_number = body['orderID'])
    print(body)
    try:
        discount = order.coupon.discount
    except:
        discount=0
    payment = Payment(
        user_id = uid,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        
        amount_paid = order.order_total - discount,
        status = body['status'],
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()
    
    # Move the cart items to Order Product table
    cart_items = CartItem.objects.filter(user_id=uid)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = uid
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.discount= item.discount
        orderproduct.total_after_discount=item.total_after_discount
        orderproduct.save()

       


        # Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.book_count -= item.quantity
        product.save()

    # Clear cart
    CartItem.objects.filter(user_id=uid).delete()

    
    
    
    
    
    
    # paypal payment method
    # uid = request.session['uid']
    # # body = json.loads(request.body)
    # print("payment")
    # print(type(order_id))
    # order = Order.objects.get(user_id=uid, is_ordered=False, order_number=order_number)

    # # Store transaction details inside Payment model
    # payment = Payment(
    #     user_id = uid,
    #     payment_id = order_id,
    #     payment_method = "COD",
    #     amount_paid = total,
    #     status = "succes",
    # )
    # payment.save()

    # order.payment = payment
    # order.is_ordered = True
    # order.save()

    # # Move the cart items to Order Product table
    # cart_items = CartItem.objects.filter(user_id=uid)

    # for item in cart_items:
    #     orderproduct = OrderProduct()
    #     orderproduct.order_id = order.id
    #     orderproduct.payment = payment
    #     orderproduct.user_id = uid
    #     orderproduct.product_id = item.product_id
    #     orderproduct.quantity = item.quantity
    #     orderproduct.product_price = item.product.price
    #     orderproduct.ordered = True
    #     orderproduct.save()

       


    #     # Reduce the quantity of the sold products
    #     product = Product.objects.get(id=item.product_id)
    #     product.book_count -= item.quantity
    #     product.save()

    # # Clear cart
    # CartItem.objects.filter(user_id=uid).delete()

    # # Send order recieved email to customer
   
    data = {
        'status':order.status,
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)


razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))







def payment_razorpay(request):
    uid = request.session['uid']
    body = json.loads(request.body)
    order = Order.objects.get(user_id = uid, is_ordered = False, order_number = body['orderID'])
    print(body)
    try:
        discount = order.coupon.discount
    except:
        discount=0
    payment = Payment(
        user_id = uid,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total-discount,
        status = body['status'],
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()
    
    # Move the cart items to Order Product table
    cart_items = CartItem.objects.filter(user_id=uid)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = uid
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.discount= item.discount
        orderproduct.total_after_discount=item.total_after_discount
        orderproduct.save()

       


#         # Reduce the quantity of the sold products
#         product = Product.objects.get(id=item.product_id)
#         product.book_count -= item.quantity
#         product.save()

#     # Clear cart
#     CartItem.objects.filter(user_id=uid).delete()
#     data = {
#         'status':order.status,
#         'order_number': order.order_number,
#         'transID': payment.payment_id,
#     }
#     return JsonResponse(data)

    
 
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
            uid = request.session['uid']
            order_number= request.session['order_number']
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            
            order = Order.objects.get(user_id = uid, is_ordered = False, order_number = order_number)
            print(payment_id)
            print(razorpay_order_id)
            print(signature)
            print(order.order_total)
            amount=int(order.order_total)
            
            
            print(538)
            discount=request.session['coupon_discount']
            
            amount=amount-discount
            amount=amount*100
     
            print("539")
            print(amount)
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            print("549")
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            print(result)
            if result is not None:
                
                try:
                    print("razor pay try2")
                    # capture the payemt
                    print(amount)
                    razorpay_client.payment.capture(payment_id, amount)
                    discount=request.session['coupon_discount']
                    payment = Payment(
                    user_id = uid,
                    payment_id = payment_id,
                    payment_method = "Razorpay",
                    amount_paid = order.order_total - discount ,
                    status ="COMPLETED",
                    
                    )
                    payment.save()
                    order.payment = payment
                    order.is_ordered = True
                    order.save()
                    print("568")
    # Move the cart items to Order Product table
                    cart_items = CartItem.objects.filter(user_id=uid)

                    for item in cart_items:
                        orderproduct = OrderProduct()
                        orderproduct.order_id = order.id
                        orderproduct.payment = payment
                        orderproduct.user_id = uid
                        orderproduct.product_id = item.product_id
                        orderproduct.quantity = item.quantity
                        orderproduct.product_price = item.product.price
                        orderproduct.ordered = True
                        orderproduct.discount= item.discount
                        orderproduct.total_after_discount=item.total_after_discount
                        orderproduct.save()

                    


                        # Reduce the quantity of the sold products
                        product = Product.objects.get(id=item.product_id)
                        product.book_count -= item.quantity
                        product.save()

                    # Clear cart
                        CartItem.objects.filter(user_id=uid).delete()

                        data = {
                 'status':"Pending",
                 'order_number': order.order_number,
                    'transID': payment.payment_id,
                             }
 
 
 
 
 
 
 
 

 
                    # render success page on successful caputre of payment
                    return render(request, 'store/checkout_succes.html',data)
                except:
                    print(exception)
                    # if there is an error while capturing payment.
                    return render(request, 'store/paymentfail.html')
            else:
                print("razorpay line508")
                # if signature verification fails.
                return render(request, 'store/paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()














def order_succes(request):
    print("order_succes")
    order_status = request.GET.get('order_status')
    order_number = request.GET.get('order_number')
    # order_number= request.GET['order_number']
    # order_status = request.GET['order_status']
    print("****")
    print(order_number)
    try:
        print("Order succes try")
        print(order_number)
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        print(order)
        context = {
        'order':order,
        'order_status':order_status,
        'order_number':order_number,
        
    }
        return render(request,'store/checkout_succes.html',context)
    except (Order.DoesNotExist):
        print("Order succes Exception")
        return redirect('home')
    
    return render(request,'store/checkout_succes.html',context)


def order_history(request):
    print("order_history")
    if 'email' in request.session:
        uid=request.session['uid']
        current_date=date.today()
        returndate={}
        order_history= OrderProduct.objects.filter(user_id=uid).annotate(ret=  F('updated_at__date') - current_date ).order_by('-created_at')
        for o in order_history:
            
            r=o.updated_at + datetime.timedelta(days=7)
            # print(o.updated_at + datetime.timedelta(days=7))
            print("*******")
            print(r.date())
            print(current_date)
            print("******")
            if r.date() > current_date:
                returndate.update({o.id:False})
            else:
                returndate.update({o.id:True})
            print(returndate)
            
   
        context={'order_history':order_history,
                 'current_date' : current_date,
                 'returndate' : returndate
                 }
        
        return render(request,'orders.html',context)
    else:
        return render(request,'orders_access_denied.html')
    
def cancel_order(request,oid):
    print(oid)
    print("yeah s")
    order_cancel = OrderProduct.objects.get(id=oid)
    if order_cancel.status=="Delivered":
        order_cancel.status = 'Delivered'
        order_cancel.save()
        return redirect(order_history)
    else:
        
        order_cancel.status = 'Cancelled'
        order_cancel.save()
        return redirect(order_history)
    
def return_order(request,oid):
    is_in_return=False
    order_details=[]
    print("returnproduct")
    uid=request.session['uid']
    if OrderProduct.objects.filter(Q(id=oid) & Q(user=uid)).exists():
        order_details=OrderProduct.objects.get(id=oid)
        return_details=''
        if Return_Products.objects.filter(return_product=order_details.id).exists():
            print("redirect")
            is_in_return=True
            return_details=Return_Products.objects.get(return_product=order_details.id)
            
        print(order_details.id)
        if request.method=="POST":
            print("******")
            reson=request.POST['reson']
            comment=request.POST['comments']
            print(reson)
            if reson =="1":
      
                ret=Return_Products(return_product=order_details,returnstatus='Waiting',reson="Damaged Product",comment=comment)
                ret.save()
            elif reson=="2":
    
                ret=Return_Products(return_product=order_details,returnstatus='Waiting',reson="Didn't meet my expectations",comment=comment)
                ret.save()
            else:
                print("##")
                ret=Return_Products(return_product=order_details,returnstatus='Waiting',reson="Changed my Mind",comment=comment)
                ret.save()
            
            print(comment)
            return JsonResponse(
                    {
                        'success':True},

                                safe=False
                            
                            )
    
        context={
            'order_number':oid,
            'order_details':order_details,
            'is_in_return':is_in_return,
            'return_details':return_details
        }
        
        return render(request,'return_order.html',context)
    else:
        return redirect(order_history)
    
def orders_page(request,order_number):
    order_details=Order.objects.get(order_number=order_number,is_ordered=True)
    print(order_details.id)
    order_id = order_details.id
    order_product_details=OrderProduct.objects.filter(order_id=order_id)
    print(order_product_details)

    
    context={
        'order_id':order_number,
        'order_details':order_details,
        'order_product_details':order_product_details,
   
    }
    return render(request,'orders_page_user.html',context)

@login_required(login_url='login')
def invoice(request,order_number):
    
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


def checkout_success(request):
    request.session['coupon_code']=""
    request.session['coupon_id']=""
    request.session['coupon_discount']=0
    return render(request,'store/checkout_succes.html')
def checkout_fail(request):
    return render(request,'store/checkout_fail.html')