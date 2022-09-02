from django import forms
from accounts.models import Account

#form for product management
class ProfileForm(forms.ModelForm):

    class Meta:
        model = Account

    
        fields = ('first_name','last_name','email','password')
        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control rounded-0','required':True}),
            'last_name' :forms.TextInput(attrs={'class':'form-control rounded-0','required':True}),
            'email' :forms.EmailInput(attrs={'class':'form-control rounded-0','required':True}),
            'password' : forms.PasswordInput(attrs={'class':'form-control rounded-0','required':True}),
            
           
        }