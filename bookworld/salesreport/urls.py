from django.urls import URLPattern, path
from . import views
urlpatterns = [
    # path('',views.product_view,name="productview"),
    
    path('',views.salespage,name='sales_report'),
    path('<int:year>',views.salespage,name='sales_report_year'),
    path('<int:year>/<int:month>',views.salespage),
    path('<int:year>/<int:month>/<int:day>',views.salespage),
    path('salesreportbyyearmonth',views.salesreportbyyearmonth,name='salesreportbyyearmonth'),
    path('create-pdf_year', views.create_pdf_year, name='create-pdf_year'),

]