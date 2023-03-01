from . import models
from django.forms import ModelForm


class ProductForm(ModelForm):
    class Meta:
        model = models.Product
        fields = ['product_name', 'product_desc']

# Create the form class.
class PromoForm(ModelForm):
    class Meta:
        model = models.Promo
        fields = ['promo_name', 'promo_code']

form_listing = [ProductForm, PromoForm]