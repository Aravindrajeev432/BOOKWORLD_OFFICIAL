from django.shortcuts import render

# Create your views here.
def error_404(request,exception):
    return render(request,'404.html')