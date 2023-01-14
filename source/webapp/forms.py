from django import forms

from webapp.models import Product, Review
from django.forms import widgets


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "category", "picture"]
        widgets = {"description": widgets.Textarea}