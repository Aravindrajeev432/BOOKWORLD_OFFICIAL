from django.db import models
from django.forms import IntegerField
from accounts.models import Account
from category . models import Category
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import FileExtensionValidator
# from django_extensions.db.fields import AutoSlugField
# Create your models here.

class Product(models.Model):
    book_name = models.CharField(max_length=200,unique = True)
    # slug      = models.SlugField(unique = True,blank=True)
    author = models.CharField(max_length=50)
    description =  models.TextField(max_length=500,blank=True)
    price = models.IntegerField(validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to = 'photos/book',validators=[FileExtensionValidator(allowed_extensions=["jpg","jpeg","webp"])])
    category     = models.ForeignKey(Category, on_delete=models.CASCADE)
    book_count = models.IntegerField(validators=[MinValueValidator(0)],default=0)
    is_active = models.BooleanField(default=False)
    def get_url(self):
        return reverse('product_page',args=[self.category.slug, self.slug])

    def __str__(self):
        return self.book_name
    
class Product_Offer(models.Model):
    product = models.OneToOneField(Product,on_delete=models.CASCADE,related_name = "offerof")
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    active = models.BooleanField( default=True)
    def __str__(self):
            return self.product.book_name
        
        
class Category_Offer(models.Model):
    category = models.OneToOneField(Category,on_delete=models.CASCADE)
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    active = models.BooleanField( default=True)
    def __str__(self):
            return self.category.category_name
        
class Coupon(models.Model):
    coupon_code = models.CharField(max_length=30,unique=True)
    valid_from = models.DateTimeField( null = True)
    valid_to = models.DateTimeField( null = True )
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.coupon_code


class WishlistItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)


    def __str__(self):
        return self.product.book_name