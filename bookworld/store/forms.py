from django import forms
from .models import Product

#form for product management
class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        # fields= ['book_name','author','description','price','image','category',]
        fields = ('book_name','author','description','price','image','category','book_count')
        widgets = {
            'book_name': forms.TextInput(attrs={'class':'form-control','required':True}),

            'author': forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control','required':True}),
            'price':forms.NumberInput(attrs={'class':'form-control'}),
            'image':forms.FileInput(attrs={'class':'form-control'}),
            'category':forms.Select(attrs={'class':'form-control','id':'id_cat'}),
            'book_count':forms.NumberInput(attrs={'class':'form-control'}),
        }