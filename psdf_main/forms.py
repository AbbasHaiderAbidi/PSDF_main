from django import forms
from .models import *

from django.core.exceptions import ValidationError
class UserForm(forms.ModelForm):
    class Meta:
        model = users
        fields = ['username', 'password', 'nodal', 'region', 'utilname', 'contact', 'address']
        # fields = '__all__'
        REGIONS = [('','Region'),('North','North'), ('South','South'),('East','East'),('West','West'),('North East','North East')]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control col-md-6 mb-3 text-center', 'placeholder' : 'Enter username', 'id' : 'username'}),
            'password' : forms.PasswordInput(attrs={'class': 'form-control col-md-6 mb-3 text-center', 'placeholder' : 'Enter password', 'id' : 'password', 'name' : 'password'}),
            'nodal' : forms.TextInput(attrs={'placeholder':'Nodal Officer','class':'form-control col-md-5 mb-3 text-center'}),
            'region' : forms.Select(attrs={'placeholder':'Region','class':'form-control col-md-3 text-center','style':'height:100%;'}, choices=REGIONS),
            'utilname' : forms.TextInput(attrs={'placeholder':'Name of Utility','class':'form-control col-md-6 mb-3 text-center', 'id':'utility'}),
            'contact' : forms.TextInput(attrs={'placeholder':'Contact Number','class':'form-control col-md-6 mb-3 text-center'}),
            'address' : forms.TextInput(attrs={'id':'address', 'class':'form-control text-center mb-3', 'placeholder':'Enter the Address','style':'height:100%;'})
        }
