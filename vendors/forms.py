from django import forms

class VendorForm(forms.Form):
    agree = forms.BooleanField(label="Agree to terms", widget=forms.CheckboxInput)