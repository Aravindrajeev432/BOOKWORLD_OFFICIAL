
from django.db import models
from accounts.models import Account
from store . models import Product
from store . models import Coupon
# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField()
    is_active =models.BooleanField(default=True)
    discount=models.IntegerField(default=0)
    discounttype=models.CharField(max_length=50,default='none')
    total_after_discount=models.IntegerField()
    coupon=models.ForeignKey(Coupon,on_delete=models.CASCADE,null=True)
    def sub_total(self):
        return self.product.price * self.quantity
    def __str__(self):
        return self.product.book_name