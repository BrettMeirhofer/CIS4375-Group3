from . import models
from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory


class ProductPromoForm(ModelForm):
    title = "Products"
    field_titles = ["Product", "Current Price", "Promo Price"]

    def setfk(self, instance, parentinstance):
        instance.promo = parentinstance


    class Meta:
        model = models.ProductPromo
        fields = ['product', 'current_price', 'promo_price']


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


class ProductForm(ModelForm):
    formsets = [ProductImageFormSet, ProductProductTagFormSet]
    class Meta:
        model = models.Product
        fields = ['product_name', 'product_desc', 'created_date', 'product_status']
        widgets = {
            'created_date': DateInput(),
        }


class PromoForm(ModelForm):
    formsets = [ProductPromoFormSet]
    class Meta:
        model = models.Promo
        fields = ['promo_name', 'promo_code', 'promo_status']


# Create the form class.
class ProductStatusForm(ModelForm):
    class Meta:
        model = models.ProductStatus
        fields = ["status_name", "status_desc"]


form_listing = [ProductForm, PromoForm, ProductStatusForm]

