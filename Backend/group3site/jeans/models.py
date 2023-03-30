from django.db import models
from django import forms
from django.utils import timezone

from decimal import Decimal
from django.forms.widgets import Input


IsManaged = False


class MoneyField(models.DecimalField):
    pass


def past_validator(value):
    if value > timezone.now().date():
        raise forms.ValidationError("The date must be in the past!")
    return value


def not_zero_validator(value):
    if value == 0:
        raise forms.ValidationError("The value cannot be zero")


class DescriptiveModel(models.Model):
    id = models.AutoField(primary_key=True)
    description = "Blank Description"
    pk_desc = "Standard Auto-Increment PK"
    load_order = -1

    class Meta:
        abstract = True
        managed = IsManaged


# Used as an abstract parent for status codes
class StatusCode(DescriptiveModel):
    description = "Used to soft delete rows with a reason name and desc"
    status_name = models.CharField(max_length=40, verbose_name="Name")
    status_desc = models.TextField(max_length=200, blank=True, null=True, verbose_name="Description")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    list_fields = ["status_name", "status_desc"]
    category = "Other"

    def __str__(self):
        return self.status_name

    class Meta:
        abstract = True
        managed = IsManaged


# Used as an abstract parent for labels
class LabelCode(DescriptiveModel):
    description = "Allows for multiple named categories"
    type_name = models.CharField(max_length=40, verbose_name="Name")
    type_desc = models.TextField(max_length=200, blank=True, null=True, verbose_name="Description")
    category = "Other"
    load_order = 1

    def __str__(self):
        return self.type_name

    class Meta:
        abstract = True
        managed = IsManaged


class CustomerStatus(StatusCode):
    description = 'Refers to the current state of the customer'
    load_order = 1

    class Meta:
        db_table = "CustomerStatus"
        verbose_name_plural = "Customer Status"
        managed = IsManaged


class ProductStatus(StatusCode):
    description = 'Refers to the current state of the product'
    load_order = 1

    class Meta:
        db_table = "ProductStatus"
        verbose_name_plural = "Product Status"
        managed = IsManaged


class PromoStatus(StatusCode):
    description = 'Refers to the current state of the promo'
    load_order = 1

    class Meta:
        db_table = "PromoStatus"
        verbose_name_plural = "Promo Status"
        managed = IsManaged


class ProductTag(StatusCode):
    description = 'Used to categorize Products'
    load_order = 1

    class Meta:
        db_table = "ProductTag"
        verbose_name_plural = "Product Tag"
        managed = IsManaged


class Brand(DescriptiveModel):
    description = 'The company that owns the Brand for a product'
    brand_name = models.CharField(max_length=40, verbose_name="Name")
    brand_desc = models.TextField(max_length=200, blank=True, null=True, verbose_name="Description")
    brand_site = models.URLField(verbose_name="Website URL")
    load_order = 1
    list_fields = ["brand_name", "brand_site"]

    class Meta:
        db_table = "Brand"
        verbose_name_plural = "Brand"
        managed = IsManaged

    def __str__(self):
        return self.brand_name


class Product(DescriptiveModel):
    description = 'Anything sold by a Store.'
    product_name = models.CharField(max_length=80, verbose_name="Name")
    product_desc = models.TextField(max_length=200, blank=True, null=True, verbose_name="Description")
    product_price = MoneyField(max_digits=19, decimal_places=4, verbose_name="Price $", default=0.00)
    product_brand = models.ForeignKey(Brand, on_delete=models.RESTRICT, blank=True, null=True, verbose_name="Brand")
    product_status = models.ForeignKey(ProductStatus, on_delete=models.RESTRICT, blank=True, null=True, verbose_name="Status")
    product_tags = models.ManyToManyField(ProductTag, through="ProductProductTag")
    created_date = models.DateField(verbose_name="Date")
    load_order = 2
    list_fields = ["product_name", "created_date", "product_status", "get_current_price"]
    list_func_names = {"get_current_price": "Price"}

    def get_current_price(self):
        test = "${0:.2f}".format(float(self.product_price))
        return test

    class Meta:
        db_table = "Product"
        verbose_name_plural = "Product"
        managed = IsManaged

    def __str__(self):
        return self.product_name


class Promo(DescriptiveModel):
    description = 'Describes a promotion for a group of products most often a sale'
    promo_name = models.CharField(max_length=80, verbose_name="Name")
    promo_code = models.CharField(max_length=10, unique=True, verbose_name="Redemption Code")
    promo_status = models.ForeignKey(PromoStatus, on_delete=models.RESTRICT, verbose_name="Status")
    promo_products = models.ManyToManyField(Product, through="ProductPromo")
    created_date = models.DateField(verbose_name="Date")
    promo_desc = models.TextField(max_length=400, verbose_name="Description", blank=True, null=True)
    load_order = 2
    list_fields = ["promo_name", "promo_code", "promo_status"]

    class Meta:
        db_table = "Promo"
        verbose_name_plural = "Promo"
        managed = IsManaged

    def __str__(self):
        return self.promo_name


class ProductProductTag(DescriptiveModel):
    description = 'Used to associate a ProductTag with a Product'
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_tag = models.ForeignKey(ProductTag, on_delete=models.CASCADE)
    created_date = models.DateField()
    load_order = 3

    class Meta:
        db_table = "ProductProductTag"
        verbose_name_plural = "Product Product Tag"
        managed = IsManaged


class ProductImage(DescriptiveModel):
    description = 'An image with a caption that displays a product'
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product")
    image_url = models.URLField(verbose_name="Image URL")
    image_caption = models.CharField(max_length=200, blank=True, null=True, verbose_name="Caption")
    load_order = 3

    def getfk(self):
        return self.product

    class Meta:
        db_table = "ProductImage"
        verbose_name_plural = "Product Image"
        managed = IsManaged


class ProductPromo(DescriptiveModel):
    description = 'Used to associate a Product with a Promo and stores promo price data'
    product = models.ForeignKey(Product, on_delete=models.RESTRICT, verbose_name="Product")
    promo = models.ForeignKey(Promo, on_delete=models.RESTRICT, verbose_name="Promo")
    current_price = MoneyField(max_digits=19, decimal_places=4, verbose_name="Current Price $", default=0.00)
    promo_price = MoneyField(max_digits=19, decimal_places=4, verbose_name="Promo Price $", default=0.00)
    load_order = 3

    def getfk(self):
        return self.promo

    class Meta:
        db_table = "ProductPromo"
        verbose_name_plural = "Product Promo"
        managed = IsManaged


class Customer(DescriptiveModel):
    description = 'Name and email for a customer who will recieve promo emails'
    first_name = models.CharField(max_length=200, verbose_name="First Name")
    last_name = models.CharField(max_length=200, verbose_name="Last Name")
    email = models.EmailField(verbose_name="Email Address")
    created_date = models.DateField(verbose_name="Created Date")
    customer_status = models.ForeignKey(CustomerStatus, on_delete=models.RESTRICT, verbose_name="Status")
    load_order = 2
    list_fields = ["first_name", "last_name", "email", "created_date", "customer_status"]

    def __str__(self):
        return self.email

    class Meta:
        db_table = "Customer"
        verbose_name_plural = "Customer"
        managed = IsManaged


class CustomerPromo(DescriptiveModel):
    description = 'Records when a customer redeems a promo. Key data point for promo success'
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT)
    promo = models.ForeignKey(Promo, on_delete=models.RESTRICT)
    created_date = models.DateField()
    load_order = 4

    list_fields = ["customer", "promo", "created_date"]

    class Meta:
        db_table = "CustomerPromo"
        verbose_name_plural = "Customer Promo"
        managed = IsManaged