from django.forms import ModelForm
from django import forms
from .models import Product
from django.utils.text import slugify

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = [ 
                'title',
                'category',
                'description',
                'image',
                'media',
                'price'
    ]
        
    def clean_desc(self):
        data = self.form.cleaned_data.get('description')
        if len(data) < 6:
            raise forms.validationError("The description is not long enough")