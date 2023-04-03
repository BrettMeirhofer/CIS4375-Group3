from . import models
from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.contrib import admin
from django.contrib.admin.widgets import AutocompleteSelect
from django import forms


class ProductPromoForm(ModelForm):
    title = "Products"
    field_titles = ["Product", "Current Price $", "Promo Price $"]

    def setfk(self, instance, parentinstance):
        instance.promo = parentinstance

    class Meta:
        model = models.ProductPromo
        fields = ['product', 'current_price', 'promo_price']
        widgets = {
            'current_price': forms.widgets.NumberInput(attrs={'class': 'money'}),
            'promo_price': forms.widgets.NumberInput(attrs={'class': 'money'}),
            'product': forms.widgets.Select(attrs={'class': 'js-example-basic-single'}),
        }


class ProductProductTagForm(ModelForm):
    title = "Tags"
    field_titles = ["Tag"]

    def setfk(self, instance, parentinstance):
        instance.product = parentinstance

    class Meta:
        model = models.ProductProductTag
        fields = ['product_tag',]


class ProductImageForm(ModelForm):
    title = "Images"
    field_titles = ["URL", "Caption"]

    def setfk(self, instance, parentinstance):
        instance.product = parentinstance

    class Meta:
        model = models.ProductImage
        fields = ['image_url', 'image_caption']


ProductPromoFormSet = inlineformset_factory(
    models.Promo, models.ProductPromo, form=ProductPromoForm,
    extra=1, can_delete=True, can_delete_extra=True
)


ProductImageFormSet = inlineformset_factory(
    models.Product, models.ProductImage, form=ProductImageForm,
    extra=1, can_delete=True, can_delete_extra=True
)

ProductProductTagFormSet = inlineformset_factory(
    models.Product, models.ProductProductTag, form=ProductProductTagForm,
    extra=1, can_delete=True, can_delete_extra=True
)


class DateInput(forms.DateInput):
    input_type = 'date'


class NumberInput(forms.widgets.Input):
    input_type = "number"
    template_name = "django/forms/widgets/number.html"


class ProductForm(ModelForm):
    formsets = [ProductImageFormSet, ProductProductTagFormSet]

    class Meta:
        model = models.Product
        fields = ['product_name', 'product_desc', 'created_date', 'product_status', 'product_price']
        widgets = {
            'created_date': DateInput(),
            'product_price': forms.widgets.NumberInput(attrs={'class': 'money'})
        }


class PromoForm(ModelForm):
    formsets = [ProductPromoFormSet]

    class Meta:
        model = models.Promo
        fields = ['promo_name', 'promo_code', 'promo_status', 'promo_desc']



class BrandForm(ModelForm):
    class Meta:
        model = models.Brand
        fields = ['brand_name', 'brand_site', 'brand_desc']


# Create the form class.
class ProductStatusForm(ModelForm):
    class Meta:
        model = models.ProductStatus
        fields = ["status_name", "status_desc"]


class PromoStatusForm(ModelForm):
    class Meta:
        model = models.PromoStatus
        fields = ["status_name", "status_desc"]


class CustomerStatusForm(ModelForm):
    class Meta:
        model = models.CustomerStatus
        fields = ["status_name", "status_desc"]


class ProductTagForm(ModelForm):
    class Meta:
        model = models.ProductTag
        fields = ["status_name", "status_desc"]


class CustomerPromoForm(ModelForm):
    field_titles = ["Promo", "Redeem Date"]

    def setfk(self, instance, parentinstance):
        instance.customer = parentinstance

    class Meta:
        model = models.CustomerPromo
        fields = ["promo", "created_date"]
        widgets = {
            'created_date': DateInput(),
        }


CustomerPromoFormSet = inlineformset_factory(
    models.Customer, models.CustomerPromo, form=CustomerPromoForm,
    extra=1, can_delete=True, can_delete_extra=True
)


class CustomerForm(ModelForm):
    formsets = [CustomerPromoFormSet]
    class Meta:
        autocomplete_fields = ('customer',)
        model = models.Customer
        fields = ["first_name", "last_name", "email", "created_date", "customer_status"]
        widgets = {
            'created_date': DateInput(),
        }


form_listing = [ProductForm, PromoForm, ProductStatusForm, CustomerPromoForm, CustomerForm, BrandForm, PromoStatusForm,
                CustomerStatusForm, ProductTagForm]
