
from django import forms
from orders.models import banner

#form for product management
class BannerForm(forms.ModelForm):

    class Meta:
        model = banner

        fields= ['banner_image']

        widgets = {
            'banner_image':forms.FileInput(attrs={'class':'form-control rounded-0','required':True}),
            
        }