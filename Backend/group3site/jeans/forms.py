from . import models
from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.contrib import admin
from django.contrib.admin.widgets import AutocompleteSelect
from django import forms


class ProductPromoForm(ModelForm):
    title = "Products"
    field_titles = ["Product", "Current Price $", "Promo Price $", "Display"]
    prefix="productpromo"

    def setfk(self, instance, parentinstance):
        instance.promo = parentinstance

    class Meta:
        model = models.ProductPromo
        fields = ['product', 'current_price', 'promo_price', "display_product"]
        widgets = {
            'current_price': forms.widgets.NumberInput(attrs={'class': 'money'}),
            'promo_price': forms.widgets.NumberInput(attrs={'class': 'money'}),
            'product': forms.widgets.Select(attrs={'class': 'js-example-basic-single'}),
        }


class ProductProductTagForm(ModelForm):
    title = "Tags"
    prefix = "productproducttag"
    field_titles = ["Tag"]

    def setfk(self, instance, parentinstance):
        instance.product = parentinstance

    class Meta:
        model = models.ProductProductTag
        fields = ['product_tag',]


class ProductImageForm(ModelForm):
    title = "Images"
    prefix = "productimage"
    field_titles = ["URL", "Caption", "Primary"]

    def setfk(self, instance, parentinstance):
        instance.product = parentinstance

    class Meta:
        model = models.ProductImage
        fields = ['image_url', 'image_caption', 'primary_image']


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
    inline = ["created_date", "product_status"]
    class Meta:
        model = models.Product
        fields = ['product_name', 'created_date', 'product_status', 'product_price', 'product_desc']
        widgets = {
            'created_date': DateInput(),
            'product_price': forms.widgets.NumberInput(attrs={'class': 'money'})
        }


class PromoForm(ModelForm):
    formsets = [ProductPromoFormSet]
    add_actions = [{"name": "Print", "url": "print_promo"}]
    inline = ["created_date", "end_date"]

    class Meta:
        model = models.Promo
        fields = ['promo_name', 'promo_code', 'promo_status', 'created_date', 'end_date', 'promo_desc']
        widgets = {
            'created_date': DateInput(),
            'end_date': DateInput(),
        }


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


class StateForm(ModelForm):
    class Meta:
        model = models.State
        fields = ["state_name", "country"]


class CountryForm(ModelForm):
    class Meta:
        model = models.Country
        fields = ["country_name"]


class ProductTagForm(ModelForm):
    class Meta:
        model = models.ProductTag
        fields = ["tag_name", "tag_desc"]


class CustomerPromoProductForm(ModelForm):
    field_titles = ["Product", "Quantity", "Normal Price", "Promo Price", "Line Total", "Line Discount"]
    title = "Products"
    prefix = "customerpromoproduct"
    def setfk(self, instance, parentinstance):
        instance.customer_promo = parentinstance

    class Meta:
        model = models.CustomerProductPromo
        fields = ["product", "quantity", "normal_price", "promo_price", "line_total", "line_discount"]
        widgets = {
            'quantity': forms.widgets.NumberInput(attrs={"style": "width:75px;padding:10px 0px"}),
            'normal_price': forms.widgets.NumberInput(attrs={'class': 'money', 'readonly': ""}),
            'promo_price': forms.widgets.NumberInput(attrs={'class': 'money', 'readonly': ""}),
            'line_total': forms.widgets.NumberInput(attrs={'class': 'money', 'readonly': ""}),
            'line_discount': forms.widgets.NumberInput(attrs={'class': 'money', 'readonly': ""})
        }


CustomerProductPromoFormSet = inlineformset_factory(
    models.CustomerPromo, models.CustomerProductPromo, form=CustomerPromoProductForm,
    extra=1, can_delete=True, can_delete_extra=True
)


class CustomerPromoForm(ModelForm):
    formsets = [CustomerProductPromoFormSet]
    inline = ["total_spent", "total_discount"]
    class Meta:
        model = models.CustomerPromo
        fields = ["customer", "promo", "created_date", "total_spent", "total_discount"]
        widgets = {
            'customer': forms.widgets.Select(attrs={'class': 'js-example-basic-single'}),
            'created_date': DateInput(),
            'total_spent': forms.widgets.NumberInput(attrs={'class': 'money', 'readonly': ""}),
            'total_discount': forms.widgets.NumberInput(attrs={'class': 'money', 'readonly': ""})
        }

    class Media:
        js = ('js/customer_product_promo.js',)


class CustomerForm(ModelForm):
    inline = ["created_date", "customer_status", "first_name", "last_name", "state", "country"]
    class Meta:
        autocomplete_fields = ('customer',)
        model = models.Customer
        fields = ["first_name", "last_name", "email", "phone_number", "created_date",
                  "customer_status", "zip_code", "city", "address", "state", "country"]
        widgets = {
            'created_date': DateInput(),
            'phone_number': forms.widgets.TextInput(attrs={"placeholder":"123-453-6748", "pattern":"[0-9]{3}-[0-9]{3}-[0-9]{4}", "class": "phone", "maxlength": 12}),
            'address': forms.widgets.TextInput(attrs={"style": "width:500px;"})
        }


form_listing = [ProductForm, PromoForm, ProductStatusForm, CustomerPromoForm, CustomerForm, BrandForm, PromoStatusForm,
                CustomerStatusForm, ProductTagForm, CountryForm, StateForm]

