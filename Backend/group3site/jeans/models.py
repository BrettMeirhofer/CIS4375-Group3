from django.db import models
from django import forms
#from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
import os
from django.db import connection

IsManaged = False

def past_validator(value):
    if value > timezone.now().date():
        raise forms.ValidationError("The date must be in the past!")
    return value


def not_zero_validator(value):
    if value == 0:
        raise forms.ValidationError("The value cannot be zero")


class MoneyField(models.DecimalField):
    def __init__(self):
        super().__init__(max_digits=19, decimal_places=4, default=0)

    def __str__(self):
        return "$" + super.__str__(self)

    widget = forms.Textarea


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
    status_name = models.CharField(max_length=40)
    status_desc = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    list_fields = ["status_name", "status_desc"]
    list_headers = ["Name", "Description"]
    category = "Other"

    def __str__(self):
        return self.status_name

    class Meta:
        abstract = True
        managed = IsManaged


# Used as an abstract parent for labels
class LabelCode(DescriptiveModel):
    description = "Allows for multiple named categories"
    type_name = models.CharField(max_length=40)
    type_desc = models.CharField(max_length=200, blank=True, null=True)
    category = "Other"
    load_order = 1

    def __str__(self):
        return self.type_name

    class Meta:
        abstract = True
        managed = IsManaged


class Image(DescriptiveModel):
    image_url = models.URLField()
    image_caption = models.CharField(max_length=200, blank=True, null=True)
    description = "A link to an image"
    pk_desc = "Standard Auto-Increment PK"
    load_order = 1

    class Meta:
        db_table = "Image"
        verbose_name_plural = "Image"
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
    description = 'The Brand that supplies certain Products'
    brand_name = models.CharField(max_length=80)
    brand_desc = models.CharField(max_length=200, blank=True, null=True)
    brand_site = models.URLField()
    load_order = 1

    class Meta:
        db_table = "Brand"
        verbose_name_plural = "Brand"
        managed = IsManaged

    def __str__(self):
        return self.brand_name


class Product(DescriptiveModel):
    description = 'Anything sold by a Store'
    product_name = models.CharField(max_length=80)
    product_desc = models.CharField(max_length=200, blank=True, null=True)
    product_price = models.DecimalField(max_digits=19, decimal_places=4, default=0)
    product_brand = models.ForeignKey(Brand, on_delete=models.RESTRICT)
    product_status = models.ForeignKey(ProductStatus, on_delete=models.RESTRICT)
    product_tags = models.ManyToManyField(ProductTag, through="ProductProductTag")
    product_images = models.ManyToManyField(Image, through="ProductImage")
    created_date = models.DateField(name="created_date")
    load_order = 2
    list_fields = ["product_name", "product_desc", "created_date", "product_status"]
    list_headers = ["Product Name", "Product Desc", "Created", "Status"]

    class Meta:
        db_table = "Product"
        verbose_name_plural = "Product"
        managed = IsManaged

    def __str__(self):
        return self.product_name


class Promo(DescriptiveModel):
    description = 'Describes a promotion for a group of products'
    promo_name = models.CharField(max_length=80)
    promo_code = models.CharField(max_length=10, unique=True)
    promo_status = models.ForeignKey(PromoStatus, on_delete=models.RESTRICT)
    promo_products = models.ManyToManyField(Product, through="ProductPromo")
    created_date = models.DateField()
    load_order = 2
    list_fields = ["promo_name", "promo_code", "promo_status"]
    list_headers = ["Promo Name", "Promo Code", "Status"]

    class Meta:
        db_table = "Promo"
        verbose_name_plural = "Promo"
        managed = IsManaged

    def __str__(self):
        return self.promo_name


class ProductProductTag(DescriptiveModel):
    description = 'Used to associate a ProductTag with a Product'
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    product_tag = models.ForeignKey(ProductTag, on_delete=models.RESTRICT)
    created_date = models.DateField()
    load_order = 3

    class Meta:
        db_table = "ProductProductTag"
        verbose_name_plural = "Product Product Tag"
        managed = IsManaged


class ProductImage(DescriptiveModel):
    description = 'Used to associate an Image with a Product'
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    product_image = models.ForeignKey(Image, on_delete=models.RESTRICT)
    load_order = 3

    class Meta:
        db_table = "ProductImage"
        verbose_name_plural = "Product Image"
        managed = IsManaged


class ProductPromo(DescriptiveModel):
    description = 'Used to associate a Product with a Promo'
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    promo = models.ForeignKey(Promo, on_delete=models.RESTRICT)
    load_order = 3

    class Meta:
        db_table = "ProductPromo"
        verbose_name_plural = "Product Promo"
        managed = IsManaged


class Customer(DescriptiveModel):
    description = 'Name and email for a customer who will recieve promo emails'
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    created_date = models.DateField()
    customer_status = models.ForeignKey(CustomerStatus, on_delete=models.RESTRICT)
    load_order = 1

    class Meta:
        db_table = "Customer"
        verbose_name_plural = "Customer"
        managed = IsManaged
