from multiprocessing import context
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from carts.views import _cart_id
from carts.models import Cart,CartItem
from .models import Account
from twilio.rest import Client
from django.conf import settings
from django.contrib import messages, auth
from django.contrib.auth import authenticate
# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_login(request):

    if 'email' in request.session:
        return redirect('/homepage')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass']
        
        print(email)
        print(password)
        # user = auth.authenticate(email=email, password=password)
        # if user is not None:
        #     auth.login(request,user)
        #     return HttpResponse('<h1>Logged IN</h1>')
        user = authenticate(email=email, password=password)
        if user is not None and user.is_admin == False:
            
                print("user is not admin and not none ")
                try :
                    cart=Cart.objects.get(cart_id=_cart_id(request))
                    is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                    if is_cart_item_exists:
                        cart_item =CartItem.objects.filter(cart=cart)
                        for item in cart_item:
                            item.user_id= user.id
                            item.save()
                except :
                    pass
                print("l succes")
                if user.is_blocked == True:
                    auth.login(request, user)
                    request.session['uid'] = user.id
                    return JsonResponse(
                    {
                        'success':True},

                                safe=False
                            
                            )
                else:
                    auth.login(request, user)
                    request.session['email'] = user.email
                    request.session['uid'] = user.id
                    request.session['first_name'] = user.first_name
                    request.session['last_name'] = user.last_name
                
               
                    return JsonResponse(
                    {
                        'success':True},

                                safe=False
                            
                            )
        else:   
                print(user)
               
                print("user is none")
                return JsonResponse(
                {'success':False
                },
                safe=False
            )   
    return render(request, 'login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register(request):
    if 'email' in request.session:
        return redirect('/homepage')
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password1'] 
        user_name=""
        user = Account.objects.create_user(first_name = first_name, last_name = last_name, email = email, password = password)
        user.Phone_number = phone
        user.save()
        return redirect(user_login)
    return render(request, 'register.html')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    auth.logout(request)
    request.session.flush()
    return redirect("/")


def otp_verfication_send(request):
    if request.method == 'POST':
        otp_number = request.POST['otp_phone']
        
        
        print(otp_number)
        
        if Account.objects.filter(Phone_number = otp_number).exists():
            user = Account.objects.get(Phone_number=otp_number)
            Phone_number = "+91"+request.POST['otp_phone']
            account_sid = settings.ACCOUNT_SID
            auth_token = settings.AUTH_TOKEN
            client=Client(account_sid,auth_token)
            verification = client.verify \
                    .services(settings.SERVICE) \
                    .verifications \
                    .create(to=Phone_number,channel='sms')
        
            return render(request,'otp_verification.html',{'Phone_number':otp_number,'user':user,})
        else:
            print("fail")
        
        
        
    messages.info(request,'invalid mobile number ! !')
    return render(request, 'login.html')

def otp_verification_check(request,Phone_number):

    if request.method=='POST':
        if Account.objects.filter(Phone_number= Phone_number).exists():
            user = Account.objects.get(Phone_number= Phone_number)
           
            phone_no = "+91" + str(Phone_number)
            otp_input =  request.POST['otp']
         
            if len(otp_input)>0:

                
                account_sid = settings.ACCOUNT_SID
                auth_token = settings.AUTH_TOKEN
                client = Client(account_sid, auth_token)
            
                verification_check = client.verify \
                                    .services(settings.SERVICE) \
                                    .verification_checks \
                                    .create(to= phone_no, code= otp_input)
        
                if verification_check.status == "approved":
                    auth.login(request, user)
                    request.session['email'] = user.email
                    request.session['uid'] = user.id
                    request.session['first_name'] = user.first_name
                    request.session['last_name'] = user.last_name
                    
                    return redirect('home')
                else:   
                    messages.error(request,'Invalid OTP')
                    return redirect('otp_verification_check',Phone_number)
            else:
                messages.error(request,'Invalid OTP')
                
                return redirect('otp_verfication_check',Phone_number)

        else:

                messages.error(request,'Invalid Phone number')
                
                return redirect('otp_verification_check',Phone_number)

    # return render(request, 'accounts/otp_verification_check.html',{'Phone_number':Phone_number})
    return render(request, 'accounts/otp_verification_check.html',{'Phone_number':Phone_number})
