from . import models
from django import forms
from django.forms import ModelForm


class DateInput(forms.DateInput):
    input_type = 'date'


class ProductForm(ModelForm):
    class Meta:
        model = models.Product
        fields = ['product_name', 'product_desc', 'created_date', 'product_status']
        widgets = {
            'created_date': DateInput(),
        }


class PromoForm(ModelForm):
    class Meta:
        model = models.Promo
        fields = ['promo_name', 'promo_code', 'promo_status']


# Create the form class.
class ProductStatusForm(ModelForm):
    class Meta:
        model = models.ProductStatus
        fields = ["status_name", "status_desc"]


form_listing = [ProductForm, PromoForm, ProductStatusForm]