from django.shortcuts import render,redirect

from admins.views import adminlogin

# Create your views here.
def error_404(request,exception):
    user=request.user
    try:
        if user.is_admin == True:
            return redirect(adminlogin)
    except AttributeError:
        pass
    return render(request,'404.html')