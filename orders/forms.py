from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'country', 'state', 'city','address']