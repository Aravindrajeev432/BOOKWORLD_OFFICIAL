

from django.db import models
from accounts.models import Account
from store.models import Product,Coupon
# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.FloatField()
    status = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)
    
def __str__(self):
    return self.payment_id

class Order(models.Model):
    STATUS =(
        ('Processing','Processing'),
        ('Shipped','Shipped'),
        ('Deliverd','Deliverd'),
        ('Cancelled','Cancelled'),
    )
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zipcode =models.CharField(max_length=30,default='000000')
    order_total = models.FloatField()
    shipping_charge = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='Processing')
    
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    coupon=models.ForeignKey(Coupon,on_delete=models.CASCADE,null=True)
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'

    def __str__(self):
        return self.first_name
    
class OrderProduct(models.Model):
    STATUS =(
        ('Processing','Processing'),
        ('Shipped','Shipped'),
        ('Deliverd','Deliverd'),
        ('Cancelled','Cancelled'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS, default='Processing')
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    discount =models.IntegerField()
    total_after_discount=models.IntegerField()
    def __str__(self):
        return self.product.book_name
    
class Return_Products(models.Model):
    STATUS =(
        ('Waiting','Waiting'),
        ('Approved','Approved'),
        ('Rejected','Rejected')
   
    )
    return_product= models.ForeignKey(OrderProduct,on_delete=models.CASCADE)
    reson=models.CharField(max_length=200)
    comment= models.CharField(max_length=200)
    returnstatus=models.CharField(max_length=200,choices=STATUS, default='Processing')
    
    
class banner(models.Model):
    
    banner_image =models.ImageField( upload_to='photos/banner', height_field=None, width_field=None, max_length=None,blank=True)
    
    is_selected = models.BooleanField(default=False)