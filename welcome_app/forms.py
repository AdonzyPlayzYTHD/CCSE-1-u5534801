from django import forms
from .models import Product

class ProductForm(forms.ModelForm): # the products form class showing the attributes associated with each product
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'inventory']